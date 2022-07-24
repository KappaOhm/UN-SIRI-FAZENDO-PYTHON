import discord
from EnvironmentVariables import CHISMECITO_ROLE_ID, CODING_ROLE_ID, DESIGN_ROLE_ID, FPS_ROLE_ID, MESSAGE_FOR_ROLE_ID, \
    REDROOM_ROLE_ID, SALES_ROLE_ID, SHITPOST_ROLE_ID, SURVIVAL_ROLE_ID


class HandleRoles:

    async def remove_or_add_role(client, payload, is_add):

            if payload.message_id == MESSAGE_FOR_ROLE_ID:
                guild_id = payload.guild_id
                guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
                if payload.emoji.name == '🎨':
                    role = discord.utils.get(guild.roles,
                                            id=DESIGN_ROLE_ID)  # DISEÑADOR
                elif payload.emoji.name == '📟':
                    role = discord.utils.get(guild.roles,
                                            id=CODING_ROLE_ID)  # PROGRAMADOR
                elif payload.emoji.name == '🙊':
                    role = discord.utils.get(guild.roles,
                                            id=CHISMECITO_ROLE_ID)  # CHISMECITO
                elif payload.emoji.name == 'Panting':
                    role = discord.utils.get(guild.roles,
                                            id=REDROOM_ROLE_ID)  # REDROOM
                elif payload.emoji.name == 'TomUhm':
                    role = discord.utils.get(guild.roles,
                                            id=SHITPOST_ROLE_ID)  # SHITPOST
                elif payload.emoji.name == 'MaruMoney':
                    role = discord.utils.get(guild.roles,
                                            id=SALES_ROLE_ID)  # OFERTAS
                elif payload.emoji.name == 'MinecraftGrassBlock':
                    role = discord.utils.get(guild.roles,
                                            id=SURVIVAL_ROLE_ID)  # SURVIVAL
                elif payload.emoji.name == 'KeyF':
                    role = discord.utils.get(guild.roles, id=FPS_ROLE_ID)  # FPS
                else:
                    role = discord.utils.get(guild.roles, name=payload.emoji.name)
                    
                if role is not None:
                    member = discord.utils.get(guild.members, id=payload.user_id)
                    if member is not None:
                        if is_add:
                            await member.add_roles(role)
                            print("Added role: ", role)
                        else:
                            await member.remove_roles(role)
                            print("Removed role: ", role)
                    else:
                        print("Member not found.")
                else:
                    print("Role not found.")
