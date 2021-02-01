import telebot
from time import sleep

from crex_bot_c import get_activeorders,get_orderbook,get_recenttrades,get_balances

bot = telebot.TeleBot("")

users = [419779084]

@bot.message_handler(func=lambda message: message.chat.id not in users)
def some(message):
   bot.send_message(message.chat.id, "Sorry")


@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.reply_to(message,'/get_activorders - посмотреть активные ордера\n/orders - посмотреть заявки\n/history - история сделок\n/balance - Получаем баланс валют')

@bot.message_handler(commands=['get_activorders'])
def send_welcome(message):

	orders = get_activeorders()

	for i in orders:
		bot.send_message(message.chat.id,i)


@bot.message_handler(commands=['orders'])
def start_handler(message):
    send = bot.send_message(message.chat.id,'Введи пару валют')
    bot.register_next_step_handler(send,orders)




def orders(message):
	instrument = message.text
	try:
		orders_by,orders_sell = get_orderbook(instrument,'5')

		bot.send_message(message.chat.id,orders_by)
		bot.send_message(message.chat.id,orders_sell)
	except:
		bot.send_message(message.chat.id,'Что-то пошло не так 😢')



@bot.message_handler(commands=['history'])
def start_handler(message):
    send = bot.send_message(message.chat.id,'Введи пару валют')
    bot.register_next_step_handler(send,recenttrades)

def recenttrades(message):
	instrument = message.text

	try:
		history = get_recenttrades(instrument,'10')
		bot.send_message(message.chat.id,history)


		
	except:
		bot.send_message(message.chat.id,'Что-то пошло не так 😢')


@bot.message_handler(commands=['balance'])
def send_balance(message):

	balance = get_balances()

	send = bot.send_message(message.chat.id,balance)
    



bot.polling()
