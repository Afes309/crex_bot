import requests
import datetime
import base64
import hmac
from hashlib import sha512

import time


baseUrl = 'https://api.crex24.com'
apiKey = ''
secret = ''






'''Получаем список свих заявок'''
def get_activeorders():
	path = "/v2/trading/activeOrders"

	nonce = round(datetime.datetime.now().timestamp() * 1000)

	key = base64.b64decode(secret)
	message = str.encode(path + str(nonce), "utf-8")
	t_hmac = hmac.new(key, message, sha512)
	signature = base64.b64encode(t_hmac.digest()).decode()

	headers = {'X-CREX24-API-KEY':apiKey,'X-CREX24-API-NONCE':str(nonce),'X-CREX24-API-SIGN':signature}


	r = requests.get(baseUrl+path, headers = headers)
	#print(r.text)

	orders_list = []

	for i in r.json():
		instr_1 = i['instrument'].split('-')[0]
		instr_2 = i['instrument'].split('-')[1]
		data = (f'{i["timestamp"]}\n{i["instrument"]}\nID ордера {i["id"]}\nТип {i["side"]}\nИсп./Всего {i["volume"]-i["remainingVolume"]}/{i["volume"]} {instr_1}\nЦена {i["price"]:.10f} {instr_2}\n')
		
		orders_list.append(data)
	#print(orders_list)
	return orders_list


def get_recenttrades(instrument,limit):
	path = '/v2/public/recentTrades?instrument='+instrument+'&limit='+limit

	r = requests.get(baseUrl+path)


'''Получаем список ордеров'''
def get_orderbook(instrument,limit):

	instr_1 = instrument.split('-')[0]

	path = '/v2/public/orderBook?instrument='+instrument+'&limit='+limit
	r = requests.get(baseUrl+path)
	resp_buy = r.json()['buyLevels']
	resp_sell = r.json()['sellLevels']
	#print(f'Покупка {instr_1}\n {resp_buy[0]}')
	#print(f'Продажа {instr_1}\n {resp_sell[0]}')

	orders = {}

	for i in range(5):
		try:
			orders[f'buy{i}'] = f'{resp_buy[i]["price"]:.10f}          {resp_buy[i]["volume"]:.3f}'
		except:
			orders[f'buy{i}'] = ''
		try:
			orders[f'sell{i}'] = f'{resp_sell[i]["price"]:.10f}        {resp_sell[i]["volume"]:.3f}'
		except:
			orders[f'sell{i}'] = ''

	order_str = f"Покупка					Продажа\n\nЦена 			Кол-во Цена 			Кол-во\n🟢{orders['buy0']}		🔴{orders['sell0']}\n🟢{orders['buy1']}		🔴{orders['sell1']}\n🟢{orders['buy2']}		🔴{orders['sell2']}\n"

	order_str_by = f"🟢ПОКУПКА ({instrument})\n\nЦена                          Кол-во\n{orders['buy0']}\n{orders['buy1']}\n{orders['buy2']}\n{orders['buy3']}\n{orders['buy4']}\n"
	order_str_sell = f"🔴ПРОДАЖА ({instrument})\n\nЦена                        Кол-во\n{orders['sell0']}\n{orders['sell1']}\n{orders['sell2']}\n{orders['sell3']}\n{orders['sell4']}\n"

	return order_str_by,order_str_sell

	
'''Получаем историю сделок'''
def get_recenttrades(instrument,limit):

	instr_1 = instrument.split('-')[0]

	path = '/v2/public/recentTrades?instrument='+instrument+'&limit='+limit
	r = requests.get(baseUrl+path)

	

	recenttrades_mess = 'Время Цена Объем\n\n'

	for i in r.json():
		if i['side'] == 'sell':
			recenttrades_mess += f"🔴 {i['timestamp']}\n    {i['price']:.9f}    {i['volume']:.1f}\n"
		
		elif i['side'] == 'buy':
			recenttrades_mess += f"🟢 {i['timestamp']}\n    {i['price']:.9f}    {i['volume']:.1f}\n"


	return recenttrades_mess

'''Получаем баланс валют'''
def get_balances():
	path = '/v2/account/balance'

	nonce = round(datetime.datetime.now().timestamp() * 1000)

	key = base64.b64decode(secret)
	message = str.encode(path + str(nonce), "utf-8")
	t_hmac = hmac.new(key, message, sha512)
	signature = base64.b64encode(t_hmac.digest()).decode()

	headers = {'X-CREX24-API-KEY':apiKey,'X-CREX24-API-NONCE':str(nonce),'X-CREX24-API-SIGN':signature}


	r = requests.get(baseUrl+path, headers = headers)

	coin_balence = 'БАЛАНС\n\n'

	for i in r.json():
		coin_balence += f"Валюта({i['currency']})\n Доступно--{i['available']:.9f} В ордерах--{i['reserved']}\n"

	return coin_balence



if __name__ == '__main__':

	get_balances()

	#get_recenttrades('CHND-BTC','1000')