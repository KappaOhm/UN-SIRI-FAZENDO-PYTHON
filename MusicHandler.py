import asyncio

import discord
from EmbedMessages import EmbedMessages
from EnvironmentVariables import FFMPEG_OPTIONS, SECONDS_TO_DISCONNECT, YDL_OPTIONS
from SiriMain import URL_queue, adding_song, song_playing, songs_titles, voice_client_playing
from youtube_dl import YoutubeDL


class MusicHandler:

    # DESCONECTAR EL BOT SI DADOS X SEGUNDOS NO HA REPRODUCIDO AUDIO
    async def auto_disconnect(channel):
        global voice_client_playing
        await asyncio.sleep(SECONDS_TO_DISCONNECT)
        if voice_client_playing is not None and not voice_client_playing.is_playing():
            await EmbedMessages.send_embed_msg(channel, None, "Me voy por inactividad ⏱️")
            await voice_client_playing.disconnect() 

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
                MusicHandler.play_song(channel, URL_queue.pop(0)), client.loop)
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
            MusicHandler.check_queue(channel)

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
