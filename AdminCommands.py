import json
from datetime import date, timedelta
from random import randint

import requests
from BotTokens import EXCHANGE_RATE_TOKEN
from EmbedMessages import EmbedMessages
from EnvironmentVariables import OWNER_ID, SIRI_FAZENDO_PLATA_EMOJI, bomdia_gifs, bomdia_messages, \
    not_allowed_channel_ids
from LevelSystem import LevelSystem, pending_pick


class AdminCommands:

    # ATRIBUTOS DE CLASE
    cache_rate = 0
    
    async def process_commands(channel,text,original_message):
            
        if original_message.author.id == OWNER_ID:

            global pending_pick

            if text.startswith('.ttest'):
                await EmbedMessages.send_embed_msg(channel,None,AdminCommands.daily_USD_to_COP())

            if text.startswith('.setusd'):
                AdminCommands.cache_rate = int(text[len('.setusd ' ):len(text)])
                await original_message.add_reaction('✨')
                
            # ESTE METODO SE USA PARA HACER QUE EL BOT ENVIE CUALQUER MENSAJE QUE DESEEMOS
            if text.startswith('.anuncio'):           
                await EmbedMessages.send_embed_msg(channel,None,text[len('.anuncio' ):len(text)])
                await original_message.delete()

            # CAMBIAR LA PROBABILIDAD DE QUE SIRI PLANTE COINS
            if text.startswith('.setchance'):
                LevelSystem.chance = int(text[len('.setchance '):])
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
                await LevelSystem.plant_coins(channel,password,True)

    async def daily_message(channel):
        random_index1 = randint(0, len(bomdia_messages) - 1)
        random_index2 = randint(0, len(bomdia_gifs) - 1)
        await EmbedMessages.send_embed_msg(channel,None,bomdia_messages[random_index1])
        await channel.send(bomdia_gifs[random_index2])

    def daily_USD_to_COP():
        payload = {}
        headers= {"apikey": EXCHANGE_RATE_TOKEN}
        today = date.today().strftime('%Y-%m-%d') 
        yesterday = (date.today() - timedelta(days = 2)).strftime('%Y-%m-%d') 
        convert_url = "https://api.apilayer.com/currency_data/timeframe?start_date={}&end_date={}".format(yesterday,today)
        convert_response = requests.request("GET", convert_url, headers=headers, data = payload)
        json_convert_response = json.loads(convert_response.text)
        today_rate=int(json_convert_response['quotes'][today]['USDCOP'])
        yesterday_rate=int(json_convert_response['quotes'][yesterday]['USDCOP'])
        
        if AdminCommands.cache_rate == 0:
            change_percentage = ((today_rate-yesterday_rate)/yesterday_rate)*100
        else:
            change_percentage = ((today_rate-AdminCommands.cache_rate)/AdminCommands.cache_rate)*100

        AdminCommands.cache_rate = today_rate
        
        base_message = '💵** 1 USD ** -> $ ' + str(today_rate) + '** COP**💰' + ' % ' + "{:.2f}".format(change_percentage)
        
        if change_percentage > 0.00:
            return( base_message+ ' 📈')
        elif change_percentage == 0.00:
            return( base_message)
        else:
            return( base_message+ ' 📉')
