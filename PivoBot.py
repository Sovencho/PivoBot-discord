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
@bot.command(pass_context=True, aliases=['l'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Вышел из {channel}")
    else:
        await ctx.send("Я не нахожусь в голосовом чате для отключения")


@bot.command(pass_context=True, aliases=['p'])
async def play(ctx, url: str):

    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"Бот подключился к {channel}\n")
        await ctx.send(f"Подключился к каналу {channel}")

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("Больше нет треков в очереди\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "/" + first_file)
            if length != 0:
                print("Трек закончился! Проигрывается следующий\n")
                print(f"Трек в очереди: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 1

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("Не найдено треков после окончания очереди\n")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Удаление старого файла трека")
    except PermissionError:
        print("Попытка удаления файла в то время, пока он проигрываетя")
        await ctx.send("ОШИБКА: Трек проигрывается")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Удаление старой папки очереди")
            shutil.rmtree(Queue_folder)
    except:
        print("Не найдено старой папки очереди")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Скачивание трека\n")
            ydl.download([url])
    except:
        c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -f " + '"' + c_path + '"' + " -s " + url)

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Переименован файл: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1

    nname = name.rsplit("-", 2)
    await ctx.send(f"Проигрывается: {nname[0]}")
    print("Трек проигрывается\n")


@bot.command(pass_context=True, aliases=['pau'])
async def pause(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Трек на паузе")
        voice.pause()
        await ctx.send("Трек на паузе")
    else:
        print("Трек не проигрывается, пауза не была осуществлена")
        await ctx.send("Трек не проигрывается, пауза не была осуществлена")


@bot.command(pass_context=True, aliases=['r'])
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Трек проигрывается дальше")
        voice.resume()
        await ctx.send("Трек проигрывается дальше")
    else:
        print("Трек не был на паузе")
        await ctx.send("Трек не был на паузе")


@bot.command(pass_context=True)
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    queues.clear()

    queue_infile = os.path.isdir("./Queue")
    if queue_infile is True:
        shutil.rmtree("./Queue")

    if voice and voice.is_playing():
        print("Трек остановился")
        voice.stop()
        await ctx.send("Трек остановился")
    else:
        print("Не было проигрывающихся треков для остановки")
        await ctx.send("Не было проигрывающихся треков для остановки")


queues = {}

@bot.command(pass_context=True, aliases=['q'])
async def queue(ctx, url: str):
    if not os.path.isdir("./Queue"):
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Скачивание аудио\n")
        ydl.download([url])
    await ctx.send("Добавлен трек " + str(q_num) + " в очередь")

    print("Добавлен трек в очередь\n")

#-------------------------------------------------------------
@bot.command(pass_context=True, aliases=['s'])
async def skip(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.stop()
        await ctx.send("Проигрывается следующий трек")

#--------------------------------------------------------------------
@bot.command(pass_context=True)
async def cat(ctx):
    response = requests.get("https://aws.random.cat/meow")
    data = response.json()
    await ctx.send(data["file"])

#--------------------------------------------------------------------
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

#-----------------------------------------------------------------------
@bot.command()
async def pivo(ctx):
    await ctx.send("Получи своё цифровое пиво в ебало и свали нахер :beer: :heart:")


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
    embed.add_field(name = "Страница разработчика в VK", value = "https://vk.com/sovencho")
    
    await ctx.send(embed=embed)


bot.run(TOKEN)