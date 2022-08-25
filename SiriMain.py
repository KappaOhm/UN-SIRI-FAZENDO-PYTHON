# IMPORTS
import asyncio
import calendar
from datetime import date, datetime
from random import randint

import discord
from AdminCommands import *
from BotTokens import BOT_TOKEN
from discord import Intents
from discord.ext import tasks
from EmbedMessages import *
from EnvironmentVariables import *
from HandleRoles import *
from LevelAndCoinsSystem import *
from MusicHandler import *
from ReplyMessages import *

# INICIALIZAR CLIENTE DE DISCORD
intents = Intents.all()
client = discord.Client(intents=intents)

# MENSAJE AL INICIAR EL BOT
@client.event
async def on_ready():
    print('siri mais incrível do mundo\n---------------------------')

# TAREA QUE SE CORRE CADA 24 HORAS, PARA HACER QUE EL BOT ENVIE UN MENSAJE TODOS LOS DIAS A UNA HORA ESPECIFICA  
@tasks.loop(hours=24)
async def called_once_a_day():
    channel = client.get_channel(LOBBY_TEXT_CHANNEL_ID)
    random_index1 = randint(0, len(bomdia_messages) - 1)
    random_index2 = randint(0, len(bomdia_gifs) - 1)
    await EmbedMessages.send_embed_msg(channel,None,bomdia_messages[random_index1])
    await channel.send(bomdia_gifs[random_index2])

    #REVISAR CUMPLEAÑOS
    users = await LevelSystem.read_users_data()
    for user in users:
        today = str(date.today())
        today_no_year = today[len('YYYY-'):]
        month_name = calendar.month_name[int(today_no_year[:len(today_no_year)-len('-DD')])]
        mont_day = today_no_year[len('MM-'):]
        if 'bd' in users[user] and users[user]['bd'] == month_name + " " + mont_day:
            random_index1 = randint(0, len(cum_messsages) - 1)
            random_index2 = randint(0, len(cum_images) - 1)
            await EmbedMessages.send_embed_msg(channel,None,cum_messsages[random_index1] + client.get_user(int(user)).mention )
            await channel.send(cum_images[random_index2])

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
    global is_disconnected

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
            is_disconnected = True        

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
