import discord
from EnvironmentVariables import SIRI_IMAGE

last_reply_msg = None

class EmbedMessages:
    # ENVIAR MENSAJES EMBEBIDOS (EL FORMATO ES MAS BONITO)
    async def send_embed_msg(channel, title, description):
        def_description = description if description is not None else ''
        def_title = title if title is not None else ''
        embedVar = discord.Embed(title=def_title,
                                description=def_description,
                                color=0xFFA500)
        return await channel.send(embed=embedVar)

    # EMBEDIDO CON LOS COMANDOS DE MUSICA AL USAR .help
    async def help_embed_msg(message):
        embedVar = discord.Embed(title="Lista de comandos",
                                description="Estos son los comandos disponibles de un siri fanzendo barra",
                                color=0xFFA500)
        embedVar.set_author(name="by KappaOhm")
        embedVar.set_thumbnail(url=SIRI_IMAGE)
        embedVar.add_field(
            name=".cmd", value="Muestra comandos relacionados a XP y monedas", inline=False)
        embedVar.add_field(
            name=".setcum", value="Registra tu propio cumpleaños indicando el día y el mes (DD-MM)", inline=False)
        embedVar.add_field(
            name=".deletecum", value="Borra el registro de tu cumpleaños", inline=False)        
        embedVar.add_field(
            name=".gif", value="Seguido de un termino de busqueda hace que siri busque y responda con un GIF relacionado", inline=False)
        embedVar.add_field(
            name=".play | .p", value="Reproduce enlaces o terminos de busqueda de Youtube \n Es posible agregar playlists y seguir usando el comando para agregar más canciones", inline=False)
        embedVar.add_field(
            name=".next | .n", value="Permiten avanzar a la siguiente canción en cola", inline=False)
        embedVar.add_field(
            name=".shuffle | .s", value="Aleatoriza el orden de las canciones en cola", inline=False)
        embedVar.add_field(
            name=".stop", value="Detiene la reproducción de música y vacia la cola de reproducción", inline=False)
        embedVar.add_field(
            name=".clear", value="Vacia la cola de reproducción", inline=False)
        embedVar.add_field(
            name=".q", value="Muestra la cola 😈 (de reproducción)", inline=False)
        embedVar.add_field(
            name=".leave", value="Desconecta a siri del chat de voz", inline=False)
        await message.channel.send(embed=embedVar)
    
    # EMBEDIDO CON LOS COMANDOS ALREDEDOR DE XP Y MONEDAS AL USAR .cmd
    async def cmd_embed_msg(message):
        embedVar = discord.Embed(title="Lista de comandos relacionados a XP y monedas",
                                description="",
                                color=0xFFA500)
        embedVar.set_author(name="by KappaOhm")
        embedVar.set_thumbnail(url=SIRI_IMAGE)
        embedVar.add_field(name=".xp | .xp @usuario",
                        value="Muestra la informacion del usuario", inline=False)
        embedVar.add_field(name=".pick",
                        value="Seguido de un codigo aleatorio de 4 caracteres recoge siri monedas plantadas", inline=False)
        embedVar.add_field(
            name=".lb", value="Muestra la tabla de puntuaciones de experiencia", inline=False)
        embedVar.add_field(
            name=".par X", value="Apuesta X monedas a que un número aleatorio entre 1 y 100 será par", inline=False)
        embedVar.add_field(
            name=".impar X", value="Apuesta X monedas a que un número aleatorio entre 1 y 100 será impar", inline=False)
        await message.channel.send(embed=embedVar)

    async def play_embed_msg(channel, title, description):
        global last_reply_msg

        def_description = description if description is not None else ''
        def_title = title if title is not None else ''
        embedVar = discord.Embed(title=def_title,
                                description=def_description,
                                color=0xFFA500)

        msg = await channel.send(embed=embedVar)
        await msg.add_reaction('⏸️')
        await msg.add_reaction('⏭️')

        if last_reply_msg is not None:
            await last_reply_msg.clear_reactions()
        last_reply_msg = msg 
