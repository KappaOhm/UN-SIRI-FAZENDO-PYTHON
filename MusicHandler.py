import asyncio
from random import shuffle

import discord
from EmbedMessages import EmbedMessages
from EnvironmentVariables import BOT_ID, FFMPEG_OPTIONS, SECONDS_TO_DISCONNECT, SIRI_CHAT_TEXT_CHANNEL_ID, YDL_OPTIONS
from youtube_dl import YoutubeDL

voice_client_playing = None
adding_song = False
is_playlist = False
songs_titles = []
URL_queue = []
song_playing = ""

class MusicHandler:

    # DESCONECTAR EL BOT SI DADOS X SEGUNDOS NO HA REPRODUCIDO AUDIO
    async def auto_disconnect(channel):
        global voice_client_playing
        global songs_titles
        global URL_queue
        global adding_song
        await asyncio.sleep(SECONDS_TO_DISCONNECT)
        if voice_client_playing is not None and not voice_client_playing.is_playing():
            voice_client_playing.stop()
            await voice_client_playing.disconnect() 
            voice_client_playing = None
            adding_song = False
            songs_titles = []
            URL_queue = []
            await EmbedMessages.send_embed_msg(channel, None, "Me voy por inactividad ⏱️")
            
    # MANEJO DE COLA PARA CANCIONES
    def add_to_queue(adding_song, URL):
        global URL_queue
        if adding_song:
            URL_queue.append(URL)

    # ESTA FUNCION SE LLAMA AUTOMATICAMENTE CUANDO UNA CANCION TERMINA ( atributo after del metodo .play() ) O CON EL COMANDO ".next"
    # SE ENCARGA DE VERIFICAR SI HAY CANCIONES EN COLA PARA DAR LA ORDEN DE REPRODUCIRLAS O DE LO CONTRARIO VERIFICAR SI DEBE DESCONECTAR EL BOT POR INACTIVIDAD
    def check_queue(channel,client):
        global URL_queue
        global adding_song
        global songs_titles

        if len(URL_queue) > 0:
            asyncio.run_coroutine_threadsafe(
                MusicHandler.play_song(channel, URL_queue.pop(0),client), client.loop)
        else:
            asyncio.run_coroutine_threadsafe(
                MusicHandler.auto_disconnect(channel), client.loop)

    # REPRODUCIR CANCIONES EN COLA
    async def play_song(channel, URL, client):
        global is_playlist
        global songs_titles
        global song_playing

        current_song_title = songs_titles[0]
        await EmbedMessages.play_embed_msg(channel, "🤟 Reproduciendo", current_song_title)
        songs_titles.pop(0)

        song_playing = current_song_title

        source = await discord.FFmpegOpusAudio.from_probe(URL, **FFMPEG_OPTIONS)
        voice_client_playing.play(source, after=lambda e: MusicHandler.check_queue(channel,client))

    # OBTENER UNA URL DE YOUTUBE SIN IMPORTAR QUE METODO DE BUSCA SE USE (URL DIRECTA, TERMINO DE BUSQUEDA, PLAYLIST)
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

    # MANEJAR LA REPRODUCCION DE MÚSICA CON REACCIONES
    async def control_music_with_reactions(payload,client):
        global voice_client_playing

        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if payload.emoji.name == '⏭️' and not payload.member.bot and songs_titles:
            voice_client_playing.pause()
            await EmbedMessages.send_embed_msg(channel, "Siguiente canción 🦀", None)
            await message.clear_reactions()
            MusicHandler.check_queue(channel,client)

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

    def detect_music_reaction(payload):
        return not payload.user_id == BOT_ID and payload.emoji.name != '⏭️' and payload.emoji.name !='⏸️' and payload.emoji.name !='▶️'
    

    # LEER MENSAJES DE TEXTO PARA VERIFICAR COMANDOS DE MUSICA
    async def process_commands(channel,text,original_message,client):
        global voice_client_playing
        global adding_song
        global is_playlist
        global songs_titles
        global URL_queue
        
        message_author = original_message.author
        
        # COMANDO PLAY
        if (text.startswith('.play') or text.startswith('.p ')) and channel.id == SIRI_CHAT_TEXT_CHANNEL_ID:

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
                MusicHandler.check_queue(channel,client)
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
            if voice_client_playing is not None:
                voice_client_playing.stop()
                await voice_client_playing.disconnect()
                await EmbedMessages.send_embed_msg(channel, None,"Ah pero ya me echaron, todo bien🦀🔪")
