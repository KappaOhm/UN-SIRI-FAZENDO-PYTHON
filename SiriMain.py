# IMPORTS
import asyncio
import calendar
import os
from datetime import date, datetime
from random import randint, shuffle

import discord
from BotTokens import BOT_TOKEN
from discord import Intents
from discord.ext import tasks
from discord_components import Button, DiscordComponents
from EmbedMessages import *
from EnvironmentVariables import *
from HandleRoles import *
from LevelAndCoinsSystem import *
from ReplyMessages import *
from youtube_dl import YoutubeDL

# INICIALIZAR CLIENTE DE DISCORD
intents = Intents.all()
client = discord.Client(intents=intents)
DiscordComponents(client)

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
            await EmbedMessages.send_embed_msg(channel,None,cum_messsages[random_index1] +client.get_user(int(user)).mention )
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
    print("Waiting {} hours to send daily message".format(hours_left))
    print('---------------------------')
    await asyncio.sleep(hours_left*60*60)
    print("Finished waiting")

# DESCONECTAR EL BOT SI DADOS X SEGUNDOS NO HA REPRODUCIDO NADA
async def auto_disconnect(channel):
    await asyncio.sleep(SECONDS_TO_DISCONNECT)
    if voice_client_playing is not None and not voice_client_playing.is_playing():
        await EmbedMessages.send_embed_msg(channel, None, "Me voy por inactividad ⏱️")
        await voice_client_playing.disconnect() 

# ESTA FUNCION SE LLAMA AUTOMATICAMENTE CUANDO UNA CANCION TERMINA (after del .play) O CON EL COMANDO ".next"
# SE ENCARGA DE VERIFICAR SI HAY CANCIONES EN COLA PARA DAR LA ORDEN DE REPRODUCIRLAS O DE LO CONTRARIO VERIFICAR SI DEBE DESCONECTAR EL BOT
def check_queue(channel):
    global URL_queue
    global adding_song
    global songs_titles

    if len(URL_queue) > 0:
        asyncio.run_coroutine_threadsafe(
            play_song(channel, URL_queue.pop(0)), client.loop)
    else:
        asyncio.run_coroutine_threadsafe(
            auto_disconnect(channel), client.loop)

# MANEJO DE COLA PARA CANCIONES
def add_to_queue(adding_song, URL):
    global URL_queue
    if adding_song:
        URL_queue.append(URL)        

# REPRODUCIR CANCIONES EN COLA
async def play_song(channel, URL):
    global is_playlist
    global songs_titles
    global song_playing

    current_song_title = songs_titles[0]
    await EmbedMessages.play_embed_msg(channel, "🤟 Reproduciendo", current_song_title)
    songs_titles.pop(0)

    song_playing = current_song_title

    source = await discord.FFmpegOpusAudio.from_probe(URL, **FFMPEG_OPTIONS)
    voice_client_playing.play(source, after=lambda e: check_queue(channel))

