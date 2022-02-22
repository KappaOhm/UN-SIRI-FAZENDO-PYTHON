# IMPORTS
import discord
import asyncio
import os

from asyncio import sleep
from random import randint, shuffle

from discord import Intents
from discord.ext import tasks
from youtube_dl import YoutubeDL
from datetime import datetime
from discord_components import Button, SelectOption

from level_system import *
from embed_message import *
from reply_messages import *
from handle_roles import *
from vars import *
from bot_tokens import bot_token

# INICIALIZAR CLIENTE DE DISCORD
intents = Intents.all()
client = discord.Client(intents=intents)

dir_path = os.path.dirname(os.path.realpath(__file__))

# MENSAJE AL INICIAR EL BOT
@client.event
async def on_ready():
    print('siri mais incrível do mundo')
    print('---------------------------')
    print(dir_path)
    print('---------------------------')

# TAREA QUE SE CORRE CADA 24 HORAS, PARA HACER QUE EL BOT ENVIE UN MENSAJE TODOS LOS DIAS A UNA HORA ESPECIFICA  
@tasks.loop(hours=24)
async def called_once_a_day():
    channel = client.get_channel(lobby_text_channel_id)
    await embed_message.send_embed_msg(channel,None,"¡Hola Bom Día! ⭐")
    await reply_messages.reply_with_GIF(channel,".gif anime lewd",None)

@called_once_a_day.before_loop
async def before():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    if current_time < '12:00:00' and current_time > '00:00:00':
        hours_left = 12-int(current_time[0:2])
    elif current_time > '12:00:00' and current_time < '24:00:00':
        hours_left = (24-int(current_time[0:2]))+12
    print("Waiting {} hours to send daily message".format(hours_left))
    print('---------------------------')
    await sleep(hours_left*60*60)
    print("Finished waiting")

# DESCONECTAR EL BOT SI DADOS X SEGUNDOS NO HA REPRODUCIDO NADA
async def auto_disconnect(message):
    await sleep(seconds_to_disconnect)
    if voice_client_playing is not None and not voice_client_playing.is_playing():
        print('Desconectado automatico de canal de voz')
        await embed_message.send_embed_msg(message.channel, None, "Me voy por inactividad ⏱️")
        await voice_client_playing.disconnect() 

# ESTA FUNCION SE LLAMA AUTOMATICAMENTE CUANDO UNA CANCION TERMINA (after del .play) O CON EL COMANDO ".next"
# SE ENCARGA DE VERIFICAR SI HAY CANCIONES EN COLA PARA DAR LA ORDEN DE REPRODUCIRLAS O DE LO CONTRARIO VERIFICAR SI DEBE DESCONECTAR EL BOT
def check_queue(message):
    global URL_queue
    global adding_song
    global songs_titles

    if len(URL_queue) > 0:
        asyncio.run_coroutine_threadsafe(
            play_song(message, URL_queue.pop(0)), client.loop)
    else:
        asyncio.run_coroutine_threadsafe(
            auto_disconnect(message), client.loop)

# MANEJO DE COLA PARA CANCIONES
def add_to_queue(adding_song, URL):
    global URL_queue
    if adding_song:
        URL_queue.append(URL)        

# REPRODUCIR CANCIONES EN COLA
async def play_song(message, URL):
    global is_playlist
    global songs_titles
    global song_playing

    if is_playlist or is_shuffled:
        current_song_title = songs_titles[0]
        await embed_message.send_embed_msg(message.channel, "🤟 Reproduciendo", current_song_title)
        songs_titles.pop(0)
    else:
        current_song_title = songs_titles[-1]
        await embed_message.send_embed_msg(message.channel, "🤟 Reproduciendo", current_song_title)
        songs_titles.pop(-1)

    song_playing = current_song_title

    source = await discord.FFmpegOpusAudio.from_probe(URL, **FFMPEG_OPTIONS)
    voice_client_playing.play(source, after=lambda e: check_queue(message))

