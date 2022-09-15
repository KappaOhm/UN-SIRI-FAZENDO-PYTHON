import json
from datetime import date, timedelta
from random import randint

import requests
from BotTokens import EXCHANGE_RATE_TOKEN, NEWSAPI_TOKEN
from EmbedMessages import EmbedMessages
from EnvironmentVariables import OWNER_ID, SIRI_FAZENDO_PLATA_EMOJI, bomdia_gifs, bomdia_messages, \
    not_allowed_channel_ids
from LevelSystem import LevelSystem, pending_pick
from newsapi import NewsApiClient


class AdminCommands:

    async def process_commands(channel,text,original_message):
            
        if original_message.author.id == OWNER_ID:

            global pending_pick

            if text.startswith('.tnews'):
                await AdminCommands.daily_new(channel)
                
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

    async def daily_new(channel):
        news_API = NewsApiClient(api_key=NEWSAPI_TOKEN)
        languages = ['en','es']
        countries = ['us','co']
        categories = ['science','health','science','technology','science','science','science']
        random_index1 = randint(0, len(languages) - 1)
        # /v2/top-headlines
        top_headlines = news_API.get_top_headlines(
            category = categories[randint(0, len(categories) - 1)],
            language = languages[random_index1],
            country  = countries[random_index1],
            page=1)

        denied_sites =['Semana.com','Pulzo.com','Theverge.com','tycsports.com']
        random_index2 = randint(0, len(top_headlines['articles'])-1)
        source_name = top_headlines['articles'][random_index2]['source']['name']
        if source_name.lower() not in (site.lower() for site in denied_sites):
            random_index2 = randint(0, len(top_headlines['articles'])-1)
            print(top_headlines['articles'][random_index2]['title'])
            await channel.send(AdminCommands.daily_USD_to_COP() + '\n\n' + '**' + top_headlines['articles'][random_index2]['title']+ '**' + '\n\n' + top_headlines['articles'][random_index2]['url'])
        else:
            await AdminCommands.daily_new(channel)
    
    def daily_USD_to_COP():
        convert_url = "https://api.apilayer.com/exchangerates_data/convert?to=COP&from=USD&amount=1"
        payload = {}
        headers= {"apikey": EXCHANGE_RATE_TOKEN}

        convert_response = requests.request("GET", convert_url, headers=headers, data = payload)
        json_convert_response = json.loads(convert_response.text)

        today = date.today().strftime('%Y-%m-%d') 
        yesterday = (date.today() - timedelta(days = 2)).strftime('%Y-%m-%d') 
        url = "https://api.apilayer.com/exchangerates_data/timeseries?start_date={}&end_date={}".format(yesterday,today)
        change_response = requests.request("GET", url, headers=headers, data = payload)
        json_change_response = json.loads(change_response.text)
        today_rate=int(json_change_response['rates'][today]['COP'])
        yesterday_rate=int(json_change_response['rates'][yesterday]['COP'])
        change_percentage = ((today_rate-yesterday_rate)/yesterday_rate)*100


        base_message = '💵** 1 USD ** -> $ ' + str(int(json_change_response['rates'][today]['COP'])) + '** COP**💰' + ' % ' + "{:.2f}".format(change_percentage)
        
        if change_percentage > 0:   
            return( base_message+ ' 📈')
        else:
            return( base_message+ ' 📉')
