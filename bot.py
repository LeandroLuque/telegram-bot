from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import telegram
import time
import os
from utils import get_info_atms

users = {} ##Store the command and location by user

def list_atms(bot, update):

	#Store user info
	users[update.message.chat_id] = {'command': update.message.text, 'location':{}}

	reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('Enviar Ubicación', request_location=True)]])

	bot.sendMessage(update.message.chat_id, 'Por favor, envie su ubicación', reply_markup=reply_markup)

def proc_location(bot, update):

	chat_id = update.message.chat_id	

	# retrieve user info
	data = users[chat_id]
	data['location'] = update.message.location

	bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

	msg, img = get_info_atms(data)

	if len(msg) > 0:
		bot.sendMessage(chat_id, msg)
		bot.send_photo(chat_id, photo=img)
	else:
		bot.sendMessage(chat_id, "No hay cajeros automáticos cercanos")

	reply_markup = telegram.ReplyKeyboardRemove()
	bot.send_message(chat_id,"Adiós", reply_markup=reply_markup)

def main():

	updater = Updater(os.environ['API_KEY_TELEGRAM'])

	updater.dispatcher.add_handler(CommandHandler(['banelco', 'link'], list_atms))
	#updater.dispatcher.add_handler(CommandHandler('link', list_link_atms))
	updater.dispatcher.add_handler(MessageHandler(Filters.location, proc_location))


	updater.start_polling()
	updater.idle()



if __name__ == '__main__':
	main()