import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
from chessGame import chessGame
import uuid
import requests
import shutil

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()
chessGameObject = {}
chessGameExist = {}


class Media:
    def __init__(self):
        self.path = "rouletteImages/"
        self.safePath = "rouletteImages"
        try:
            os.makedirs(self.path)

        except FileExistsError:
            pass

    def createDir(self, id):
        imageDir = self.path + str(id) + "-rouletteImages"
        os.makedirs(imageDir)
        print("Dir made")

    def checkDir(self, id):
        fileIs = False
        for file in os.listdir(self.safePath):
            file = file.split("-")
            file = file[0]
            file = file.split("/")
            file = int(file[0])
            if file == id:
                fileIs = True

        if not fileIs:
            self.createDir(id)
            print(f"Directory created for guild id {id}")

    def fetchImage(self, id):
        images = []
        path = self.path + str(id) + "-rouletteImages"
        for file in os.listdir(path):
            imagePath = os.path.join(path, file)
            images.append(imagePath)

        return images

    def saveImage(self, r, name, id):
        path = self.path + str(id) + "-rouletteImages/"
        with open((path + name), 'wb') as destination:
            print(f"Saving image with name {name} to path {destination}")
            shutil.copyfileobj(r.raw, destination)


media = Media()
client = commands.Bot(command_prefix="!")

rouletteFreeSend = {}


@client.event
async def on_ready():
    print(f" {client.user} has successfully connected to discord")
    for guilds in client.guilds:
        print(f"Bot is connected to {guilds} ID:{guilds.id}")


@client.command(pass_context=True)
async def roulette_free(cxt):
    try:
        rouletteFreeSend[cxt.guild.id]

    except KeyError:
        rouletteFreeSend[cxt.guild.id] = False

    change = False
    while not change:
        if not rouletteFreeSend[cxt.guild.id]:
            rouletteFreeSend[cxt.guild.id] = True
            await cxt.channel.send("!roulette can now be used anywhere")
            break

        elif rouletteFreeSend[cxt.guild.id]:
            rouletteFreeSend[cxt.guild.id] = False
            await cxt.channel.send("!roulette can now only be used in the roulette channel")
            break


@client.command(pass_context=True)
async def roulette_upload(ctx):
    try:
        url = ctx.message.attachments[0].url

    except IndexError:
        print("Unrecognised attachment")
        await ctx.channel.send("Either there is no attachment, or it is not recognised")

    else:
        if url[0:26] == "https://cdn.discordapp.com":
            r = requests.get(url, stream=True)
            imageName = str(uuid.uuid4()) + '.jpg'
            media.saveImage(r, imageName, ctx.guild.id)
            await ctx.channel.send("Your image has been saved to the roulette pool!")


@client.command(pass_context=True)
async def roulette(cxt):
    try:
        rouletteFreeSend[cxt.guild.id]

    except KeyError:
        rouletteFreeSend[cxt.guild.id] = False

    # above makes sure the server that sent the message is in the server dict

    media.checkDir(cxt.guild.id)  # makes sure there is a dir for each specific server

    if rouletteFreeSend[cxt.guild.id]:  # if you can use anywhere
        images = media.fetchImage(cxt.guild.id)
        if len(images) != 0:
            await cxt.channel.send(file=discord.File(random.choice(images)))  # sends a random image
            print(f"Roulette image sent to channel {cxt.channel.name}")

        else:
            await cxt.channel.send("This server has no roulette images, please use !roulette_upload and an image"
                                   " within the same message to upload some!")

    if not rouletteFreeSend[cxt.guild.id]:  # if cannot send anywhere
        if cxt.channel.name == "roulette":
            images = media.fetchImage(cxt.guild.id)
            if len(images) != 0:
                await cxt.channel.send(file=discord.File(random.choice(images)))  # sends a random image
                print(f"Roulette image sent to channel {cxt.channel.name}")

            else:
                await cxt.channel.send("This server has no roulette images, please use !roulette_upload and an image"
                                       " within the same message to upload some!")
        else:
            channelExist = False
            for chn in cxt.guild.text_channels:
                if chn == "roulette":
                    channelExist = True

            if channelExist:
                await cxt.channel.send("Please use this command in the roulette channel! Toggle the need for"
                                       " a specific channel with !roulette_free")

            else:
                await cxt.channel.send("Please create a channel called 'roulette' or use the command !roulette_free"
                                       " to use this command anywhere")


@client.command(pass_context=True)
async def online(msg):
    await msg.channel.send(" I am online!")


@client.command(pass_context=True)
async def chess_start(cxt):
    channelid = cxt.channel.id
    try:
        if chessGameExist[channelid]:
            await cxt.channel.send("You already have a chess game in this channel!")

    except KeyError:
        chessGameExist[channelid] = True
        chessGameObject[channelid] = chessGame(channelid)
        await cxt.channel.send("Starting up the chess game!")
        print(f"Chess game init at id {channelid}")
        chessGameObject[channelid].updateBoard()
        await cxt.channel.send(file=discord.File(chessGameObject[channelid].imagePath))


@client.command(pass_context=True)
async def legal(ctx):
    try:
        moves = chessGameObject[ctx.channel.id].legalMoves()
        await ctx.channel.send(moves)

    except KeyError:
        await ctx.channel.send("Please start a chess game in this channel with !chess_start")


@client.command(pass_context=True)
async def move(ctx, *, playerMove):
    try:
        moves = chessGameObject[ctx.channel.id].legalMoves()
        if playerMove not in moves:
            await ctx.channel.send("That move is not legal!")

        else:
            chessGameObject[ctx.channel.id].makeMove(playerMove)
            chessGameObject[ctx.channel.id].updateBoard()
            await ctx.channel.send(file=discord.File(chessGameObject[ctx.channel.id].imagePath))

    except KeyError:
        await ctx.channel.send("There is no game in this channel, please user !chess_start to make one!")


@client.command(pass_context=True)
async def show_board(ctx):
    try:
        await ctx.channel.send(file=discord.File(chessGameObject[ctx.channel.id].imagePath))

    except KeyError:
        await ctx.channel.send("There is no game in this channel, please use !chess_start to make one!")


@client.command(pass_context=True)
async def reset_board(ctx):
    try:
        if chessGameExist[ctx.channel.id]:
            chessGameObject[ctx.channel.id].resetBoard()
            await ctx.channel.send(file=discord.File(chessGameObject[ctx.channel.id].imagePath))

    except KeyError:
        await ctx.channel.send("There is no game in this channel, please use !chess_start to make one!")


@client.command(pass_context=True)
async def jake(ctx, *args):
    message = ""
    for words in args:
        message = (words[0] + "-") * random.randint(1, 4) + words
    await ctx.channel.send(message)


@client.command(pass_context=True)
async def c_help(ctx):
    await ctx.channel.send("```!online to check online status"
                           "\n\n!roulette to send a roulette message to that channel"
                           "\n\n!roulette_free to toggle the !roulette commands required channel"
                           "\n\n!roulette_upload + an image to upload an image to the roulette"
                           "\n\n!chess_start start a chess game in that channel"
                           "\n\n!move (your move here) to make a move"
                           "\n\n!legal get a list of all the legal moves"
                           "\n\n!show_board get an image of the board"
                           "\n\n!reset_board to reset the chess board"
                           "\n\n!jake 'words here' to stutter words```")


if __name__ == "__main__":
    client.run(TOKEN)
