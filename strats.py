import json

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

	if bond_price > 1000:
		return {"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "BUY", "price": buy_bond_price, "size": buy_size}

	if bond_price < 1000:

		return {"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "SELL", "price": sell_bond_price, "size": sell_size}