# IMPRIMIR CANCIONES EN COLA
async def show_queue(message):
    global songs_titles
    global song_playing

    if songs_titles:
        queue = ""
        for x in range(len(songs_titles)+1):
            if x == 0:
                queue = queue + "***" + "1. " + song_playing + " 🎵" + "***" + "\n"
            else:
                queue = queue + "**" + \
                    str(x + 1) + ". " + "**" + songs_titles[x-1] + "\n"
        await embed_message.send_embed_msg(message.channel, "Canciones en cola", queue)
    else:
        await embed_message.send_embed_msg(message.channel, None, "Aqui no hay nada mi ciela🦀")

# CARGAR LA INFORMACION DE UNA BUSQUEDA O URL DE YOUTUBE
def get_YT_info(url_song):
    global songs_titles
    global URL_queue
    global is_playlist

    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url_song, download=False)

        if 'youtu' in url_song:
            if 'entries' in info:
                is_playlist = True
                for i in info['entries']:
                    URL = i['formats'][0]['url']
                    songs_titles.append(i.get('title', None))
                    URL_queue.append(URL)
            else:
                URL = info['formats'][0]['url']
                songs_titles.append(info.get('title', None))

        else:
            new_url_song = info['entries'][0]['webpage_url']
            new_info = ydl.extract_info(new_url_song, download=False)
            URL = new_info['formats'][0]['url']
            songs_titles.append(new_info['title'])

        if is_playlist:
            return URL_queue[0]
        else:
            return URL

