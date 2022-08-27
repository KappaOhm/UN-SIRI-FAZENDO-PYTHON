import asyncio
import calendar
import json
import uuid
from datetime import date, datetime
from io import BytesIO
from random import randint

import discord
import requests
from BotTokens import TENOR_TOKEN
from EmbedMessages import EmbedMessages
from EnvironmentVariables import COINS_PER_LVL, DUNGEON_TEXT_CHANNEL_ID, LVLUP_MESSASGES, SAFADOS_ROLE_ID, SERVER_ID, \
    SHITPOST_TEXT_CHANNEL_ID, SIRI_CHAT_TEXT_CHANNEL_ID, SIRI_FAZENDO_PLATA_EMOJI, TITLES_PER_LVL, cum_images, \
    cum_messsages, not_allowed_channel_ids, sassy_messages
from PIL import Image, ImageDraw, ImageFont

# INICIARLIZAR VARIABLES
pending_pick = False
coin_amount = 0
image_rng_text = ''
pick_message_object = None

class LevelSystem:

    # ATRIBUTOS DE CLASE
    chance = 5
 
    async def process_commands(channel,text,original_message,client):
        message_author = original_message.author

        # SISTEMA DE XP POR MENSAJES
        # SOLO MENSAJES DE MÁS DE 10 CARACTERES CUENTAN PARA XP
        if channel.id != DUNGEON_TEXT_CHANNEL_ID and (len(text) > 10 or len(original_message.attachments) > 0):

            users = await LevelSystem.read_users_data()

            # MENSAJES CON INSERCIONES DE IMAGENES DAN EL TRIPLE DE XP
            xp_points = 15 if (len(original_message.attachments) > 0 and channel.id !=SHITPOST_TEXT_CHANNEL_ID) else 5

            # PLANTAR MONEDAS CON CIERTA PROPABILIDAD CADA VEZ QUE SE ENVIA UN MENSAJE
            await LevelSystem.plant_coins(channel,None,False)
                
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

    #REVISAR CUMPLEAÑOS    
    async def check_birthday(channel,client):
        users = await LevelSystem.read_users_data()
        for user in users:
            today = str(date.today())
            today_no_year = today[len('YYYY-'):]
            month_name = calendar.month_name[int(today_no_year[:len(today_no_year)-len('-DD')])]
            mont_day = today_no_year[len('MM-'):]
            if 'bd' in users[user] and users[user]['bd'] == month_name + " " + mont_day:
                random_index1 = randint(0, len(cum_messsages) - 1)
                random_index2 = randint(0, len(cum_images) - 1)

                mentione_message = await channel.send(client.get_user(int(user)).mention)
                await EmbedMessages.send_embed_msg(channel,None,cum_messsages[random_index1] + client.get_user(int(user)).mention )
                await channel.send(cum_images[random_index2])
                await mentione_message.delete()

    # LEER ARCHIVO JSON
    async def read_users_data():
        with open('users.json', 'r') as f:
            users = json.load(f)
        return users

    # ESCRIBIR EN ARCHIVO JSON
    async def write_users_data(users):
        with open('users.json', 'w') as f:
            json.dump(users, f)

    # PLANTAR MONEDAS
    async def plant_coins(channel,password,is_plant):
        global pending_pick
        global image_rng_text
        global pick_message_object
        global coin_amount
        
        if is_plant or (channel.id not in not_allowed_channel_ids and pending_pick==False and ((randint(1, 100) + LevelSystem.chance) > 100)):

            search_term = 'cangrejo'
            response = requests.get("https://g.tenor.com/v1/search?q={}&key={}&limit=150".format(search_term, TENOR_TOKEN))
            data = response.json()
            random_index = randint(0, len(data['results']) - 1)
            gif_png_url = data['results'][random_index]['media'][0]['gif']['preview']
            image_size = data['results'][random_index]['media'][0]['gif']['dims']

            image_to_pick = Image.open(BytesIO(requests.get(gif_png_url).content))
                
            image_rng_text=str(uuid.uuid4())[9:13] if password is None else password
            font_size = int(0.1*image_size[0]) if image_size[0] > image_size[1] else int(0.1*image_size[1])
            text_font = ImageFont.truetype("impact.ttf", font_size)
            drawOnImage = ImageDraw.Draw(image_to_pick)
            drawOnImage.text(xy=(image_size[0]/2,5), text=image_rng_text, fill=(255,255,255), stroke_fill=(0,0,0), stroke_width=int(font_size/10),font=text_font)
            image_to_pick.save("lastpick.png")

            coin_amount = 1 if randint(1, 100) < 80 else 2
            if coin_amount == 1:
                message_text = "Ha aparecido "+ str(coin_amount) +' ' + SIRI_FAZENDO_PLATA_EMOJI + " siri coin, escribe .pick + código para atraparla"
            else:
                message_text ="Han aparecido "+ str(coin_amount) +' ' + SIRI_FAZENDO_PLATA_EMOJI + " siri coins, escribe .pick + código para atraparlas"
            pick_message_object = await channel.send(message_text,file=discord.File('lastpick.png'))

            pending_pick = True

    # RECOGER MONEDAS
    async def pick_coins(channel,original_message,text):
        global pending_pick
        global image_rng_text
        global pick_message_object
        global coin_amount
        
        if pick_message_object is not None and channel.id == pick_message_object.channel.id and pending_pick==True:
            
                message_author = original_message.author
                
                if  text.startswith(".pick") and (randint(1, 100) > 85 ):
                    random_index = randint(0, len(sassy_messages) - 1)
                    await original_message.reply(sassy_messages[random_index])
                    
                elif text == (".pick " + image_rng_text):
                    pending_pick = False
                    await pick_message_object.delete()
                    
                    users = await LevelSystem.read_users_data()
                    user = message_author
                    users[str(user.id)]['coins'] += coin_amount
                    await LevelSystem.write_users_data(users)
                    
                    msg = await EmbedMessages.send_embed_msg(channel,None,message_author.mention + ' atrapó las siri coins' +SIRI_FAZENDO_PLATA_EMOJI)
                    await asyncio.sleep(8)
                    await original_message.delete()
                    await msg.delete()
                    
    # APOSTAR MONEDAS CON NUMERO PAR/IMPAR
    async def bet_par_impar(message, identifier):
        users = await LevelSystem.read_users_data()
        user = str(message.author.id)
        number_of_coins = int(message.content.replace(
            '.par ', '')) if identifier == 0 else int(message.content.replace('.impar ', ''))
        user_coins = users[user]['coins']

        if user_coins < 1 or number_of_coins > user_coins:
            await EmbedMessages.send_embed_msg(message.channel, None, "No tienes suficientes " + SIRI_FAZENDO_PLATA_EMOJI + " monedas!")
            return

        users[user]['coins'] -= number_of_coins
        random_number = randint(1, 100)
        condition = random_number % 2 == 0 if identifier == 0 else random_number % 2 != 0
        def_title = "Número aleatorio : " + str(random_number)

        if condition:
            # ganó
            users[user]['coins'] += number_of_coins*2
            def_description = "¡Ganaste " + \
                str(number_of_coins*2) + SIRI_FAZENDO_PLATA_EMOJI + " monedas!"
            image_url = 'https://cdn.discordapp.com/emojis/882779204431773757.png'
        else:
            # no ganó xd
            def_description = "¡Felicidades! Perdiste tus monedas y te puedes comer esta monda : "
            image_url = 'https://cdn.discordapp.com/emojis/874053563146440754.png?size=96'

        await LevelSystem.write_users_data(users)

        embedVar = discord.Embed(title=def_title,
                                description=def_description,
                                color=0xFFA500)
        embedVar.set_image(url=image_url)
        await message.channel.send(embed=embedVar)

    
    # SISTEMA DE XP
    async def update_data(users, user):
        if not user in users:
            users[user] = {}
            users[user]['experience'] = 0
            users[user]['level'] = 1
            users[user]['coins'] = 0
            
    async def add_experience(users, user, xp):
        users[user]['experience'] += xp

    async def level_up(users, user, channel,client):
        xp = users[str(user.id)]['experience']
        # 50 ES LO MINIMO PARA NIVEL 2, NO REVISAR ANTES DE ESO
        if xp > 50:
            level_start = users[str(user.id)]['level']
            level_end = int((0.06)*xp**(0.55) + 1.5)

            if level_start < level_end:
                users[str(user.id)]['level'] = level_end
                # A NIVEL 5 DAR SAFADOS
                if level_end == 5:
                    role = client.get_guild(
                        SERVER_ID).get_role(SAFADOS_ROLE_ID)
                    await user.add_roles(role)
                    await channel.send("{} `ha obtenido el rol : {} `".format(user.mention, role.name))

                # PREMIAR CON MONEDAS POR EL NIVEL ESPECIFICO
                users[str(user.id)]['coins'] += COINS_PER_LVL[level_end]

                random_index = randint(0, len(LVLUP_MESSASGES) - 1)
                await channel.send("{} `ha subido al nivel {} - Recibes {}`".format(user.mention, level_end, COINS_PER_LVL[level_end]) + SIRI_FAZENDO_PLATA_EMOJI + "` monedas " + LVLUP_MESSASGES[random_index])
                await LevelSystem.write_users_data(users)
                await LevelSystem.check_xp(None, user, channel)


    async def check_xp(message, user, channel):
        users = await LevelSystem.read_users_data()
        user = message.mentions[0] if message is not None else user
        channel = message.channel if message is not None else channel

        if str(user.id) in users:
            user_xp = users[str(user.id)]['experience']
            user_lvl = users[str(user.id)]['level']
            next_lvl_xp = 47.2298*(2*(user_lvl+1)- 3)**(20/11)
            current_lvl_base_xp = 47.2298*(2*(user_lvl)- 3)**(20/11) if user_lvl>1 else 0

            title_in_level = TITLES_PER_LVL[user_lvl]

            old_min = int(current_lvl_base_xp)
            old_max =  int(next_lvl_xp)
            progress_current_lvl = int(((user_xp - old_min) * (10 - 1)) / (old_max - old_min)) + 1

            embedVar = discord.Embed(
                title=user.display_name, description='', color=0xFFA500)
            embedVar.set_thumbnail(url=user.avatar_url)
            embedVar.add_field(name=title_in_level, value = "XP : " + str(user_xp), inline=True)
            embedVar.add_field(name="Monedas :", value = str(users[str(user.id)]['coins']) + SIRI_FAZENDO_PLATA_EMOJI, inline=True)
            if 'bd' in users[str(user.id)]:
                embedVar.add_field(name="Cumpleaños 🎂", value = str(users[str(user.id)]['bd']), inline=False)
            embedVar.add_field(name="LVL " + str(user_lvl) + " ------------------> " + " LVL " + str(user_lvl+1),
                            value = progress_current_lvl * ":orange_heart:" + (10-progress_current_lvl) * ":white_heart:", inline=False)
            await channel.send(embed=embedVar)
            await LevelSystem.write_users_data(users)
        else:
            await EmbedMessages.send_embed_msg(channel, None, "Este usuario aún no acumula XP 🎲")


    def get_leader_value(leader):
        return leader.get("leader_value")

    # LEADERBOARD
    async def get_xp_leaderboard(channel,client):
        users = await LevelSystem.read_users_data()
        if users:
            leaders = []
            for user in users:
                leader_value = {}
                leader_value["user_id"] = int(user)
                leader_value["leader_value"] = users[user]['experience']
                leaders.append(leader_value)

            leaders.sort(key=LevelSystem.get_leader_value, reverse=True)

            embedVar = discord.Embed(title="Tabla de puntuaciones",
                                    description='Aqui estão as pessoas que mais fazem barra', color=0xFFA500)

            leader_emojis = ['👑', '👽', '🧙']
            x = 1
            for leader in leaders:
                emoji = leader_emojis[x-1] if x < 4 else '⚡'
                current_user = client.get_user(leader['user_id'])
                name = emoji + " " + current_user.name + " - LVL " + \
                    str(users[str(leader['user_id'])]['level'])
                value = "# " + str(x) + " - XP : " + str(leader['leader_value']) + " - Monedas : " + str(
                    users[str(leader['user_id'])]['coins']) + SIRI_FAZENDO_PLATA_EMOJI
                embedVar.add_field(name=name, value=value, inline=False)
                if x == 1:
                    embedVar.set_thumbnail(url=current_user.avatar_url)
                x += 1
                # CALCULAR SOLO LOS 10 PRIMEROS
                if x == 11:
                    break

            await channel.send(embed=embedVar)
