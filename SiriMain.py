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
    global voice_client_playing
    global adding_song
    global songs_titles
    global URL_queue
    global is_playlist

    text = original_message.content
    channel = original_message.channel
    message_author = original_message.author
    
    # IGNORAR MENSAJES DE BOTS, TANTO SIRI COMO OTROS BOTS
    if message_author == client.user or message_author.bot:
        return

    # ELSE, EL MENSAJE NO VIENE DE NINGUN BOT
    await ReplyMessages.process_messages(channel,text,original_message)
    await AdminCommands.process_commands(channel,text,original_message)
    
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
        
    # COMANDO PLAY
    if text.startswith('.play') or (text.startswith('.p') and ".par" not in text and ".plant" not in text and ".pick" not in text) and (channel.id == SIRI_CHAT_TEXT_CHANNEL_ID):

        if message_author.voice is None:
            await EmbedMessages.send_embed_msg(channel, None, "No estas en un canal de voz 🦀")
        else:
            if voice_client_playing is not None and voice_client_playing.is_playing() and voice_client_playing.channel.id != message_author.voice.channel.id:
                await EmbedMessages.send_embed_msg(channel, None, "Ya estoy ocupado en otro canal de voz🦀")
            else:
                if text.startswith('.play'):
                    url_song = text.replace('.play ', '')
                elif text.startswith('.p'):
                    url_song = text.replace('.p ', '')
                try:
                    is_playlist = False
                    if 'list' in url_song:
                        await EmbedMessages.send_embed_msg(channel, None, "🎶 Descargando playlist...")
                    URL = MusicHandler.get_YT_info(url_song)

                    if is_playlist and voice_client_playing is None and len(URL_queue) > 0:
                        voice_client_playing = await message_author.voice.channel.connect()
                        adding_song = True
                        await MusicHandler.play_song(channel, URL_queue.pop(0),client)

                    else:
                        if voice_client_playing is None and adding_song == False:
                            voice_client_playing = await message_author.voice.channel.connect()
                            adding_song = True
                            MusicHandler.add_to_queue(adding_song, URL)
                        else:
                            MusicHandler.add_to_queue(adding_song, URL)
                            if len(URL_queue) > 0:
                                await original_message.add_reaction('🌟')
                                if is_playlist:
                                    await EmbedMessages.send_embed_msg(channel, None, "Playlist agregada 🎶")
                                else:
                                    await EmbedMessages.send_embed_msg(channel, "Cancion agregada 🦀", songs_titles[-1])

                        if len(URL_queue) > 0 and voice_client_playing.is_playing() == False:
                            await MusicHandler.play_song(channel, URL_queue.pop(0),client)
                except Exception as error:

                    if error.__context__ is not None and error.__context__.args is not None:
                        mensaje = error.__context__.args[0]
                    else:
                        mensaje = "Lo siento, ocurrió un error y es culpa de YouTube u.u"
                    print(error)
                    await EmbedMessages.send_embed_msg(channel, "Error", mensaje)

    # COMANDO NEXT
    if text == '.next' or text == '.n' and (channel.id == SIRI_CHAT_TEXT_CHANNEL_ID):
        if voice_client_playing is not None and len(URL_queue) > 0:
            voice_client_playing.pause()
            await EmbedMessages.send_embed_msg(channel, "Siguiente canción 🦀", None)
            MusicHandler.check_queue(channel)
        else:
            adding_song = False
            await EmbedMessages.send_embed_msg(channel, None, "Aqui no hay nada mi ciela 🦀")

     # COMANDO SHUFFLE
    if text == '.shuffle' or text == '.s' and (channel.id == SIRI_CHAT_TEXT_CHANNEL_ID):
        if voice_client_playing is not None and len(URL_queue) > 0:
            await EmbedMessages.send_embed_msg(channel, None, " 🧙🌟 ==> 🎲🎵")

            songs_titles_shuffled = []
            URL_queue_shuffled = []
            index_shuf = list(range(len(songs_titles)))
            shuffle(index_shuf)
            for i in index_shuf:
                songs_titles_shuffled.append(songs_titles[i])
                URL_queue_shuffled.append(URL_queue[i])

            songs_titles = songs_titles_shuffled
            URL_queue = URL_queue_shuffled
            await MusicHandler.show_queue(channel)

        else:
            adding_song = False
            await EmbedMessages.send_embed_msg(channel, None, "Aqui no hay nada mi ciela 🦀")        

    # COMANDO STOP
    if text == '.stop' and (channel.id == SIRI_CHAT_TEXT_CHANNEL_ID):
        if voice_client_playing is not None and voice_client_playing.is_playing() == True:
            voice_client_playing.stop()
            URL_queue = []
            songs_titles = []
            await EmbedMessages.send_embed_msg(channel, None, "Reproduccion de música detenida 🦀")

    # COMANDO CLEAR
    if text == '.clear' and channel.id == SIRI_CHAT_TEXT_CHANNEL_ID:
        if URL_queue:
            URL_queue = []
            songs_titles = []
            await EmbedMessages.send_embed_msg(channel, None, "Cola de reproduccion borrada🎵🤠")
        else:
            await EmbedMessages.send_embed_msg(channel, None, "Aqui no hay nada mi ciela 🦀")

    # COMANDO QUEUE
    if text == '.q' and (channel.id == SIRI_CHAT_TEXT_CHANNEL_ID):
        await MusicHandler.show_queue(channel)

    # COMANDO LEAVE
    if text == '.leave' and (channel.id == SIRI_CHAT_TEXT_CHANNEL_ID):
        is_disconnected = False
        if voice_client_playing is not None:
            songs_titles = []
            URL_queue = []
            voice_client_playing.stop()
            await voice_client_playing.disconnect()
            voice_client_playing = None
            adding_song = False
            is_disconnected = True
        if is_disconnected:
            await EmbedMessages.send_embed_msg(channel, None,"Ah pero ya me echaron, todo bien🦀🔪")

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
