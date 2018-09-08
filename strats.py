import json

#BOOK BOND BUY 999:12 998:100 995:1 SELL 1001:4 1002:15 1003:100

CONVERT_FEE = 10

def bond_passive(prices, order_id):

	buy_bond_price = 1000
	buy_size = -1

	sell_bond_price = 1000
	sell_size = -1
	
	if len(prices["buy"]) > 0:
		buy_bond_price = prices["buy"][0][0]
		buy_size = prices["buy"][0][1]

	if len(prices["sell"]) > 0:
		sell_bond_price = prices["sell"][0][0]
		sell_size = prices["sell"][0][1]

	if buy_bond_price > 1000:
		return {"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "SELL", "price": buy_bond_price, "size": buy_size}

	if sell_bond_price < 1000:
		return {"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "BUY", "price": sell_bond_price, "size": sell_size}


def adr(babz_prices, baba_prices, order_id):

	babz_buy_price = -1
	babz_buy_size = -1

	babz_sell_price = -1
	babz_sell_size = -1

	baba_buy_price = -1
	baba_buy_size = -1

	baba_sell_price = -1
	baba_sell_size = -1

	if len(babz_prices["buy"]) > 0 and len(babz_prices["sell"]) > 0 and len(baba_prices["buy"]) > 0 and len(baba_prices["sell"]) > 0:
		babz_buy_price = babz_prices["buy"][0][0]
		babz_buy_size = babz_prices["buy"][0][1]

		babz_sell_price = babz_prices["sell"][0][0]
		babz_sell_size = babz_prices["sell"][0][1]

		baba_buy_price = baba_prices["buy"][0][0]
		baba_buy_size = baba_prices["buy"][0][1]

		baba_sell_price = baba_prices["sell"][0][0]
		baba_sell_size = baba_prices["sell"][0][1]

		if babz_sell_price + CONVERT_FEE < baba_sell_price:
			return {"type": "add", "order_id": order_id, "symbol": "BABA", "dir": "BUY", "price": baba_sell_price, "size": baba_sell_size}

		if babz_buy_price > baba_buy_price + CONVERT_FEE:
			return {"type": "add", "order_id": order_id, "symbol": "BABA", "dir": "SELL", "price": baba_buy_price, "size": baba_buy_size}