# FUNCIONES CON MENSAJES DE TEXTO EN CANALES
@client.event
async def on_message(message):
    global voice_client_playing
    global voice_client_mimir
    global playing_mimir
    global adding_song
    global songs_titles
    global URL_queue
    global is_playlist
    global is_shuffled

    # IGNORAR MENSAJES DE BOTS, TANTO SIRI COMO OTROS
    if message.author == client.user or message.author.bot:
        return

    # ELSE, EL MENSAJE NO VIENE DE NINGUN BOT
    text = message.content
    await reply_messages.handle_messages(text,message)
    await reply_messages.reply_with_GIF(message.channel,text,message)
        
    # SISTEMA DE XP POR MENSAJES

    # SOLO MENSAJES DE MÁS DE 10 CARACTERES CUENTAN PARA XP
    if message.channel.id != dungeon_text_channel_id and (len(text) > 10 or len(message.attachments) > 0):
        
        users = await level_system.read_users_data()

        # MENSAJES CON INSERCIONES DE IMAGENES DAN EL TRIPLE DE XP
        xp_points = 15 if (len(message.attachments) > 0 and message.channel.id !=shitpost_text_channel_id) else 5
        await level_system.update_data(users, str(message.author.id))
        await level_system.add_experience(users, str(message.author.id), xp_points)
        await level_system.level_up(users, message.author, message.channel,client)

        await level_system.write_users_data(users)

    # COMANDO PARA REVISAR EXPERIENCIA PROPIA O DE OTRO USUARIO
    if text.startswith('.xp'):
        if text == '.xp':
            await level_system.check_xp(None, message.author, message.channel)
        else:
            await level_system.check_xp(message, None, None)

    # COMANDO LEADERBOARD
    if text == '.lb':
        await level_system.get_xp_leaderboard(message.channel,client)

    # COMANDO APOSTAR POR PAR
    if text.startswith('.par') and message.channel.id == chat_con_siri_channel_id:
        await level_system.bet_par_impar(message, 0)

    # COMANDO APOSTAR POR IMPAR
    if text.startswith('.impar') and message.channel.id == chat_con_siri_channel_id:
        await level_system.bet_par_impar(message, 1)

    # DAR MONEDAS
    if text.startswith('.award') and message.author.id == id_kappa:
        users = await level_system.read_users_data()
        number_of_coins = int(text[len(text)-2:len(text)])
        user = message.mentions[0]
        users[str(user.id)]['coins'] += number_of_coins
        await message.channel.send(user.mention)
        await embed_message.send_embed_msg(message.channel, None, "¡Te han otorgado " + str(number_of_coins) + "" + siri_fazendo_plata_emoji + " monedas!")
        await level_system.write_users_data(users)

    # COMANDO PLAY
    if text.startswith('.play') or (text.startswith('.p') and ".par" not in text) and (message.channel.id == chat_con_siri_channel_id):

        if message.author.voice is None:
            await embed_message.send_embed_msg(message.channel, None, "No estas en un canal de voz 🦀")
        else:
            if voice_client_playing is not None and voice_client_playing.is_playing() and voice_client_playing.channel.id != message.author.voice.channel.id:
                await embed_message.send_embed_msg(message.channel, None, "Ya estoy ocupado en otro canal de voz🦀")
            else:
                if text.startswith('.play'):
                    url_song = text.replace('.play ', '')
                elif text.startswith('.p'):
                    url_song = text.replace('.p ', '')
                try:
                    is_playlist = False
                    if 'list' in url_song:
                        await embed_message.send_embed_msg(message.channel, None, "🎶 Descargando playlist...")
                    URL = get_YT_info(url_song)

                    if is_playlist and voice_client_playing is None and len(URL_queue) > 0:
                        voice_client_playing = await message.author.voice.channel.connect()
                        adding_song = True
                        await play_song(message, URL_queue.pop(0))

                    else:
                        if voice_client_playing is None and adding_song == False:
                            voice_client_playing = await message.author.voice.channel.connect()
                            adding_song = True
                            add_to_queue(adding_song, URL)
                        else:
                            add_to_queue(adding_song, URL)
                            if len(URL_queue) > 0:
                                await message.add_reaction('🌟')
                                if is_playlist:
                                    await embed_message.send_embed_msg(message.channel, None, "Playlist agregada 🎶")
                                else:
                                    await embed_message.send_embed_msg(message.channel, "Cancion agregada 🦀", songs_titles[-1])

                        if len(URL_queue) > 0 and voice_client_playing.is_playing() == False:
                            await play_song(message, URL_queue.pop(0))
                except Exception as error:
                    print(error)
                    await embed_message.send_embed_msg(message.channel, "Error", error.__context__.args[0])

    # COMANDO NEXT
    if text == '.next' or text == '.n' and (message.channel.id == chat_con_siri_channel_id):
        if voice_client_playing is not None and len(URL_queue) > 0:
            voice_client_playing.pause()
            await embed_message.send_embed_msg(message.channel, "Siguiente canción 🦀", None)
            check_queue(message)
        else:
            adding_song = False
            await embed_message.send_embed_msg(message.channel, None, "Aqui no hay nada mi ciela 🦀")

     # COMANDO SHUFFLE
    if text == '.shuffle' or text == '.s' and (message.channel.id == chat_con_siri_channel_id):
        if voice_client_playing is not None and len(URL_queue) > 0:
            await embed_message.send_embed_msg(message.channel, None, " 🧙🌟 ==> 🎲🎵")

            songs_titles_shuffled = []
            URL_queue_shuffled = []
            index_shuf = list(range(len(songs_titles)))
            shuffle(index_shuf)
            for i in index_shuf:
                songs_titles_shuffled.append(songs_titles[i])
                URL_queue_shuffled.append(URL_queue[i])

            songs_titles = songs_titles_shuffled
            URL_queue = URL_queue_shuffled

            is_shuffled = True

            await show_queue(message)

        else:
            adding_song = False
            await embed_message.send_embed_msg(message.channel, None, "Aqui no hay nada mi ciela 🦀")        

    # COMANDO STOP
    if text == '.stop' and (message.channel.id == chat_con_siri_channel_id):
        if voice_client_playing is not None and voice_client_playing.is_playing() == True:
            voice_client_playing.stop()
            URL_queue = []
            songs_titles = []
            is_shuffled = False
            await embed_message.send_embed_msg(message.channel, None, "Reproduccion de música detenida 🦀")

    # COMANDO CLEAR
    if text == '.clear' and message.channel.id == chat_con_siri_channel_id:
        if URL_queue:
            URL_queue = []
            songs_titles = []
            await embed_message.send_embed_msg(message.channel, None, "Cola de reproduccion borrada🎵🤠")
        else:
            await embed_message.send_embed_msg(message.channel, None, "Aqui no hay nada mi ciela 🦀")
        is_shuffled = False

    # COMANDO QUEUE
    if text == '.q' and (message.channel.id == chat_con_siri_channel_id):
        await show_queue(message)

    # COMANDO LEAVE
    if text == '.leave' and (message.channel.id == chat_con_siri_channel_id):
        is_disconnected = False
        if voice_client_mimir is not None:
            voice_client_mimir.stop()
            await voice_client_mimir.disconnect()
            voice_client_mimir = None
            playing_mimir = False
            is_disconnected = True
        if voice_client_playing is not None:
            songs_titles = []
            URL_queue = []
            voice_client_playing.stop()
            await voice_client_playing.disconnect()
            voice_client_playing = None
            adding_song = False
            is_disconnected = True
        if is_disconnected:
            await embed_message.send_embed_msg(message.channel, None,"Ah pero ya me echaron, todo bien🦀🔪")

    # COMANDO MIMIR
    if text.startswith('.mimir') and (message.channel.id == chat_con_siri_channel_id):

        new_url_song = text.replace('.mimir ', '')
        MIMIR_USERS[message.author.id] = new_url_song
        await message.channel.send('`Su nueva música para mimir : `' + new_url_song)

    # COMANDO DE AYUDA
    if text == '.help':
        await embed_message.send_embed_help_msg(message)

    # COMANDO DE COMANDOS XP Y MONEDAS
    if text == '.cmd':
        await embed_message.send_embed_cmd_msg(message)

