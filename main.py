import io
import os
import re
import sys
import functools
import configparser
from moviepy.editor import AudioFileClip, ImageClip
#import discord
import pydub
from pydub.effects import speedup
#from discord import app_commands
import nextcord
from nextcord.ext import commands
from nextcord import application_command
from datetime import datetime
import cv2
import numpy
from unidecode import unidecode
from datetime import timezone, datetime, timedelta
# test
from config import BOT
from pydub import AudioSegment
from pydub.silence import split_on_silence

BOT_TOKEN = BOT['TOKEN'];
default_guild_ids = [458374228023050252]

intents = nextcord.Intents.default()
intents.messages = True
intents.message_content = True
#client = nextcord.Client(command_prefix='!', intents=intents)
#tree = app_commands.CommandTree(client)
bot = commands.Bot(command_prefix='!',intents=intents)
#tree = application_command.CommandTree(bot)

@bot.event
async def on_ready():
	print("Hola muchachos !")
	
async def speedup_message(message, speed):
	if len(message.attachments) == 0:
		await message.reply("Ay Caramba ! Ton message a l'air de ne contenir aucun audio..", mention_author=False)
		return
	if message.attachments[0].content_type != "audio/ogg":
		await message.reply("Ay Caramba ! Ton message n'a l'air de ne contenir aucun audio..", mention_author=False)
		return
	#msg = await message.reply("🐁💨 Acceleratioooonnnn...", mention_author=False)
    # Read voice file and converts it into something pydub can work with
	voice_file_bytes = await message.attachments[0].read()
	voice_file = io.BytesIO(voice_file_bytes)
	avatar_bytes = await message.author.avatar.read()
	banner = cv2.imread("./ImageToVideo.jpg")
	BytesToImg = numpy.fromstring(io.BytesIO(avatar_bytes).read(), numpy.uint8)
	avatar_cv = cv2.resize(cv2.imdecode(BytesToImg, cv2.IMREAD_COLOR),(100,100), cv2.INTER_LINEAR)
	banner[20:120,20:120]=avatar_cv
	banner = cv2.putText(banner, "Speed : x" + str(speed), (220,45), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,255), 1, cv2.LINE_AA)
	banner = cv2.putText(banner, "In " + unidecode(str(message.channel.name)) + " at " + str(message.created_at.astimezone(timezone(timedelta(hours=2))).strftime('%Y-%m-%d %H:%M:%S')), (140,100), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255), 1, cv2.LINE_AA)

	
	# Convert original .ogg file into a .wav file
	x = pydub.AudioSegment.from_file(voice_file)
	#final = speedup(x, speed,150,25)

	# Diviser l'audio en segments en fonction des silences
	chunks = split_on_silence(x, min_silence_len=200, silence_thresh=-40)

# Accélérer chaque segment individuellement
	accelerated_chunks = [speedup(chunk, playback_speed=speed, chunk_size=50, crossfade=10) for chunk in chunks]

# Rejoindre les segments accélérés avec un léger fondu pour maintenir la fluidité
	final = AudioSegment.silent(duration=0)
	for chunk in accelerated_chunks:
		final += chunk + AudioSegment.silent(duration=10)

	buffer = io.BytesIO()
	timenow = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
	final.export("./"+ timenow +".mp3",format="mp3")
	banner = cv2.putText(banner, "Duration : "+ str(pydub.AudioSegment.__len__(final)/1000) + "s", (220,70), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,255), 1, cv2.LINE_AA)

	audio_clip = AudioFileClip("./"+ timenow +".mp3")
	cv2.imwrite("./banner.jpg", banner)
	image_clip = ImageClip("./banner.jpg")
	
	video_clip = image_clip.set_audio(audio_clip)
	video_clip.duration = audio_clip.duration
	video_clip.fps = 30

	#video_clip.export(buffer, format="mp4")
	#nextcordFile = nextcord.File(fp=buffer ,filename=timenow + '.mp4')
	video_clip.write_videofile("./"+ timenow  + '.mp4')
	nextcordFile = nextcord.File("./"+ timenow  + '.mp4')
	

	await message.reply(content="", file=nextcordFile)

	os.remove("./"+ timenow  + '.mp3')
	os.remove("./banner.jpg")
	os.remove("./"+ timenow  + '.mp4')
    #new = io.BytesIO()
	#await bot.loop.run_in_executor(None, functools.partial(x.export, new, format='wav'))


	
@bot.message_command(name="speed 1.25", force_global=True)
async def speed25(interaction: nextcord.Interaction, message: nextcord.Message):
	await interaction.response.send_message(content="Arriba ! Arriba ! Je te prépare ça dès que possible !", ephemeral=True)
	await speedup_message(message, 1.25)
	
@bot.message_command(name="speed 1.50", force_global=True)
async def speed50(interaction: nextcord.Interaction, message: nextcord.Message):
	await interaction.response.send_message(content="Arriba ! Arriba ! Je te prépare ça dès que possible !", ephemeral=True)
	await speedup_message(message, 1.5)

@bot.message_command(name="speed 1.75", force_global=True)
async def speed75(interaction: nextcord.Interaction, message: nextcord.Message):
	await interaction.response.send_message(content="Arriba ! Arriba ! Je te prépare ça dès que possible !", ephemeral=True)
	await speedup_message(message, 1.75)
	
bot.run(BOT_TOKEN)