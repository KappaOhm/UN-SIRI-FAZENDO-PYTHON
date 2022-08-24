from EmbedMessages import EmbedMessages
from EnvironmentVariables import OWNER_ID, SIRI_FAZENDO_PLATA_EMOJI, not_allowed_channel_ids
from LevelAndCoinsSystem import LevelSystem, pending_pick

# INICIARLIZAR VARIABLES
chance = 4

class AdminCommands:
    
        async def process_commands(channel,text,original_message):
            
            if original_message.author.id == OWNER_ID:

                global pending_pick

                # ESTE METODO SE USA PARA HACER QUE EL BOT ENVIE CUALQUER MENSAJE QUE DESEEMOS
                if text.startswith('.anuncio'):           
                    await EmbedMessages.send_embed_msg(channel,None,text[len('.anuncio' ):len(text)])
                    await original_message.delete()

                # CAMBIAR LA PROBABILIDAD DE QUE SIRI PLANTE COINS
                if text.startswith('.setchance'):
                    global chance
                    chance = int(text[len('.setchance '):])
                    await original_message.add_reaction('✨')  

                # DAR MONEDAS
                if text.startswith('.award'):
                    users = await LevelSystem.read_users_data()
                    number_of_coins = int(text[len('.award '):text.index("<")])
                    user = original_message.mentions[0] 
                    users[str(user.id)]['coins'] += number_of_coins
                    await EmbedMessages.send_embed_msg(channel, None, "¡Te han otorgado " + str(number_of_coins) + "" + SIRI_FAZENDO_PLATA_EMOJI + " monedas!" + user.mention)
                    await LevelSystem.write_users_data(users)
                    await original_message.delete()
                    
                # PLANTAR MONEDAS
                if text.startswith('.plant') and channel.id not in not_allowed_channel_ids and pending_pick==False:
                    password = text[len('.plant '):]
                    await original_message.delete()
                    await LevelSystem.plant_coins(channel,password)