# IMPRIMIR CANCIONES EN COLA
async def show_queue(channel):
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
        await EmbedMessages.send_embed_msg(channel, "Canciones en cola", queue)
    else:
        await EmbedMessages.send_embed_msg(channel, None, "Aqui no hay nada mi ciela🦀")

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
    global adding_song
    global songs_titles
    global URL_queue
    global is_playlist
    global pending_pick
    global image_rng_text
    global pick_message_object
    global coin_amount
    global chance

    # IGNORAR MENSAJES DE BOTS, TANTO SIRI COMO OTROS
    if message.author == client.user or message.author.bot:
        return

    # ELSE, EL MENSAJE NO VIENE DE NINGUN BOT
    text = message.content
    channel = message.channel
   
    await ReplyMessages.process_messages(channel,text,message)

    # CAMBIAR LA PROBABILIDAD DE QUE SIRI PLANTE COINS
    if text.startswith('.setchance') and message.author.id == OWNER_ID:
        chance = int(text[len('.setchance')+1:])
        await message.add_reaction('✨')  
        
    # SISTEMA DE XP POR MENSAJES
    # SOLO MENSAJES DE MÁS DE 10 CARACTERES CUENTAN PARA XP
    if channel.id != DUNGEON_TEXT_CHANNEL_ID and (len(text) > 10 or len(message.attachments) > 0):

        users = await LevelSystem.read_users_data()

        # MENSAJES CON INSERCIONES DE IMAGENES DAN EL TRIPLE DE XP
        xp_points = 15 if (len(message.attachments) > 0 and channel.id !=SHITPOST_TEXT_CHANNEL_ID) else 5

        # PLANTAR SIRI COINS
        if channel.id not in not_allowed_channel_ids and pending_pick==False:
            if (randint(1, 100) + chance) > 100:
                pending_pick,image_rng_text,pick_message_object,coin_amount = await LevelSystem.plant_coins(channel,None)
            
        await LevelSystem.update_data(users, str(message.author.id))
        await LevelSystem.add_experience(users, str(message.author.id), xp_points)
        await LevelSystem.level_up(users, message.author, channel,client)

        await LevelSystem.write_users_data(users)
        
    # INTENTAR HACER UN PICK DE SIRI COINS
    if pick_message_object is not None:
        if channel.id not in not_allowed_channel_ids and channel.id == pick_message_object.channel.id and pending_pick==True and text.startswith('.pick'):
            if text == (".pick " + image_rng_text):
                pending_pick = False
                await pick_message_object.delete()
                
                users = await LevelSystem.read_users_data()
                user = message.author
                users[str(user.id)]['coins'] += coin_amount
                await LevelSystem.write_users_data(users)
                
                msg = await EmbedMessages.send_embed_msg(channel,None,message.author.mention + ' atrapó las siri coins' +SIRI_FAZENDO_PLATA_EMOJI)
                await asyncio.sleep(8)
                await message.delete()
                await msg.delete()

    # DAR MONEDAS
    if text.startswith('.award') and message.author.id == OWNER_ID:
        users = await LevelSystem.read_users_data()
        number_of_coins = int(text[len('.award')+1:])
        user = message.mentions[0] 
        users[str(user.id)]['coins'] += number_of_coins
        await channel.send(user.mention)
        await EmbedMessages.send_embed_msg(channel, None, "¡Te han otorgado " + str(number_of_coins) + "" + SIRI_FAZENDO_PLATA_EMOJI + " monedas!")
        await LevelSystem.write_users_data(users)

    # PLANTAR MONEDAS
    if text.startswith('.plant') and channel.id not in not_allowed_channel_ids and message.author.id == OWNER_ID and pending_pick==False:
        password = text[len('.plant')+1:]
        await message.delete()
        pending_pick,image_rng_text,pick_message_object,coin_amount = await LevelSystem.plant_coins(channel,password)
        
    # COMANDO PARA REVISAR EXPERIENCIA PROPIA O DE OTRO USUARIO
    if text.startswith('.xp'):
        if text == '.xp':
            await LevelSystem.check_xp(None, message.author, channel)
        else:
            await LevelSystem.check_xp(message, None, None)

    # COMANDO LEADERBOARD
    if text == '.lb':
        await LevelSystem.get_xp_leaderboard(channel,client)

    # COMANDO APOSTAR POR PAR
    if text.startswith('.par') and channel.id == SIRI_CHAT_TEXT_CHANNEL_ID:
        await LevelSystem.bet_par_impar(message, 0)

    # COMANDO APOSTAR POR IMPAR
    if text.startswith('.impar') and channel.id == SIRI_CHAT_TEXT_CHANNEL_ID:
        await LevelSystem.bet_par_impar(message, 1)
          
    # SETEAR UN CUMPLEAÑOS (bd)    
    if text.startswith('.setcum'):
        
        try:
            users = await LevelSystem.read_users_data()
            bd_date = text[len(text)-len('MM-DD'):]
            month_name = calendar.month_name[int(bd_date[:len(bd_date)-len('-DD')])]
            mont_day = bd_date[len('MM-'):]
            user = message.mentions[0] if message.mentions else message.author
            users[str(user.id)]['bd'] = month_name + " " + mont_day
            await message.add_reaction('🎂')
            await message.add_reaction('✨')
            await LevelSystem.write_users_data(users)
            await LevelSystem.check_xp(None, user, channel)
        except :
            await EmbedMessages.send_embed_msg(channel, None, "Ocurrio un error, quizas no usaste el formato adecuado u.u")

    # SETEAR UN CUMPLEAÑOS (bd)    
    if text.startswith('.deletecum'):
        
        users = await LevelSystem.read_users_data()
        user = message.mentions[0] if message.mentions else message.author
        del users[str(user.id)]['bd']
        await message.add_reaction('☑️')
        await LevelSystem.write_users_data(users)
        
    if text.startswith('.testbutton'):
        button1 = Button(label="Sí ", style=3, emoji='🤠',custom_id="yes")
        button2 = Button(label="No ", style=4, emoji='😔',custom_id="no")
        await channel.send('¿Deberiamos banear a Ski?', components=[[button1,button2]])
        
    # COMANDO PLAY
    if text.startswith('.play') or (text.startswith('.p') and ".par" not in text and ".plant" not in text and ".pick" not in text) and (channel.id == SIRI_CHAT_TEXT_CHANNEL_ID):

        if message.author.voice is None:
            await EmbedMessages.send_embed_msg(channel, None, "No estas en un canal de voz 🦀")
        else:
            if voice_client_playing is not None and voice_client_playing.is_playing() and voice_client_playing.channel.id != message.author.voice.channel.id:
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
                    URL = get_YT_info(url_song)

                    if is_playlist and voice_client_playing is None and len(URL_queue) > 0:
                        voice_client_playing = await message.author.voice.channel.connect()
                        adding_song = True
                        await play_song(channel, URL_queue.pop(0))

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
                                    await EmbedMessages.send_embed_msg(channel, None, "Playlist agregada 🎶")
                                else:
                                    await EmbedMessages.send_embed_msg(channel, "Cancion agregada 🦀", songs_titles[-1])

                        if len(URL_queue) > 0 and voice_client_playing.is_playing() == False:
                            await play_song(channel, URL_queue.pop(0))
                except Exception as error:

                    if error.__context__ is not None and error.__context__.args is not None:
                        mensaje = error.__context__.args[0]
                    else:
                        mensaje = "Lo siento, ocurrió un error u.u"
                    print(error)
                    await EmbedMessages.send_embed_msg(channel, "Error", mensaje)

    # COMANDO NEXT
    if text == '.next' or text == '.n' and (channel.id == SIRI_CHAT_TEXT_CHANNEL_ID):
        if voice_client_playing is not None and len(URL_queue) > 0:
            voice_client_playing.pause()
            await EmbedMessages.send_embed_msg(channel, "Siguiente canción 🦀", None)
            check_queue(channel)
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

            await show_queue(channel)

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
        await show_queue(channel)

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

