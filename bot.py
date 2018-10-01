import os
import datetime

import telegram
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from apscheduler.schedulers.background import BackgroundScheduler

from utils import get_info_atms
from atms import reload_atms

sched = BackgroundScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=8)
def scheduled_job():
    reload_atms()

def list_atms(bot, update, chat_data):
	"""
		Manejador para el comando /banelco o /link
	"""

	chat_id = update.message.chat_id
	chat_data[chat_id] = {'command': update.message.text, 'location':{}}
	reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('Enviar Ubicación', request_location=True)]])
	bot.sendMessage(chat_id, 'Por favor, envie su ubicación', reply_markup=reply_markup)

def proc_location(bot, update, chat_data):
	"""
		Manejador para los comandos que reciben
		localizaciones
	"""

	chat_id = update.message.chat_id	

	data = chat_data[chat_id]
	data['location'] = update.message.location

	bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

	msg, img = get_info_atms(data)

	if len(msg):
		bot.sendMessage(chat_id, msg)
		try:
			bot.send_photo(chat_id, photo=img)
		except Exception:
			bot.sendMessage(chat_id, "No se pudo cargar imagen con ubicación de los cajeros")
	else:
		bot.sendMessage(chat_id, "No hay cajeros automáticos cercanos")

	reply_markup = telegram.ReplyKeyboardRemove()
	bot.send_message(chat_id,"Adiós", reply_markup=reply_markup)

def main():

	updater = Updater(os.environ['API_KEY_TELEGRAM'])

	updater.dispatcher.add_handler(CommandHandler(['banelco', 'link'], list_atms, pass_chat_data=True))
	updater.dispatcher.add_handler(MessageHandler(Filters.location, proc_location, pass_chat_data=True))

	sched.start()

	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()