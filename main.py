import telegram
import time
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ChatAction
import logging
import json
import apiai
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = "922085233:AAHiGf9lDXRCN9V86xsPdF0hz8EdAcVYUdE"
updater = Updater(TOKEN)
PORT = int(os.environ.get('PORT', '8443'))
bot = telegram.Bot(token = TOKEN)
bot.setWebhook("https://akannbot.herokuapp.com/" + TOKEN)

def main():
    
    dispatcher = updater.dispatcher

    # Хендлеры
    start_command_handler = CommandHandler('start', startCommand)
    text_message_handler = MessageHandler(Filters.text, textMessage)

    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN)   
    updater.bot.setWebhook("https://akannbot.herokuapp.com/")       

    # Добавляем хендлеры в диспетчер

    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(text_message_handler)
    
    
    updater.idle()

    
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')

def textMessage(bot, update):
    request = apiai.ApiAI('9099819b68ff4ad790feca12d420626d').text_request()
    request.lang = 'ru'
    request.session_id = 'ANNBot' # ID Сессии диалога (нужно, чтобы потом учить бота)

    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
        
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')
    
if __name__ == '__main__':
    main()  