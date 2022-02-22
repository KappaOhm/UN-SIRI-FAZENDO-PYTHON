import discord

from vars import message_for_role_id
from vars import id_role_Design
from vars import id_role_Coding
from vars import id_role_Chismecito
from vars import id_role_RedRoom
from vars import id_role_ShitPost
from vars import id_role_Sales
from vars import id_role_Survival
from vars import id_role_FPS

class handle_roles:

    async def remove_or_add_role(client, payload, is_add):

            if payload.message_id == message_for_role_id:
                guild_id = payload.guild_id
                guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
                if payload.emoji.name == '🎨':
                    role = discord.utils.get(guild.roles,
                                            id=id_role_Design)  # DISEÑADOR
                elif payload.emoji.name == '📟':
                    role = discord.utils.get(guild.roles,
                                            id=id_role_Coding)  # PROGRAMADOR
                elif payload.emoji.name == '🙊':
                    role = discord.utils.get(guild.roles,
                                            id=id_role_Chismecito)  # CHISMECITO
                elif payload.emoji.name == 'Panting':
                    role = discord.utils.get(guild.roles,
                                            id=id_role_RedRoom)  # REDROOM
                elif payload.emoji.name == 'TomUhm':
                    role = discord.utils.get(guild.roles,
                                            id=id_role_ShitPost)  # SHITPOST
                elif payload.emoji.name == 'MaruMoney':
                    role = discord.utils.get(guild.roles,
                                            id=id_role_Sales)  # OFERTAS
                elif payload.emoji.name == 'MinecraftGrassBlock':
                    role = discord.utils.get(guild.roles,
                                            id=id_role_Survival)  # SURVIVAL
                elif payload.emoji.name == 'KeyF':
                    role = discord.utils.get(guild.roles, id=id_role_FPS)  # FPS
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