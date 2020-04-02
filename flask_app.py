"""
@name : flask_app.py
@author: Marco Iannella (altair1016)
"""
import set_token as st
import time
import os
from flask import Flask
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import urllib.request
import user_get_data as ugd
import speech2text as sp
import file_check as fc

get_setup = st.SetToken()
SECRET = get_setup.get_secret()
TOKEN = get_setup.get_token()

print(SECRET, TOKEN)
os._exit(0)
BOT = telepot.Bot(TOKEN)
BASIC_INFO_MESSAGE = "\n\nPuoi avere ulteriori informazioni. Come fare:" \
                     "\n- *Digita il nome della tua regione o provincia*" \
                     "\n- *Prova a chiederglielo* (es. Dammi le info per la regione Lazio)" \
                     "\n- *Premi uno dei seguenti tasti per ottenere informazioni*"

APP = Flask(__name__)

@APP.route('/{}'.format(SECRET), methods=["POST"])


def keyboard_dev():
    elements = [
        [InlineKeyboardButton(text='Bollettino giornaliero', callback_data='bg')],
        [InlineKeyboardButton(text='Rapporto Contagi', callback_data='info1'),
         InlineKeyboardButton(text='Globale', callback_data='info2')],
        [InlineKeyboardButton(text='Decessi', callback_data='info3'),InlineKeyboardButton(text='Nuovi contagi', callback_data='info4'),
         InlineKeyboardButton(text='Dimessi guariti', callback_data='info5')],
        [InlineKeyboardButton(text='Mappa Regioni', callback_data='info6'),
         InlineKeyboardButton(text='Mappa Province', callback_data='info7')]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=elements)
    return keyboard

def on_chat_message(msg):
    """
    Function from Telepot
    :param msg: telegram message
    :return: none
    """
    content_type, chat_type, chat_id = telepot.glance(msg)
    covid_data = ugd.UserGetData()
    name = msg["from"]["first_name"]
    txt = ""
    keyboard = keyboard_dev()

    if "text" in msg.keys():
        txt = msg["text"]
    if "voice" in msg.keys():
        voice = BOT.getFile(msg["voice"]["file_id"])
        print(voice)
        url = "https://api.telegram.org/file/bot" + TOKEN + "/" + voice["file_path"]
        path = fc.dir_exists("voice")
        urllib.request.urlretrieve(url, voice["file_path"])
        BOT.sendChatAction(chat_id, 'typing')
        voice_text = sp.sp2tx(voice["file_path"])
        BOT.sendChatAction(chat_id, 'typing')
        os.remove(voice["file_path"])
        os.remove(voice["file_path"].split('.')[0] + '.wav')
        voice_result = covid_data.get_data_voice(voice_text)

        if type(voice_result[0]) == list:
            message = "".join(voice_result[0])

        if voice_result[1]:
            BOT.sendMessage(chat_id, "{}, hai detto: '*{}*'. {}".format(
            name, voice_text, voice_result[0]), reply_markup=keyboard, parse_mode='Markdown')

        elif voice_result[1] is False:
            BOT.sendMessage(chat_id, "{}, hai detto: '*{}*'. "
                                     "Ti ricordo che puoi: {}".format(
                name, message , BASIC_INFO_MESSAGE), reply_markup=keyboard, parse_mode='Markdown')
            pass



    if txt == "/start":
        BOT.sendMessage(chat_id, "Benvenuto {}, qui puoi trovare un riassunto dei dati condivisi  "
                                 "dalla Protezione Civile circa la situazione nazionale italiana sui contagi Covid-19.\n{}".format(name, BASIC_INFO_MESSAGE),reply_markup=keyboard, parse_mode='Markdown')

    if content_type == 'text':
        arr = [covid_data.get_district_today_bulletin(txt), covid_data.get_regional_today_bulletin(txt)]
        BOT.sendChatAction(chat_id, 'typing')
        time.sleep(2)
        if arr[0][1] == False and arr[1][1] == False:
            if txt != "/start":
                BOT.sendMessage(chat_id, "Ciao {}, ti ricordo di usare i tasti predefiniti qui sotto. {}".format(name, BASIC_INFO_MESSAGE), reply_markup=keyboard, parse_mode='Markdown')
        else:

            if arr[0][1]:
                value_msg = arr[0][0]
            elif arr[1][1]:
                value_msg = arr[1][0]

            BOT.sendMessage(chat_id, value_msg + "\nPer avere altri dettagli: " + BASIC_INFO_MESSAGE, reply_markup=keyboard, parse_mode='Markdown')
    else:
        BOT.sendMessage(chat_id, "", reply_markup=keyboard)

