import os
import shutil
from os import system
import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get
import random
from random import randint
import asyncio
import requests

print ("Введите токен:")
TOKEN = input()
BOT_PREFIX = 'p!'

bot = commands.Bot(command_prefix=BOT_PREFIX)
bot.remove_command('help')

@bot.event
async def on_ready():
    print("Залогинен как: " + bot.user.name)
    print(f"----------\n")

#--------------------------------------------------------------------
@bot.command(pass_context=True)
async def cat(ctx):
    response = requests.get("https://aws.random.cat/meow")
    data = response.json()
    await ctx.send(data["file"])

@bot.command(pass_context=True)
async def dog(ctx):
    respone = requests.get("https://dog.ceo/api/breeds/image/random")
    data = respone.json()
    await ctx.send(data["message"])

#---------------------------------------------------------------------
@bot.command(pass_context=True)
async def roll(ctx, *, x):
    try:
        x = int(x)
        y = randint(1, x)
        await ctx.send('Ролл: ' + str(y))
    except:
        await ctx.send("ОШИБКА: В команде должны использоваться только целочисленные от 1 (использование дробных также приводит к ошибке)")

#----------------------------------------------------------------------
@bot.command()
async def avatar(ctx, *, member: discord.Member=None):
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar_url
    await ctx.send(userAvatar)

#-----------------------------------------------------------------------
@bot.command()
async def howgay(ctx):
    y = randint(1, 101)
    await ctx.send("Ты гей на " + str(y) + "% :rainbow_flag:")

#------------------------------------------------------------------------
@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.orange()
    )

    embed.set_author(name = "Список команд бота")
   
    embed.add_field(name = "p!cat", value = "Отправка рандомной картинки котиков :3")
    embed.add_field(name = "p!roll {число}", value = "Рандомное число от 1 до указанного в команде числа")
    embed.add_field(name = "p!avatar", value = "Отправка вашего аватара или аватара пользователя")
    embed.add_field(name = "p!dog", value = "Отправка рандомной картинки пёсиков :3")
    embed.add_field(name = "p!credits", value = "Инфа о разрабе, проекте и отдельные благодарности .с.")
    embed.add_field(name = 'p!howgay', value = 'Узнать на сколько ты гей :D')

    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def credits(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.orange()
        )
    embed.set_author(name = "Кредитс .с.")
    embed.add_field(name = "Разработчик", value = 'Разработчиком бота является Егор Совенчов, или же "Sovencho"')
    embed.add_field(name = "Страница в ВК разработчика", value = "https://vk.com/sovencho")
    embed.add_field(name = "Страница проекта на GitHub", value = "https://github.com/Sovencho/PivoBot-discord")
    embed.add_field(name = "Отдельные благодарности", value = "Отдельные благодарности таким людям как /dank/nil и im_tem")
    embed.add_field(name = "Материальная поддержка", value = "VISA - 4276 4413 2346 1876")
    
    await ctx.send(embed=embed)


bot.run(TOKEN)