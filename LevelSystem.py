import json
from random import randint

import discord
from EmbedMessages import EmbedMessages
from EnvironmentVariables import COINS_PER_LVL, LVLUP_MESSASGES, SAFADOS_ROLE_ID, SERVER_ID, SIRI_FAZENDO_PLATA_EMOJI, \
    TITLES_PER_LVL


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
            next_lvl_xp = 166*(-1.5 + user_lvl + 1)**(1.80)

            title = TITLES_PER_LVL[user_lvl]

            old_range = int(next_lvl_xp - 0)
            new_range = (10 - 1)
            top_next_lvl = int((((next_lvl_xp - 0) * new_range) / old_range) + 1)
            progress_current_lvl = int(
                (((user_xp - 0) * new_range) / old_range) + 1)

            embedVar = discord.Embed(
                title=user.display_name, description='', color=0xFFA500)
            embedVar.set_thumbnail(url=user.avatar_url)
            embedVar.add_field(name=title, value="XP : " +
                            str(user_xp), inline=True)
            embedVar.add_field(name="Monedas :", value=str(
                users[str(user.id)]['coins']) + SIRI_FAZENDO_PLATA_EMOJI, inline=True)
            embedVar.add_field(name="LVL " + str(user_lvl) + " ------------------> " + " LVL " + str(user_lvl+1),
                            value=progress_current_lvl * ":orange_heart:" + (top_next_lvl-progress_current_lvl) * ":white_heart:", inline=False)
            await channel.send(embed=embedVar)
            await LevelSystem.write_users_data(users)
        else:
            await EmbedMessages.embed_message.send_embed_msg(channel, None, "Este usuario aún no acumula XP 🎲")


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
