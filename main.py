import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import chess
import pygame
from chessGame import chessGame
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()
chessChannels = []

class Media:
    def __init__(self):
        self.rouletteImages = []
        imagedir = "ImageRoulette"
        for file in os.listdir(imagedir):
            location = os.path.join(imagedir, file)
            self.rouletteImages.append(location)


media = Media()
client = commands.Bot(command_prefix="!")

chessOn = False
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


@client.command(pass_context=True)
async def chess_start(cxt):
    channelid = cxt.channel.id
    if channelid in chessChannels:
        cxt.channel.send("Chess has already been initialised here!")
        pass

    else:
        chessChannels.append(channelid)
        await cxt.channel.send("Starting up the chess game")
        print("Chess game is initialised")
        gameEngine = chessGame()
        gameEngine.loadImages()
        gameEngine.createImage()
        await cxt.channel.send(file=discord.File("chessImages/board.png"))

        @client.command(pass_context=True)
        async def legal(msg):
            moves = gameEngine.legalMoves()
            await msg.channel.send(moves)

        @client.command(pass_context=True)
        async def move(cxt, *, playerMove):
            moves = gameEngine.legalMoves()
            if playerMove not in moves:
                await cxt.channel.send("That move is not legal!")

            else:
                gameEngine.makeMove(playerMove)
                gameEngine.createImage()
                await cxt.channel.send(file=discord.File("chessImages/board.png"))






client.run(TOKEN)
