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

		if buy_bond_price > 1000:
			return {"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "SELL", "price": buy_bond_price, "size": buy_size}

	if len(prices["sell"]) > 0:
		sell_bond_price = prices["sell"][0][0]
		sell_size = prices["sell"][0][1]

		if sell_bond_price < 1000:
			return {"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "BUY", "price": sell_bond_price, "size": sell_size}

def bond_aggro(prices, order_id):

	toReturn = []

	buy_bond_price = 1000
	buy_size = -1

	sell_bond_price = 1000
	sell_size = -1
	
	if len(prices["buy"]) > 0:
		buy_bond_price = prices["buy"][0][0]
		buy_size = prices["buy"][0][1]

		if buy_bond_price < 999:

			return {"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "BUY", "price": buy_bond_price+1, "size": buy_size}

	if len(prices["sell"]) > 0:
		sell_bond_price = prices["sell"][0][0]
		sell_size = prices["sell"][0][1]

		if sell_bond_price > 1001:

			return {"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "SELL", "price": sell_bond_price-1, "size": sell_size}

def adr(babz_prices, baba_prices, order_id):

	toReturn = []

	if len(babz_prices["buy"]) > 0 and len(babz_prices["sell"]) > 0 and len(baba_prices["buy"]) > 0 and len(baba_prices["sell"]) > 0:
		babz_buy_price = babz_prices["buy"][0][0]
		babz_buy_size = babz_prices["buy"][0][1]

		babz_sell_price = babz_prices["sell"][0][0]
		babz_sell_size = babz_prices["sell"][0][1]

		baba_buy_price = baba_prices["buy"][0][0]
		baba_buy_size = baba_prices["buy"][0][1]

		baba_sell_price = baba_prices["sell"][0][0]
		baba_sell_size = baba_prices["sell"][0][1]

		# if babz_sell_price + CONVERT_FEE < baba_sell_price:
		# 	return {"type": "add", "order_id": order_id, "symbol": "BABA", "dir": "BUY", "price": baba_sell_price, "size": baba_sell_size}

		# if babz_buy_price > baba_buy_price + CONVERT_FEE:
		# 	return {"type": "add", "order_id": order_id, "symbol": "BABA", "dir": "SELL", "price": baba_buy_price, "size": baba_buy_size}

		if babz_buy_price > baba_sell_price + CONVERT_FEE:

			toReturn.append({"type": "add", "order_id": order_id, "symbol": "BABA", "dir": "BUY", "price": baba_sell_price, "size": baba_sell_size})
			toReturn.append({"type": "convert", "order_id": order_id, "symbol": "BABA", "dir": "BUY", "size": baba_sell_size})
			toReturn.append({"type": "add", "order_id": order_id, "symbol": "BABZ", "dir": "SELL", "price": babz_buy_price, "size": baba_sell_size})

			return toReturn

def etf(xlk, bond, aapl, msft, goog, order_id, num_xlk, num_bonds):

	toReturn = []

	if len(xlk["buy"]) and len(xlk["sell"]) and len(bond["buy"]) and len(bond["sell"]) and len(aapl["buy"]) and len(aapl["sell"]) \
		and len(msft["buy"]) and len(msft["sell"]) and len(goog["buy"]) and len(goog["sell"]):

		xlk_buy_price = xlk["buy"][0][0]
		xlk_buy_size = xlk["buy"][0][1]

		xlk_sell_price = xlk["sell"][0][0]
		xlk_sell_size = xlk["sell"][0][1]

		bond_buy_price = bond["buy"][0][0]
		bond_buy_size = bond["buy"][0][1]

		bond_sell_price = bond["sell"][0][0]
		bond_sell_size = bond["sell"][0][1]

		aapl_buy_price = aapl["buy"][0][0]
		aapl_buy_size = aapl["buy"][0][1]

		aapl_sell_price = aapl["sell"][0][0]
		aapl_sell_size = aapl["sell"][0][1]

		msft_buy_price = msft["buy"][0][0]
		msft_buy_size = msft["buy"][0][1]

		msft_sell_price = msft["sell"][0][0]
		msft_sell_size = msft["sell"][0][1]

		goog_buy_price = goog["buy"][0][0]
		goog_buy_size = goog["buy"][0][1]

		goog_sell_price = goog["sell"][0][0]
		goog_sell_size = goog["sell"][0][1]

		# print("Parsed prices")

		xlk_fair_buy = ((3 * bond_buy_price) + (2 * aapl_buy_price) + (3 * msft_buy_price) + (2 * goog_buy_price))/10.0

		# print("Fair buy: ", xlk_fair_buy)
		# print("Sell price: ", xlk_sell_price)

		if xlk_fair_buy > xlk_sell_price:

			# print("ETF -> Stocks")
			print("Making transaction buy transaction")

			toReturn.append({"type": "add", "order_id": order_id, "symbol": "XLK", "dir": "BUY", "price": xlk_sell_price, "size": xlk_sell_size})

			toReturn.append({"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "SELL", "price": bond_buy_price, "size": xlk_sell_size*3})
			toReturn.append({"type": "add", "order_id": order_id, "symbol": "AAPL", "dir": "SELL", "price": aapl_buy_price, "size": xlk_sell_size*2})
			toReturn.append({"type": "add", "order_id": order_id, "symbol": "MSFT", "dir": "SELL", "price": msft_buy_price, "size": xlk_sell_size*3})
			toReturn.append({"type": "add", "order_id": order_id, "symbol": "GOOG", "dir": "SELL", "price": goog_buy_price, "size": xlk_sell_size*2})

		xlk_fair_sell = ((3 * bond_sell_price) + (2 * aapl_sell_price) + (3 * msft_sell_price) + (2 * goog_sell_price))/10.0

		# print("Fair sell: ", xlk_fair_sell)
		# print("Buy price: ", xlk_buy_price)

		if xlk_fair_sell < xlk_buy_price:

			print("Making sell transaction")

			toReturn.append({"type": "add", "order_id": order_id, "symbol": "AAPL", "dir": "BUY", "price": aapl_sell_price, "size": aapl_sell_size})
			toReturn.append({"type": "add", "order_id": order_id, "symbol": "MSFT", "dir": "BUY", "price": msft_sell_price, "size": msft_sell_size})
			toReturn.append({"type": "add", "order_id": order_id, "symbol": "GOOG", "dir": "BUY", "price": goog_sell_price, "size": goog_sell_size})

			toReturn.append({"type": "add", "order_id": order_id, "symbol": "XLK", "dir": "SELL", "price": xlk_buy_price, "size": xlk_buy_size})

		if num_xlk > 50:
			toReturn.append({"type": "convert", "order_id": order_id, "symbol": "XLK", "dir": "SELL", "size": num_xlk})

		if num_bonds > 50:
			toReturn.append({"type": "convert", "order_id": order_id, "symbol": "XLK", "dir": "BUY", "size": num_bonds})
					
		return toReturn