def on_callback_query(msg):
    """
    Call back function from Telepot
    :param msg: telegram message
    :return: none
    """

    covid_data = ugd.UserGetData()
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, chat_id, query_data)
    if query_data == 'bg':
        text_message = covid_data.get_today_bulletin()
        BOT.sendMessage(chat_id, "Eccoti le informazioni richieste:\n\n\t" + text_message)

    elif query_data == 'info1':
        img_path = covid_data.get_whole_bulletin_perc_trend()
        BOT.sendChatAction(chat_id, 'upload_photo')
        time.sleep(2)
        BOT.sendPhoto(chat_id, open(img_path, 'rb'),
                      "Ecco qualche informazione grafica alla percentuale contagi. "
                      "La formula utilizzata per il calcolo è : "
                      "casi_positivi/numero_tamponi_giornaliero * 100")
    elif query_data == 'info2':
        img_path = covid_data.get_whole_bulletin_trend()
        BOT.sendChatAction(chat_id, 'upload_photo')
        time.sleep(2)
        BOT.sendPhoto(chat_id, open(img_path, 'rb'), "Ecco qualche informazione grafica relativamente ai contagi, deceduti e guariti")
    elif query_data == 'info3':
        img_path = covid_data.get_generic_bulletin_trend("diff","deceduti", "Decessi", "r")
        BOT.sendChatAction(chat_id, 'upload_photo')
        time.sleep(2)
        BOT.sendPhoto(chat_id, open(img_path, 'rb'), "Ecco qualche informazione grafica relativamente ai decessi")
    elif query_data == 'info4':
        img_path = covid_data.get_generic_bulletin_trend("","nuovi_positivi", "Nuovi Contagi", "b")
        BOT.sendChatAction(chat_id, 'upload_photo')
        time.sleep(2)
        BOT.sendPhoto(chat_id, open(img_path, 'rb'), "Ecco qualche informazione grafica relativamente ai nuovi contagi")
    elif query_data == 'info5':
        img_path = covid_data.get_generic_bulletin_trend("","dimessi_guariti", "Dimessi guariti", "g")
        BOT.sendChatAction(chat_id, 'upload_photo')
        time.sleep(2)
        BOT.sendPhoto(chat_id, open(img_path, 'rb'), "Ecco qualche informazione grafica relativamente ai dimessi guariti")
    elif query_data == 'info6':
        ##img_path = gg.map_generator()
        png_path = "figures/heatmap/png/global/"
        BOT.sendChatAction(chat_id, 'upload_photo')
        os.system("python3.7 geomap_generator.py")
        img_path = png_path + fc.file_exists(png_path)
        BOT.sendChatAction(chat_id, 'upload_photo')
        BOT.sendPhoto(chat_id, open(img_path, 'rb'), "Mappa delle regioni contagiate")
    elif query_data == 'info7':
        png_path = "figures/heatmap/png/district/"
        BOT.sendChatAction(chat_id, 'upload_photo')
        os.system("python3.7 geomap_generator.py d")
        img_path = png_path + fc.file_exists(png_path)
        BOT.sendChatAction(chat_id, 'upload_photo')
        BOT.sendPhoto(chat_id, open(img_path, 'rb'), "Mappa delle province contagiate")

    BOT.answerCallbackQuery(query_id, text="")

    keyboard = keyboard_dev()
    BOT.sendMessage(chat_id, BASIC_INFO_MESSAGE, reply_markup=keyboard, parse_mode='Markdown')


BOT = telepot.Bot(TOKEN)
#bot.message_loop(on_chat_message)
MessageLoop(BOT, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')
while 1:
    time.sleep(10)
