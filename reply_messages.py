import discord
import requests

from random import randint

from embed_message import embed_message
from vars import id_kappa
from vars import red_room_channel_id
from vars import REDROOM_RESPONSES
from vars import CONTEXTO
from vars import TRECE
from bot_tokens import tenor_token

class reply_messages:

    async def reply_with_GIF(channel,text,original_message):

        if text.startswith('.gif'):
            search_term = text[5:]
            response = requests.get("https://g.tenor.com/v1/search?q={}&key={}&limit=100".format(search_term, tenor_token))
            data = response.json()
            random_index = randint(0, len(data['results']) - 1)
          
            if original_message is None:
                await channel.send(data['results'][random_index]['media'][0]['gif']['url'])

            elif original_message.reference is not None:
                referenced_message = await channel.fetch_message(original_message.reference.message_id)
                await referenced_message.reply(data['results'][random_index]['media'][0]['gif']['url'])
            else:
                await channel.send(data['results'][random_index]['media'][0]['gif']['url'])
            await original_message.delete()

    async def handle_messages(text,message):

        if text.startswith('.kickmsg'):
            try:
                user = message.mentions[0]
                embedVar = discord.Embed(title='ATENCION - ¡Has sido dad@ de alta!',
                                        description='Se ha detectado completa inactividad de tu parte en nuestro servidor y nuestro deseo es que los miembros de la comunidad tengan interes por hacer parte de la misma',
                                        color=0xFFA500)
                embedVar.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/875044852314816522/930228514601451591/axoHey.png')
                embedVar.set_image(
                    url='https://cdn.discordapp.com/attachments/875044852314816522/930231541550968922/Screenshot_3.png')
                embedVar.add_field(name='Eres bievenid@ de vuelta siempre que desees y puedes unirte siguiendo este enlace :',
                                value='https://discord.gg/DGUHvUyXNc', inline=False)
                await user.send(embed=embedVar)
                await message.add_reaction('✅')
            except:
                await message.author.send(
                    'ocurrio un errorsinho con el comando "' + text + '" - escribe bien esa monda🦀🔪')

        # RESPONDER A IMAGENES EN RED ROOM
        if message.channel.id == red_room_channel_id and len(message.attachments) > 0:
            random_number = randint(0, 99)
            random_index = randint(0, len(REDROOM_RESPONSES) - 1)
            if random_number < 25:
                message_to_reply = await message.channel.fetch_message(message.id)
                await message_to_reply.reply(REDROOM_RESPONSES[random_index])

        if text.startswith('siri'):
            await message.channel.send('eu estou fazendo barra')
            await message.add_reaction('🦀')

        if text.startswith('hable paisa'):
            await message.channel.send('eso si jamaaaaaas')

        if text.endswith('verde'):
            await message.channel.send('agache y me lo muerde 🦀')

        if text.endswith('contexto'):
            random_index = randint(0, len(CONTEXTO) - 1)
            await message.channel.send(CONTEXTO[random_index])

        if text.endswith('complejo'):
            await message.channel.send('complejo como mi cangrejo 🥵')

        if text.endswith('trece') or text == '12 + 1' or text == '12+1':
            await message.add_reaction('🥵')
            random_index = randint(0, len(TRECE) - 1)
            await message.channel.send(TRECE[random_index])

        if text == 'ocho' or text == 'Ocho' or text == '8' or text == '7+1' or text == '7 + 1':
            await message.channel.send('por el culo te la enclocho 🤠')

        if text == 'cinco' or text == 'Cinco'  or text == '5' or text == '4+1' or text == '4 + 1':
            await message.channel.send('por el culo te la hinco 🤠')

        if text == 'mamelo' or text == 'mámelo' or text == 'a mamarlo' or text == 'me lo mama' or text == 'como lo mama':
            await message.add_reaction('🅰️')
            await message.add_reaction('🅱️')
            await message.add_reaction('🇪')
            await message.add_reaction('🇷')
        
        if text.startswith('.anuncio') and message.author.id == id_kappa:
            await message.delete()
            await embed_message.send_embed_msg(message.channel,None,text[8:len(text)]) 