# CONECTAR BOT AL VOICE CHAT DE AFKs Y LIMPIAR VARIABLES CUANDO SE DESCONECTA DE CUALQUIER CANAL DE VOZ
@client.event
async def on_voice_state_update(member, before, after):
    global voice_client_playing
    global playing_mimir
    global voice_client_mimir
    global songs_titles
    global URL_queue
    global adding_song
    global is_disconnected
    global is_shuffled

    before_channel = before.channel
    after_channel = after.channel
    if member.id == id_bot:
        if after.mute == True or after.suppress == True:
            await member.edit(mute=False)
        if before_channel is not None and before_channel.id == mimir_voice_channel_id and after_channel is None:
            if voice_client_mimir is not None:
                voice_client_mimir.stop()
                await voice_client_mimir.disconnect(force=True)
            playing_mimir = False
            return
        if before_channel is not None and after_channel is None:
            voice_client_playing = None
            adding_song = False
            is_disconnected = True
            is_shuffled = False
            URL_queue = []
            songs_titles = []

    if before_channel is not None and before_channel.id != mimir_voice_channel_id:
        if after_channel is not None and after_channel.id == mimir_voice_channel_id:
            await sleep(1)
            if playing_mimir == False and voice_client_playing is None:
                songs_titles = []
                URL_queue = []
                if MIMIR_USERS.get(member.id) is not None:
                    url_song = MIMIR_USERS[member.id]
                else:
                    url_song = MIMIR_USERS["default"]
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url_song, download=False)
                    URL = info['formats'][0]['url']
                    source = await discord.FFmpegOpusAudio.from_probe(
                        URL, **FFMPEG_OPTIONS)

                    voice_client_mimir = await after_channel.connect()
                    voice_client_mimir.play(source)
                    playing_mimir = True

# SALUDAR MIEMBROS NUEVOS CUANDO ACEPTAN LAS REGLAS (CRIBADO DE MIEMBROS)
@client.event
async def on_member_update(memberBefore, memberAfter):
    if memberBefore.pending == True and memberAfter.pending == False:
        guild = client.get_guild(server_id)
        role = discord.utils.get(guild.roles, id=id_role_Amateur)
        await memberAfter.add_roles(role)
        print("Added welcome role: ", role)
        channel = guild.get_channel(lobby_text_channel_id)
        await sleep(2)
        random_index = randint(0, len(WELCOME_GIFS) - 1)
        await channel.send(client.get_user(memberAfter.id).mention)
        await channel.send(WELCOME_GIFS[random_index])

# AGREGAR O QUITAR ROLES CON REACCIONES
@client.event
async def on_raw_reaction_add(payload):
    await handle_roles.remove_or_add_role(client,payload,True)

@client.event
async def on_raw_reaction_remove(payload):
    await handle_roles.remove_or_add_role(client,payload,False)

# CORRER BOT
called_once_a_day.start()
client.run(bot_token)