SERVER_ID = 693278533899780117
OWNER_ID  = 268991138310914048
BOT_ID    = 875112526151577670

DUNGEON_TEXT_CHANNEL_ID      = 100000000000000000
LOBBY_TEXT_CHANNEL_ID        = 693278534642171957
SIRI_CHAT_TEXT_CHANNEL_ID    = 693278534642171957
RED_ROOM_TEXT_CHANNEL_ID     = 909837786415267841
ALT_RED_ROOM_TEXT_CHANNEL_ID = 874297345599238154
SHITPOST_TEXT_CHANNEL_ID     = 874373777797046312

MESSAGE_FOR_ROLE_ID = 945245431766601769

AMATEUR_ROLE_ID     = 840714667008720917
SAFADOS_ROLE_ID     = 874016688247562260
DESIGN_ROLE_ID      = 882360206976221284
CODING_ROLE_ID      = 882360339172298772
CHISMECITO_ROLE_ID  = 875124750056316998
REDROOM_ROLE_ID     = 875472165615599667
SHITPOST_ROLE_ID    = 875472130530242570
SALES_ROLE_ID       = 882360458978422804
SURVIVAL_ROLE_ID    = 840714709535162378
FPS_ROLE_ID         = 875118283521671228

SIRI_FAZENDO_PLATA_EMOJI = "<:SiriFazendoPlata:883917010260615188>"
SIRI_IMAGE = SIRI_IMAGE = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/95fa93bc-bb27-45ae-ab2f-680ea92bd79e/deqbwof-3e625c35-29d3-48bf-9180-9d810de75b35.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzk1ZmE5M2JjLWJiMjctNDVhZS1hYjJmLTY4MGVhOTJiZDc5ZVwvZGVxYndvZi0zZTYyNWMzNS0yOWQzLTQ4YmYtOTE4MC05ZDgxMGRlNzViMzUucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.jBtTOS2i26MbSWyEot-40E6ZjLXeWH9snECMaWVEj2w"
SECONDS_TO_DISCONNECT = 600

pick_message_object = None
voice_client_playing = None

adding_song = False
is_playlist = False
pending_pick = False

songs_titles = []
URL_queue = []

song_playing = ""
image_rng_text = ""
coin_amount = 0
chance = 4
                    #1,2,3,4,5,6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28, 29, 30
COINS_PER_LVL = [0,0,5,5,5,5,10,15,20,25,30,20,20,20,20,25,30,30,30,30,35,40,40,40,40,40,40,50,100,125,200]

TITLES_PER_LVL = ["Noob","Noob","Noob","Mera tía","Aprendiz","Amateur", #1-5
                    "Kinkster","Safado Ajolotote","Safado Ajolotote","Cremosin","Diva", #6-10
                    "Diva","Bichota","Bichota","Bichota","Arrechx", #11-15
                    "Arrechx","Arrechx","xxx","xxx","xxx", #16-20
                    "Master","Master","Leyenda","Leyenda","ski lo mama", #21-25
                    "Admin","Admin","Super Admin","Mega Admin","Giga Admin" #26-30
                ]

LVLUP_MESSASGES =['¡Felicidades!🥳🎉`',
                  '¡Tudo um conchesumadre!🐒`',
                  '¡Eso bichota!💅`',
                  '¡Como lo mueve esa muchachota!💅`'
                    ]

YDL_OPTIONS = {
  'format': 'bestaudio',
  'default_search': 'auto'
    }

FFMPEG_OPTIONS = {
    'before_options':
    '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
    }

not_allowed_channel_ids =[DUNGEON_TEXT_CHANNEL_ID]

cum_messsages =[ 'Bolos de mamão para você 🍰 ¡Feliz cum! ',
                 'Entre más vieja la pasa más sabrosa es la fruta 🥵 ¡Feliz cumpleaños! ',
                 'Parabéns querido amigo. Você nunca será tão jovem novamente, então aproveite 🎉'
                ]

