import json
from io import BytesIO
from random import randint

import discord
import requests
from BotTokens import TENOR_TOKEN
from EmbedMessages import EmbedMessages
from EnvironmentVariables import ALT_RED_ROOM_TEXT_CHANNEL_ID, OWNER_ID, RED_ROOM_TEXT_CHANNEL_ID, context, contexto, \
    redroom_responses
from PIL import Image, ImageDraw, ImageFont


class ReplyMessages:

    async def process_messages(channel,text,original_message):
        text = text.lower()

        if text.startswith('.anal'):
            await ReplyMessages.image_analysis(channel) 
        
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
            await EmbedMessages.help_embed_msg(original_message)

        # COMANDO DE COMANDOS XP Y MONEDAS
        if text == '.cmd':
            await EmbedMessages.cmd_embed_msg(original_message)
             
        # RESPONDER A IMÁGENES EN RED ROOM
        if (channel.id == RED_ROOM_TEXT_CHANNEL_ID or channel.id == ALT_RED_ROOM_TEXT_CHANNEL_ID) and len(original_message.attachments) > 0:
                random_number = randint(0, 99)
                random_index = randint(0, len(redroom_responses) - 1)
                if random_number < 15:
                    message_to_reply = await channel.fetch_message(original_message.id)
                    await message_to_reply.reply(redroom_responses[random_index])

        if text.startswith('siri'):
            await original_message.add_reaction('🦀')

        if text == 'siri':
            await channel.send('eu estou fazendo barra')
            await original_message.add_reaction('🦀')   

        if text.startswith('hable paisa'):
            await channel.send('eso si jamaaaaaas')

        if text.endswith('verde'):
            await channel.send('agache y me lo muerde 🦀')

        if text.endswith('contexto'):
            random_index = randint(0, len(contexto) - 1)
            await channel.send(contexto[random_index])

        if text.endswith('context'):
            random_index = randint(0, len(context) - 1)
            await channel.send(context[random_index])

        if text.endswith('complejo'):
            await channel.send('complejo como mi cangrejo 🥵')

        if text == 'ocho' or text == '8' or text == '7+1' or text == '7 + 1':
            await channel.send('por el culo te la enclocho 🤠')

        if text == 'cinco'  or text == '5' or text == '4+1' or text == '4 + 1':
            await channel.send('por el culo te la hinco 🤠')

        if text == 'mamelo' or text == 'mamalo' or text == 'a mamarlo' or text == 'me lo mama' or text == 'me lo tiene que mamar':
            await original_message.add_reaction('🅰️')
            await original_message.add_reaction('🅱️')
            await original_message.add_reaction('🇪')
            await original_message.add_reaction('🇷')

        # ENVIAR UN MENSAJE ANTES DE KICKEAR A ALGUIEN DEL SERVER
        if text.startswith('.kickmsg'):
            try:
                user = original_message.mentions[0]
                embedVar = discord.Embed(title='ATENCIÓN - ¡Has sido dad@ de alta!',
                                        description='Se ha detectado completa inactividad de tu parte en nuestro servidor y nuestro deseo es que los miembros de la comunidad tengan interés por hacer parte de la misma.',
                                        color=0xFFA500)
                embedVar.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/875044852314816522/930228514601451591/axoHey.png')
                embedVar.set_image(
                    url='https://cdn.discordapp.com/attachments/875044852314816522/930231541550968922/Screenshot_3.png')
                embedVar.add_field(name='Eres bievenid@ de vuelta siempre que desees y puedes unirte siguiendo este enlace :',
                                value='https://discord.gg/HaBQQKBQeB', inline=False)
                await user.send(embed=embedVar)
                await original_message.add_reaction('✅')
            except:
                await original_message.author.send(
                    'ocurrió un errorsinho con el comando "' + text + '" - escribe bien esa mondá🦀🔪')    

    async def image_analysis(channel):
        if channel.last_message.reference is not None:
            try:
                img_url = channel.last_message.reference.resolved.attachments[0].url
                api_url = "https://emotion-detection2.p.rapidapi.com/emotion-detection"
                payload = {"url": img_url}
                headers = {
                    "content-type": "application/json",
                    "X-RapidAPI-Key": "99e3481a54msh7e9ce20b8b543d6p17327ejsn788e1fa0653b",
                    "X-RapidAPI-Host": "emotion-detection2.p.rapidapi.com"
                }
                
                response = requests.request("POST", api_url, json=payload, headers=headers)
                json_response = json.loads(response.text)
                image = Image.open(BytesIO(requests.get(img_url).content))
                width, height = image.size
                # BORRAR MENSAJE QUE LLAMÓ AL COMANDO
                await channel.delete_messages([discord.Object(id=channel.last_message_id)])
                for object in json_response:
                    probability = object['emotion']['probability']*100
                    text_to_show = object['emotion']['value']+ "\n" + str("{:.2f}".format(probability))+"%"
                    
                    probability_int = int(probability)
                    if probability_int < 80 and probability_int > 55:
                        fill_color= 'gold'
                    elif probability_int > 80:
                        fill_color= 'limegreen'
                    else:
                        fill_color= 'crimson'

                    x1=int(object['rectangle']['left'])
                    x2=int(object['rectangle']['right'])
                    y1=int(object['rectangle']['top'])
                    y2=int(object['rectangle']['bottom'])
                    
                    drawOnImage=ImageDraw.Draw(image)
                    drawOnImage.rectangle([(x1,y1),(x2,y2)],outline=fill_color,fill=None,width=2)
                    font_size = int(width*0.05)
                    text_font = ImageFont.truetype("impact.ttf", font_size)
                    
                    x_text = x1 +(x2-x1)/4
                    y_text = y1 +(y2-y1)/2
                    drawOnImage.text(xy=(x_text,y_text), text=text_to_show, fill=fill_color, stroke_fill=(0,0,0), stroke_width=1,font=text_font)
                    
                image.save("lastanal.png")
                await channel.send(file=discord.File('lastanal.png'))
            except Exception as error:
                await EmbedMessages.send_embed_msg(channel,None,"⛔ No se pudo procesar la imagen, rostro no detectado ⛔")
                print(error)
