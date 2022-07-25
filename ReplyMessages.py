
from random import randint

import discord
import requests
from BotTokens import TENOR_TOKEN
from EmbedMessages import EmbedMessages
from EnvironmentVariables import OWNER_ID, RED_ROOM_TEXT_CHANNEL_ID, contexto, redroom_responses, trece


class ReplyMessages:

    async def process_messages(channel,text,original_message):

        channel = original_message.channel
        
        if text.startswith('.gif'):
            search_term = text[5:]
            response = requests.get("https://g.tenor.com/v1/search?q={}&key={}&limit=15".format(search_term, TENOR_TOKEN))
            data = response.json()
            random_index = randint(0, len(data['results']) - 1)
            gif_url = data['results'][random_index]['media'][0]['gif']['url']
 
            # ESTO ES PARA CREAR UN GIF DE LA NADA, COMO EN EL MENSAJE DIARIO
            if original_message is None:
                await channel.send(gif_url)

            # HACER UNA RESPUESTA
            elif original_message.reference is not None:
                embedVar = discord.Embed(title='',description=original_message.author.mention,color=0xFFA500)
                embedVar.set_image(url=gif_url)      
                referenced_message = await channel.fetch_message(original_message.reference.message_id)
                await referenced_message.reply(embed=embedVar)
                await original_message.delete()
            # ENVIAR UN GIF NORMAL
            else:
                embedVar = discord.Embed(title='',description=original_message.author.mention,color=0xFFA500)
                embedVar.set_image(url=gif_url)          
                await channel.send(embed=embedVar)
                await original_message.delete()
                       
        # COMANDO DE AYUDA
        if text == '.help' or text == '.h' :
            await EmbedMessages.send_embed_help_msg(original_message)

        # COMANDO DE COMANDOS XP Y MONEDAS
        if text == '.cmd':
            await EmbedMessages.send_embed_cmd_msg(original_message)

        if text.startswith('.kickmsg'):
            try:
                user = original_message.mentions[0]
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
                await original_message.add_reaction('✅')
            except:
                await original_message.author.send(
                    'ocurrio un errorsinho con el comando "' + text + '" - escribe bien esa monda🦀🔪')
                    
        # RESPONDER A IMAGENES EN RED ROOM
        if channel.id == RED_ROOM_TEXT_CHANNEL_ID and len(original_message.attachments) > 0:
                random_number = randint(0, 99)
                random_index = randint(0, len(redroom_responses) - 1)
                if random_number < 15:
                    message_to_reply = await channel.fetch_message(original_message.id)
                    await message_to_reply.reply(redroom_responses[random_index])

        if text.startswith('siri'):
            await channel.send('eu estou fazendo barra')
            await original_message.add_reaction('🦀')

        if text.startswith('hable paisa'):
            await channel.send('eso si jamaaaaaas')

        if text.endswith('verde'):
            await channel.send('agache y me lo muerde 🦀')

        if text.endswith('contexto'):
            random_index = randint(0, len(contexto) - 1)
            await channel.send(contexto[random_index])

        if text.endswith('complejo'):
            await channel.send('complejo como mi cangrejo 🥵')

        if text.endswith('trece') or text == '12 + 1' or text == '12+1':
            await original_message.add_reaction('🥵')
            random_index = randint(0, len(trece) - 1)
            await channel.send(trece[random_index])

        if text == 'ocho' or text == 'Ocho' or text == '8' or text == '7+1' or text == '7 + 1':
            await channel.send('por el culo te la enclocho 🤠')

        if text == 'cinco' or text == 'Cinco'  or text == '5' or text == '4+1' or text == '4 + 1':
            await channel.send('por el culo te la hinco 🤠')

        if text == 'mamelo' or text == 'mámelo' or text == 'a mamarlo' or text == 'me lo mama' or text == 'como lo mama':
            await original_message.add_reaction('🅰️')
            await original_message.add_reaction('🅱️')
            await original_message.add_reaction('🇪')
            await original_message.add_reaction('🇷')
            
        if text.startswith('.anuncio') and original_message.author.id == OWNER_ID:
            await original_message.delete()
            await EmbedMessages.send_embed_msg(channel,None,text[8:len(text)]) 
