import os
import discord
from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()


class Media:
    def __init__(self):
        self.rouletteImages = []
        imagedir = "ImageRoulette"
        for file in os.listdir(imagedir):
            location = os.path.join(imagedir, file)
            self.rouletteImages.append(location)


media = Media()
client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print(f" {client.user} has successfully connected to discord")
    for guilds in client.guilds:
        print(f"Bot is connected to {guilds} ID:{guilds.id}")


@client.command(pass_context=True)
async def roulette(msg):
    await msg.channel.send(file=discord.File(random.choice(media.rouletteImages)))
    print(f"Roulette image sent to channel {msg.channel.name}")


@client.command(pass_context=True)
async def online(msg):
    await msg.channel.send(" I am online!")


client.run(TOKEN)
