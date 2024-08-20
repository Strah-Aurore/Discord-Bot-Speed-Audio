import io
import os
import cv2
import numpy
from unidecode import unidecode
from datetime import timezone, datetime, timedelta

import nextcord
from nextcord.ext import commands

from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.effects import speedup
from moviepy.editor import AudioFileClip, ImageClip

from config import BOT
BOT_TOKEN = BOT['TOKEN'];
# the servers you want the bot to run in
default_guild_ids = [458374228023050252]

intents = nextcord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
	print("Hola muchachos !")
	
async def speedup_message(interaction, message, speed):
	# answering with a temp message
	await interaction.response.send_message(content="Arriba ! Arriba ! Je te prépare ça dès que possible !", ephemeral=True)
	# checking there is an attachments (no text-only message) and then checking the type of the attachments (so it's audio)
	if len(message.attachments) == 0 or message.attachments[0].content_type != "audio/ogg":
		await message.reply("Ay Caramba ! Ton message a l'air de ne contenir aucun audio..", mention_author=False)
		return
    # putting the voice message and the user avatar in a variable
	voice_file_bytes = await message.attachments[0].read()
	avatar_bytes = await message.author.avatar.read()
	# In the previous tests I did, the sped up voice sounded like a "chipmunk" and somes words were difficult to understand
	# So I did some processing here to make the audio clearer
	chunks = split_on_silence(AudioSegment.from_file(io.BytesIO(voice_file_bytes)), min_silence_len=200, silence_thresh=-40)
	accelerated_chunks = [speedup(chunk, playback_speed=speed, chunk_size=50, crossfade=10) for chunk in chunks]
	final = AudioSegment.silent(duration=0)
	for chunk in accelerated_chunks:
		final += chunk + AudioSegment.silent(duration=10)
	# getting the actuel time to name the file and the temp file (not necessary)
	timenow = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
	# exporting the accelerated mp3
	final.export("./"+ timenow +".mp3",format="mp3")
	# getting the base layer for the mp4 banner and then putting info on the video banner
	# (such as User avatar, acceleration, duration, what channel it's from)
	banner = cv2.imread("./ImageToVideo.jpg")
	banner[20:120,20:120]=cv2.resize(cv2.imdecode(numpy.fromstring(io.BytesIO(avatar_bytes).read(), numpy.uint8), cv2.IMREAD_COLOR),(100,100), cv2.INTER_LINEAR)
	banner = cv2.putText(banner, "Speed : x" + str(speed), (220,45), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,255), 1, cv2.LINE_AA)
	banner = cv2.putText(banner, "In " + unidecode(str(message.channel.name)) + " at " + str(message.created_at.astimezone(timezone(timedelta(hours=2))).strftime('%Y-%m-%d %H:%M:%S')), (140,100), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255), 1, cv2.LINE_AA)
	banner = cv2.putText(banner, "Duration : "+ str(AudioSegment.__len__(final)/1000) + "s", (220,70), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,255), 1, cv2.LINE_AA)
	# exporting the final banner
	cv2.imwrite("./banner.jpg", banner)
	# importing back the mp3 file, couldn't find a proper way to do it
	# I couldn't just pass it like a variable because the speed up extension is different from the video one
	audio_clip = AudioFileClip("./"+ timenow +".mp3")
	# here it fuse together the mp3 and the banner (and it enter some settings)
	# you may think it's a weird thing to do
	# But right now, Discord unfortunatly doesn't support embed for audio file on mobile
	# so if you send a mp3 file, the user must download it and then play it outside Discord, that's really annoying
	# so I came up with this idea to just fuse it into a mp4 =)
	# and that's great because it allow me to customize it a bit !
	video_clip = ImageClip("./banner.jpg").set_audio(audio_clip)
	video_clip.duration = audio_clip.duration
	video_clip.fps = 30
	# exporting the videofile
	video_clip.write_videofile("./"+ timenow  + '.mp4')
	# importing it back but this time with the Nextcord library
	nextcordFile = nextcord.File("./"+ timenow  + '.mp4')
	# replying to the original message by sending the mp4 and not mentionning
	await message.reply(content="", file=nextcordFile, mention_author=False)
	# and then removing the temporary mp3 and mp4 files
	os.remove("./"+ timenow  + '.mp3')
	os.remove("./banner.jpg")
	os.remove("./"+ timenow  + '.mp4')

# This part of the code looks redundant but it's just to offer many options
@bot.message_command(name="speed 1.25", force_global=True)
async def speed25(interaction: nextcord.Interaction, message: nextcord.Message):
	await speedup_message(interaction, message, 1.25)
	
@bot.message_command(name="speed 1.50", force_global=True)
async def speed50(interaction: nextcord.Interaction, message: nextcord.Message):
	await speedup_message(interaction,message, 1.5)

@bot.message_command(name="speed 1.75", force_global=True)
async def speed75(interaction: nextcord.Interaction, message: nextcord.Message):
	await speedup_message(interaction,message, 1.75)
	
bot.run(BOT_TOKEN)