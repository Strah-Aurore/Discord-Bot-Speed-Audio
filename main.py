import io
import os
import re
import sys
import functools
import configparser

#import discord
import pydub
#from discord import app_commands
import nextcord
from nextcord.ext import commands
from nextcord import application_command

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
	msg = await message.reply("✨ Accelerating...", mention_author=False)
    # Read voice file and converts it into something pydub can work with
	voice_file_bytes = await message.attachments[0].read()
	voice_file = io.BytesIO(voice_file_bytes)
	
	# Convert original .ogg file into a .wav file
	x = pydub.AudioSegment.from_file(voice_file)
	final = pydub.speedup(x, playback_speed=(speed))
	await final.export("C:/Users/Aurore/Documents/project/Bot-Speed-Audio/temp/final.mp3",format="mp3")
	await msg.edit(content="test", attachments=[nextcord.File('C:/Users/Aurore/Documents/project/Bot-Speed-Audio/temp/final.mp3')])
    #new = io.BytesIO()
	#await bot.loop.run_in_executor(None, functools.partial(x.export, new, format='wav'))


	
@bot.message_command(name="accelere 1.25", force_global=True)
async def accelere25(interaction: nextcord.Interaction, message: nextcord.Message):
	await interaction.response.send_message(content="Arriba ! Arriba ! Je te prépare ça dès que possible !", ephemeral=True)
	await speedup_message(message, 1.25)
	
@bot.message_command(name="accelere 1.5", force_global=True)
async def accelere50(interaction: nextcord.Interaction, message: nextcord.Message):
	await interaction.response.send_message(content="Arriba ! Arriba ! Je te prépare ça dès que possible !", ephemeral=True)
	await speedup_message(message, 1.5)

@bot.message_command(name="accelere 1.75", force_global=True)
async def accelere75(interaction: nextcord.Interaction, message: nextcord.Message):
	await interaction.response.send_message(content="Arriba ! Arriba ! Je te prépare ça dès que possible !", ephemeral=True)
	await speedup_message(message, 1.75)
	
bot.run(BOT_TOKEN)