cum_images=['https://media1.tenor.com/images/695be54002b18bcc4fb10396945d9730/tenor.gif?itemid=26302039',
            'https://c.tenor.com/8b7jfGD9lb8AAAAC/happy-birthday-birthday-cake.gif',
            'https://c.tenor.com/1M47Ae-a_2UAAAAC/bob-esponja-las-mananitas.gif',
            'https://c.tenor.com/ol9MSbL43VgAAAAC/happy-birthday.gif',
            'https://c.tenor.com/oJneSXnNGecAAAAC/happy-birthday.gif',
            'https://media4.giphy.com/media/9rO5Aksmn0dHQKXJAu/giphy.gif?cid=790b7611c00252b4856982538886c8e669a0481d322fe39b&rid=giphy.gif&ct=g',
            'https://giphy.com/gifs/lazy-corgi-OSOOHw7N9gb3R06OU7',
            'https://media2.giphy.com/media/xT0BKxnpSJmgU3KtAk/giphy.gif?cid=790b7611cb33a98a5fe7e389e1ba67b81ae51a1ee7c85e97&rid=giphy.gif&ct=g',
            'https://media3.giphy.com/media/mcJohbfGPATW8/giphy.gif?cid=790b7611a433b7adf4410f71edafe0faa553b9a14f4ab3ca&rid=giphy.gif&ct=g',
            'https://i.pinimg.com/564x/3d/9f/05/3d9f059e6dd638dc192febbca9b536a6.jpg'
            ]

bomdia_messages =['¡Hola Bom Día!⭐',
                  'Eu gostaria que você pudesse desfrutar de um dia inesquecível. Com esta mensagem, eu não só lhe desejo um bom dia, mas também desejo que possamos nos ver o mais rapidamente possível, para que os segundos parem de parecer horas🐒',
                  '🦄Problemas, trabalho, dificuldades, decepção … tudo ao seu lado parece uma miniatura, já que só penso em poder estar em seus braços para poder desfrutar do nosso amor juntos. Por esta razão, quero desejar-lhe a minha vida desde o primeiro minuto🦄',
                  '🦀Obrigado por tornar cada despertar mais bonito que o anterior, bom dia a todos.🦀',
                  '🐢Se eu não digo bom dia para você todos os dias, é como se eu estivesse perdendo alguma coisa na minha vida e eu não pudesse aproveitar o dia🐢',
                  '🐒Se você quer ser feliz, você tem que fazer os outros felizes. E contanto que você faça isso feliz você será🐒',
                  '🐸Ninguém é tão rico que não precise de um sorriso. Bom día🐸',
                  '☀️Cada belo trabalho é construído lentamente. Bom día☀️',
                  '🎃A vida é como uma lenda: não importa que seja longa, mas que seja bem contada',
                  '🍉A felicidade não vem de fora, ela nasce de dentro🍉',
                  '🌕Perseverança é muito importante para o sucesso. E se não se cansar de bater à porta com o necessário vigor e paciência, alguém a abrirá no final🌕',
                  '🔮Seja paciente e não espere que tudo venha imediatamente🔮',
                  '✨Se exageramos nossas alegrias, como fazemos com nossas tristezas, nossos problemas perderiam importância✨',
                  '✨Se exageramos nossas alegrias, como fazemos com nossas tristezas, nossos problemas perderiam importância✨',
                  '🍨Se um problema tiver uma solução, não há necessidade de se preocupar. Se não tiver solução, a preocupação não ajuda🍨',
                  '🌺Ter sucesso é falhar repetidamente, mas sem perder o entusiasmo🌺',
                  '🌱Seu tempo é limitado, então não o desperdice vivendo a vida de outra pessoa🌱',
                  '🌈Se você pensa que pode ou se você pensa que não pode, de qualquer forma, você tem toda a razão🌈',
                  '🌈Se você pensa que pode ou se você pensa que não pode, de qualquer forma, você tem toda a razão🌈',
                  '🐋Você nunca pode atravessar o oceano até que você tenha coragem de perder de vista a costa🐋',
                  '🍨O guerreiro de sucesso é um homem médio, mas com um foco apurado como um raio laser🍨',
                  '🍉Tudo o que a mente humana pode conceber, ela pode conquistar🍉',
                  '🌼Você não pode mudar o vento, mas pode pode ajustar as velas do barco para chegar onde quer🌼',
                  '🐸E quando você pensar em desistir, lembre-se dos motivos que te fizeram aguentar até agora🐸',
                  '🌺As dificultades incentivam a perseverança. A perseverança gera força. A força nos torna implacáveis. Nunca desista🌺',
                  '🌕Não diga eu te amo como se fosse um bom dia, diga bom dia como se fosse um eu te amo🌕',
                  '🎃A primeira obrigação de todo ser humano é ser feliz, a segunda é fazer os outros felizes. Bom Dia!',
                  '🌱Se você quer que seus sonhos se tornem realidade, o primeiro passo é levantar! Bom Dia!',
                  '🍉Parece que a vida me devia algo e me pagou com sua linda amizade. Feliz Dia!',
                  '🌼Muito bom dia! Espero que seja tão bonito para você quanto seu sorriso é para os outros🌼',
                  '🌺Desejo a você toda felicidade e amor do mundo, um lindo dia, e que tudo seja lindo e positivo. Eu te amo muito e tenha um feliz dia🌺',
                  '🌺Desejo a você toda felicidade e amor do mundo, um lindo dia, e que tudo seja lindo e positivo. Eu te amo muito e tenha um feliz dia🌺',
                  '🔮Desejo a você um dia maravilhoso cheio de momentos felizes🔮'   
                ]

