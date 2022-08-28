# IMPORTS
import asyncio
from datetime import datetime
from random import randint

import discord
from AdminCommands import *
from BotTokens import BOT_TOKEN
from discord import Intents
from discord.ext import tasks
from EmbedMessages import *
from EnvironmentVariables import *
from HandleRoles import *
from LevelSystem import *
from MusicHandler import *
from ReplyMessages import *

# INICIALIZAR CLIENTE DE DISCORD
intents = Intents.all()
client = discord.Client(intents=intents)

# MENSAJE AL INICIAR EL BOT
@client.event
async def on_ready():
    print('siri mais incrível do mundo\n---------------------------')

# TAREA QUE SE CORRE CADA 24 HORAS
@tasks.loop(hours=24)
async def called_once_a_day():
    lobby_channel = client.get_channel(LOBBY_TEXT_CHANNEL_ID)
    fazendoplata_channel = client.get_channel(LOBBY_TEXT_CHANNEL_ID)
    # ENVIAR MENSAJES DIARIOS
    await AdminCommands.daily_message(lobby_channel)
    # await AdminCommands.daily_new(fazendoplata_channel)
    EmbedMessages.send_embed_msg(fazendoplata_channel,None,AdminCommands.daily_USD_to_COP())
    
    # REVISAR SI EL DIA DE HOY CUMPLE ALGUN MIEMBRO PARA ENVIAR MENSAJE DE FELICITACION
    await LevelSystem.check_birthday(lobby_channel,client)

@called_once_a_day.before_loop
async def before():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Hora actual =", current_time)
    if current_time < '12:00:00' and current_time > '00:00:00':
        hours_left = 12-int(current_time[0:2])
    elif current_time > '12:00:00' and current_time < '24:00:00':
        hours_left = (24-int(current_time[0:2]))+12
    print("Esperando {} horas para enviar el mensaje diario".format(hours_left)+'\n---------------------------')
    await asyncio.sleep(hours_left*60*60)
    print("Mensaje diario enviado")

# FUNCIONES CON MENSAJES DE TEXTO EN CANALES
@client.event
async def on_message(original_message):
    global chance
    global pending_pick

    text = original_message.content
    channel = original_message.channel
    message_author = original_message.author
    
    # IGNORAR MENSAJES DE BOTS, TANTO SIRI COMO OTROS BOTS
    if message_author == client.user or message_author.bot:
        return

    # ELSE, EL MENSAJE NO VIENE DE NINGUN BOT
    await ReplyMessages.process_messages(channel,text,original_message)
    await AdminCommands.process_commands(channel,text,original_message)
    await MusicHandler.process_commands(channel,text,original_message,client)
    await LevelSystem.process_commands(channel,text,original_message,client)
    

# CONECTAR BOT AL VOICE Y LIMPIAR VARIABLES CUANDO SE DESCONECTA DE CUALQUIER CANAL DE VOZ
@client.event
async def on_voice_state_update(member, before, after):
    global voice_client_playing
    global songs_titles
    global URL_queue
    global adding_song

    before_channel = before.channel
    after_channel = after.channel

    if member.id == BOT_ID:
        if after.mute == True or after.suppress == True:
            await member.edit(mute=False)
        if before_channel is not None and after_channel is None:
            voice_client_playing = None
            songs_titles = []
            URL_queue = []
            adding_song = False  

# SALUDAR MIEMBROS NUEVOS CUANDO ACEPTAN LAS REGLAS (CRIBADO DE MIEMBROS)
@client.event
async def on_member_update(memberBefore, memberAfter):
    if memberBefore.pending == True and memberAfter.pending == False:
        guild = client.get_guild(SERVER_ID)
        role = discord.utils.get(guild.roles, id=AMATEUR_ROLE_ID)
        await memberAfter.add_roles(role)
        print("Added welcome role: ", role)
        channel = guild.get_channel(LOBBY_TEXT_CHANNEL_ID)
        await asyncio.sleep(2)
        random_index = randint(0, len(welcome_gifs) - 1)
        await channel.send(client.get_user(memberAfter.id).mention)
        await channel.send(welcome_gifs[random_index])

# AGREGAR O QUITAR ROLES CON REACCIONES
@client.event
async def on_raw_reaction_add(payload):
    is_for_roles = not payload.user_id == BOT_ID and payload.emoji.name != '⏭️' and payload.emoji.name !='⏸️' and payload.emoji.name !='▶️'
    
    if is_for_roles :
        await HandleRoles.remove_or_add_role(client,payload,True)
    else:
        await MusicHandler.control_music_with_reactions(payload,client)

@client.event
async def on_raw_reaction_remove(payload):
    is_for_roles = not payload.user_id == BOT_ID and payload.emoji.name != '⏭️' and payload.emoji.name !='⏸️' and payload.emoji.name !='▶️'

    if is_for_roles:
        await HandleRoles.remove_or_add_role(client,payload,False)

# CORRER BOT
called_once_a_day.start()
client.run(BOT_TOKEN)
