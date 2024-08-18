import io
import os
import re
import sys
import functools
import configparser

#import discord
import pydub
from pydub.effects import speedup
#from discord import app_commands
import nextcord
from nextcord.ext import commands
from nextcord import application_command
from datetime import datetime

# test
from config import BOT
from pydub import AudioSegment

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
	msg = await message.reply("🐁💨 Acceleratioooonnnn...", mention_author=False)
    # Read voice file and converts it into something pydub can work with
	voice_file_bytes = await message.attachments[0].read()
	voice_file = io.BytesIO(voice_file_bytes)
	
	# Convert original .ogg file into a .wav file
	x = pydub.AudioSegment.from_file(voice_file)
	final = speedup(x, speed,150,25)
	buffer = io.BytesIO()
	timenow = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
	#final.export("C:/Users/Aurore/Documents/project/Discord-Bot-Speed-Audio/temp/"+ timenow +".mp3",format="mp3")
	final.export(buffer, format="mp3")
	nextcordFile = nextcord.File(fp=buffer ,filename=timenow + '.mp3')
	await msg.edit(content="Acceleration x"+str(speed)+" terminée Amigos ! :cowboy: ", file=nextcordFile)
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