bomdia_gifs =['https://media.tenor.com/images/0c9d88ea6c328802517f38501aa77d64/tenor.gif',
                'https://tenor.com/view/cute-anime-wave-hi-hello-gif-8807701',
                'https://tenor.com/view/to-love-ru-lala-deviluke-anime-tail-waving-gif-15113196',
                'https://tenor.com/view/neko-anime-kawaii-nya-hi-gif-14223397',
                'https://tenor.com/view/hello-hi-wave-anime-gif-11503720',
                'https://tenor.com/view/anime-hi-girl-wave-hello-gif-5142315',
                'https://tenor.com/view/love-heart-gif-22449692',
                'https://tenor.com/view/anime-girl-run-fall-hi-gif-23177143',
                'https://tenor.com/view/panties-skirt-anime-butt-booty-gif-15810147',
                'https://tenor.com/view/anime-hey-hello-peek-smile-gif-17556391',
                'https://tenor.com/view/cat-pussy-gif-5284960',
                'https://tenor.com/view/momo-and-rito-to-love-ru-momo-and-rito-cuddle-gif-18845471',
                'https://tenor.com/view/hello-wave-cute-anime-cartoon-gif-7537923',
                'https://tenor.com/view/hey-chat-hello-chat-anime-gif-21088710',
                'https://tenor.com/view/corgi-jump-hi-hey-hello-gif-4505201',
                'https://tenor.com/view/anime-girl-wink-flirty-hibike-euphonium-gif-5364920',
                'https://tenor.com/view/hi-hey-gif-21307782',
                'https://tenor.com/view/redo-of-healer-redo-of-a-healer-redo-of-the-healer-anime-anime-girl-gif-20602961',
                'https://tenor.com/view/komi-san-ily-gif-23488189',
                'https://tenor.com/view/crab-rave-mmd-v-tuber-alymew-alymew-dance-gif-22688312',
                'https://tenor.com/view/anime-anime-girl-girl-cat-gif-18514354',
                'https://tenor.com/view/shera-elf-anime-gif-16600170',
                'https://tenor.com/view/hihi-gif-18680839',
                'https://tenor.com/view/hug-anime-anime-cuddle-gif-17789646',
                'https://tenor.com/view/boobs-ecchi-anime-heart-gif-15899467'
            ]

welcome_gifs = [
    'https://tenor.com/view/good-morning-gif-18894104',
    'https://tenor.com/view/welcome-hello-franfine-frandrescher-gif-10692711',
    'https://tenor.com/view/who-are-you-identify-yourself-gun-safety-vest-gif-21025666',
    'https://tenor.com/view/flaming-elmo-gif-21450484',
    'https://tenor.com/view/ara-anime-eyebrow-up-gif-18062714',
    'https://tenor.com/view/ara-ara-lily-ellenn-soulworker-gif-19976514',
    'https://tenor.com/view/sailor-moon-venus-bienvenido-beso-sonrisa-gif-10333326',
    'https://tenor.com/view/welcome-gif-18737601',
    'https://tenor.com/view/anime-welcome-hi-hello-smile-gif-17567703',
    'https://tenor.com/view/welcome-to-our-office-eric-cartman-tolkien-black-south-park-s9e3-gif-22316454',
    'https://tenor.com/view/youre-welcome-cute-smile-gif-16728264',
    'https://tenor.com/view/red-head-girl-anime-welcome-emi-yusa-gif-15338285'
    ]

