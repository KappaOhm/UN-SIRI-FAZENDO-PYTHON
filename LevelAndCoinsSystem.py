import json
import uuid
from io import BytesIO
from random import randint

import discord
import requests
from BotTokens import TENOR_TOKEN
from EmbedMessages import EmbedMessages
from EnvironmentVariables import COINS_PER_LVL, LVLUP_MESSASGES, SAFADOS_ROLE_ID, SERVER_ID, SIRI_FAZENDO_PLATA_EMOJI, \
    TITLES_PER_LVL
from PIL import Image, ImageDraw, ImageFont


class LevelSystem:
    
    # LEER ARCHIVO JSON
    async def read_users_data():
        with open('users.json', 'r') as f:
            users = json.load(f)
        return users

    # ESCRIBIR EN ARCHIVO JSON
    async def write_users_data(users):
        with open('users.json', 'w') as f:
            json.dump(users, f)

    async def plant_coins(channel):
            global pick_message_object
            global image_rng_text
            global coin_amount
            
            search_term = 'cangrejo'
            response = requests.get("https://g.tenor.com/v1/search?q={}&key={}&limit=150".format(search_term, TENOR_TOKEN))
            data = response.json()
            random_index = randint(0, len(data['results']) - 1)
            gif_png_url = data['results'][random_index]['media'][0]['gif']['preview']
            image_size = data['results'][random_index]['media'][0]['gif']['dims']

            image_to_pick = Image.open(BytesIO(requests.get(gif_png_url).content))
            
            image_rng_text=str(uuid.uuid4())[9:13]
            font_size = int(0.1*image_size[0]) if image_size[0] > image_size[1] else int(0.1*image_size[1])
            text_font = ImageFont.truetype("impact.ttf", font_size)
            drawOnImage = ImageDraw.Draw(image_to_pick)
            drawOnImage.text(xy=(image_size[0]/2,5), text=image_rng_text, fill=(255,255,255), stroke_fill=(0,0,0), stroke_width=int(font_size/10),font=text_font)
            image_to_pick.save("lastpick.png")

            coin_amount = 1 if randint(1, 100) < 80 else 2
            if coin_amount == 1:
                message_text = "Ha aparecido "+ str(coin_amount) +' ' + SIRI_FAZENDO_PLATA_EMOJI + " siri coin, escribe .pick + código para atraparla"
            else:
                message_text ="Han aparecido"+ str(coin_amount) +' ' + SIRI_FAZENDO_PLATA_EMOJI + " siri coins, escribe .pick + código para atraparlas"
            pick_message_object = await channel.send(message_text,file=discord.File('lastpick.png'))
            return True,image_rng_text,pick_message_object,coin_amount

    async def try_pick(channel):
        print('')

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
            current_lvl_base_xp = 47.2298*(2*(user_lvl)- 3)**(20/11)

            title = TITLES_PER_LVL[user_lvl]

            old_min = int(current_lvl_base_xp)
            old_max =  int(next_lvl_xp)
            progress_current_lvl = int(((user_xp - old_min) * (10 - 1)) / (old_max - old_min)) + 1

            embedVar = discord.Embed(
                title=user.display_name, description='', color=0xFFA500)
            embedVar.set_thumbnail(url=user.avatar_url)
            embedVar.add_field(name=title, value="XP : " +
                            str(user_xp), inline=True)
            embedVar.add_field(name="Monedas :", value=str(
                users[str(user.id)]['coins']) + SIRI_FAZENDO_PLATA_EMOJI, inline=True)
            embedVar.add_field(name="LVL " + str(user_lvl) + " ------------------> " + " LVL " + str(user_lvl+1),
                            value=progress_current_lvl * ":orange_heart:" + (10-progress_current_lvl) * ":white_heart:", inline=False)
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
