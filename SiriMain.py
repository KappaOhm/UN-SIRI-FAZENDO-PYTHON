# IMPORTS
import asyncio
import calendar
from datetime import date, datetime
from random import randint, shuffle

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
    #await ReplyMessages.process_messages(channel,".gif bom dia",None)

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
    print("Current Time =", current_time)
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

    # SISTEMA DE XP POR MENSAJES
    # SOLO MENSAJES DE MÁS DE 10 CARACTERES CUENTAN PARA XP
    if channel.id != DUNGEON_TEXT_CHANNEL_ID and (len(text) > 10 or len(original_message.attachments) > 0):

        users = await LevelSystem.read_users_data()

        # MENSAJES CON INSERCIONES DE IMAGENES DAN EL TRIPLE DE XP
        xp_points = 15 if (len(original_message.attachments) > 0 and channel.id !=SHITPOST_TEXT_CHANNEL_ID) else 5

        # PLANTAR MONEDAS CON CIERTA PROPABILIDAD CADA VEZ QUE SE ENVIA UN MENSAJE
        if channel.id not in not_allowed_channel_ids and pending_pick==False:
            if (randint(1, 100) + chance) > 100:
                await LevelSystem.plant_coins(channel,None)
            
        await LevelSystem.update_data(users, str(message_author.id))
        await LevelSystem.add_experience(users, str(message_author.id), xp_points)
        await LevelSystem.level_up(users, message_author, channel,client)

        await LevelSystem.write_users_data(users)

    # RECOGER MONEDAS
    if text.startswith('.pick') and channel.id not in not_allowed_channel_ids:
        await LevelSystem.pick_coins(channel,original_message,text)  
      
    # COMANDO PARA REVISAR EXPERIENCIA PROPIA O DE OTRO USUARIO
    if text.startswith('.xp'):
        if text == '.xp':
            await LevelSystem.check_xp(None, message_author, channel)
        else:
            await LevelSystem.check_xp(original_message, None, None)

    # COMANDO LEADERBOARD
    if text == '.lb':
        await LevelSystem.get_xp_leaderboard(channel,client)

    # COMANDO APOSTAR POR PAR
    if text.startswith('.par') and channel.id == SIRI_CHAT_TEXT_CHANNEL_ID:
        await LevelSystem.bet_par_impar(original_message, 0)

    # COMANDO APOSTAR POR IMPAR
    if text.startswith('.impar') and channel.id == SIRI_CHAT_TEXT_CHANNEL_ID:
        await LevelSystem.bet_par_impar(original_message, 1)
          
    # SETEAR UN CUMPLEAÑOS
    if text.startswith('.setcum'):
        try:
            users = await LevelSystem.read_users_data()
            bd_date = text[len('.setcum '):]
            month_number = int(bd_date[len('DD-'):])
            month_name = calendar.month_name[month_number]
            mont_day = bd_date[:len('DD')]
            datetime(2000,month_number,int(mont_day))
            user = original_message.mentions[0] if original_message.mentions else message_author
            users[str(user.id)]['bd'] = month_name + " " + mont_day
            await original_message.add_reaction('🎂')
            await original_message.add_reaction('✨')
            await LevelSystem.write_users_data(users)
            await LevelSystem.check_xp(None, user, channel)
        except :
            await EmbedMessages.send_embed_msg(channel, None, "Ocurrió un error, quizas NO usaste una fecha válida o el formato adecuado u.u")

    # ELIMINAR UN CUMPLEAÑOS
    if text.startswith('.deletecum'):
        users = await LevelSystem.read_users_data()
        user = original_message.mentions[0] if original_message.mentions else message_author
        del users[str(user.id)]['bd']
        await original_message.add_reaction('☑️')
        await LevelSystem.write_users_data(users)

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