redroom_responses = [
    'https://tenor.com/view/mmm-blonde-gif-13403074',
    'https://tenor.com/view/yeah-you-know-i-like-it-that-way-smile-pretty-gif-15791825',
    'https://tenor.com/view/lollipop-lips-how-you-doin-you-know-i-like-that-gif-15404129',
    'https://tenor.com/view/like-mmmhmm-i-like-that-shit-lip-bite-sassy-gif-16384921',
    'https://tenor.com/view/anime-smug-face-smug-anime-girl-smug-smug-face-smug-smile-gif-23765538',
    'https://tenor.com/view/anime-yummy-ara-seduced-gif-18335383',
    'https://tenor.com/view/seal-approval-seal-of-approval-sea-lion-gif-5057575',
    'https://tenor.com/view/anime-blushing-lewd-shimoneta-hot-gif-5453531',
    'https://tenor.com/view/marty1234-gif-7333564',
    'https://tenor.com/view/yes-anime-evil-smile-gif-11514563',
    'https://tenor.com/view/horny-anime-gif-19368853',
    'https://tenor.com/view/vrchat-shana-vrchat-shana-lick-licking-gif-14110643',
    'https://tenor.com/view/azur-lane-chibi-shouting-mad-angry-gif-15485754',
    'https://c.tenor.com/HiboJY9qehoAAAAC/nut-button-press.gif',
    'https://tenor.com/view/cum-cum-mode-anime-cum-mode-anime-cum-cum-anime-gif-22504000',
    'https://tenor.com/view/cum-cum-mode-anime-cum-mode-anime-cum-cum-anime-gif-22504000',
    'https://c.tenor.com/3nAdVLDwDxkAAAAC/anime-swinging.gif',
    'https://tenor.com/view/smug-anime-gif-10199270',
    'https://tenor.com/view/sailor-moon-gif-22468266',
    'https://tenor.com/view/yuru-yuri-gif-20021302',
    'https://tenor.com/view/kyouko-toshinou-yuru-yuri-smug-smile-laugh-gif-13909640',
    'https://tenor.com/view/anime-gif-20554208',
    'https://tenor.com/view/shake-girl-lewd-gif-15781464',
    'https://tenor.com/view/spy-x-family-anya-anya-forger-anya-spy-x-family-anya-spy-x-family-anime-gif-25679849',
    'https://tenor.com/view/thumbs-up-gif-20749336'
    ]

contexto = ['te la comes sin pretexto 🤠',
            'Te la comés, la masticás, la tragás sin pretexto. Así no estés dispuesto, pero tal vez alguna vez te lo has propuesto, y te seré honesto, te haré el favor y te lo presto, tan fuerte que tal vez me den arresto. Ya no aguantás ni el sexto, así que lo dejamos pospuesto, pero te falta afecto y te lo dejo otra vez puesto, te aplasto en la pared como insecto tan duro que sale polvo de asbesto, llamo al arquitecto Alberto y al modesto Ernesto, y terminás más abierto que portón de asentamiento, ya no tenés más almacenamiento así que necesitás asesoramiento y a tu madre llamamos para darle su afecto así hasta el agotamiento y al siguiente día repetimos y hasta con repuesto, y te la meto sin pretexto, así no estés dispuesto, pero tal vez alguna vez te lo has propuesto, y te seré honesto te haré el favor y te lo presto, tan fuerte que tal vez me den arresto, ya no aguantás ni el sexto, así que lo dejamos pospuesto, pero te falta afecto y te lo dejo otra vez puesto, te aplasto en la pared como insecto tan duro que sale polvo de asbesto, llamo al arquitecto Alberto y al modesto Ernesto, y terminás más abierto que portón de asentamiento, ya no tenés más almacenamiento así que necesitás asesoramiento y a tu madre llamamos para darle su afecto así hasta el agotamiento y al siguiente día repetimos pero ya estás descompuesto así que para mí continuar sería incorrecto y me voy sin mostrar algún gesto, dispuesto a seguir apenas y ya estés compuesto voy y te doy el impuesto pero no sin antes avisarte que este es el contexto'
            ]