# CONECTAR BOT AL VOICE CHAT DE AFKs Y LIMPIAR VARIABLES CUANDO SE DESCONECTA DE CUALQUIER CANAL DE VOZ
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


# MANEJAR LA REPRODUCCION DE MÚSICA CON REACCIONES
async def control_music_with_reactions(payload):
    global voice_client_playing

    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if payload.emoji.name == '⏭️' and not payload.member.bot and songs_titles:
        voice_client_playing.pause()
        await EmbedMessages.send_embed_msg(channel, "Siguiente canción 🦀", None)
        await message.clear_reactions()
        check_queue(channel)

    elif payload.emoji.name == '⏸️' and not payload.member.bot and voice_client_playing.is_playing():
        await message.clear_reactions()

        await message.add_reaction('▶️')
        await message.add_reaction('⏭️')

        voice_client_playing.pause()
    
    elif payload.emoji.name == '▶️' and not payload.member.bot:
        await message.clear_reactions()

        await message.add_reaction('⏸️')
        await message.add_reaction('⏭️')

        voice_client_playing.resume()


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
        await control_music_with_reactions(payload)

@client.event
async def on_raw_reaction_remove(payload):
    is_for_roles = not payload.user_id == BOT_ID and payload.emoji.name != '⏭️' and payload.emoji.name !='⏸️' and payload.emoji.name !='▶️'

    if is_for_roles:
        await HandleRoles.remove_or_add_role(client,payload,False)

# TEST DE BUTTON COMPONENTS
@client.event
async def on_button_click(interaction):
    if interaction.component.custom_id == "yes":
        await interaction.respond(content = "¡Tú sí sabes!",ephemeral =True)
    if interaction.component.custom_id == "no":
        await interaction.send(content = "Chale, aguafiestas...",ephemeral =True)
        
# CORRER BOT
called_once_a_day.start()
client.run(BOT_TOKEN)