trece = ['Te la empujo y te la pongo pa que me la peses, y te meto la guamayeta un millon de veces que de tanta monda van a respirar hasta los peces si te pareció poco... los dobladillos del culo al leer esto texto se te estremecen, esa raja seca una mondaquera se merece, tranquila que sigo como jason en viernes 13, la cabeza de la mondá después se me adormece, pero tranquilo que eso no te favorece, si se despierta te va regar de leche y después me agradeces, el chiquito se te esflorece, tranquila que de mondá en éste grupo no se carece y si te la meten por el oído te en ensordeces y si te la meten entre todos te desfortaleces y eso no te conviene porque te enflaqueces pero tranquila que esos pelos del culo vuelven y te crecen como campo te reflorece y a tu maldit4 madre se la empujo a veces, ya que el culo se le enmugrece y si me ve la mondá nuevamente se aloquece y eso no te conviene porque me vas hacer que de nuevo contigo empiece te lo meto desde que amanece hasta que anochece. Ahora resulta pasa y acontece que desde que cuando dices el número 13 la monda mía en tu culo aparece, te la hecho adentro y el cuerpo se te estremece, toca recalcar que cuando esta adentro más se crece, ya te di mondaquera que más se te ofrece? Quieres más monda o eso parece, ahora por falta de picha ya no padeces, cada que te lo hecho en la cara te enloqueces, tranquilo que hoy de leche también se te abastece, esto namas es el calentamiento espera un momento a que empiece, te gusta que te de de beber cuando anochece y también tomar cada vez que amanece, me disculpo si usted ya me aborrece, pero mi leche florece en el culo del que diga el número prohibido 13, quieres que siga? te preguntaras si esto me enorgullece, y obvio que enorgullece porque eso allá bajo no se te des humedece, solo se re humedece, no es mi culpa si no aguantas tanto y tu cuerpo se retuerce, pero no te fuerces, tampoco te esfuerces que esta pichera que te doy es buena porque te rejuvenece y así no te envejeces',
         'Aquí tienes pa que me la beses, entre más me la beses más me crece, busca un cura pa que me la rece, y trae un martillo pa que me la endereces, por el chiquito se te aparece toas las veces y cuando te estreses aquí te tengo éste pa que te desestreses, con este tallo el jopo se te esflorece, se cumple el ciclo hasta que anochece, to los días y toas las veces, de tanto entablar la raja del jopo se te desaparece, porque este sable no se compadece, si pides ñapa se te ofrece, y si repites se te agradece, no te hace rico pero tampoco te empobrece, no te hace inteligente pero tampoco te embrutece, y no paro aquí compa que éste nuevamente se endurece, hasta que amanece, cambie esa cara que parece que se entristece, si te haces viejo éste te rejuvenece, no te hago bulla porque depronto te ensordece, y eso cuadro no te favorece, pero tranquilo que éste te abastece, porque allá abajo se te humedece, viendo como el que me cuelga resplandece, si a ti te da miedo a mí me enorgullece, y así toas las vece ¿que te parece?, y tranquilo mijo que aquí éste reaparece, no haga fuerza porque éste se sobrecrece, una fresadora te traigo pa que me la freses, así se fortalece y de nuevo la historia se establece, que no se te nuble la vista porque éste te la aclarece, y sino le entendiste nuevamente la explicación se te ofrece, pa que por el chiquito éste de nuevo te empiece... Aquí tienes para que me la beses, entre más me la beses más me crece, busca un cura para que me la rece, un martillo para que me la endereces, un chef para que me la aderece, 8000 mondas por el culo se te aparecen, si me la sobas haces que se me espese, si quieres la escaneas y te la llevas para que en tu hoja de vida la anexes, te la meto por debajo del agua como los peces, y aquella flor de monda que en tu culo crece, reposa sobre tus nalgas a veces y descansa en paz en tu chicorio cuando anochece'
         ]
