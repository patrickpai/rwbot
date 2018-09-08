import json

#BOOK BOND BUY 999:12 998:100 995:1 SELL 1001:4 1002:15 1003:100

CONVERT_FEE = 10
	
def etf_aggro(xlk, bond, aapl, msft, goog, order_id):

	toReturn = []

	if len(xlk["buy"]) and len(xlk["sell"]) and len(bond["buy"]) and len(bond["sell"]) and len(aapl["buy"]) and len(aapl["sell"]) \
		and len(msft["buy"]) and len(msft["sell"]) and len(goog["buy"]) and len(goog["sell"]):

		xlk_buy_price = xlk["buy"][0][0]
		xlk_buy_size = xlk["buy"][0][1]

		xlk_sell_price = xlk["sell"][0][0]
		xlk_sell_size = xlk["sell"][0][1]

		bond_buy_price = bond["buy"][0][0]

		bond_sell_price = bond["sell"][0][0]

		aapl_buy_price = aapl["buy"][0][0]

		aapl_sell_price = aapl["sell"][0][0]

		msft_buy_price = msft["buy"][0][0]

		msft_sell_price = msft["sell"][0][0]

		goog_buy_price = goog["buy"][0][0]

		goog_sell_price = goog["sell"][0][0]

		xlk_fair_buy = ((3 * bond_buy_price) + (2 * aapl_buy_price) + (3 * msft_buy_price) + (2 * goog_buy_price))/10

		#if xlk_buy_price < xlk_fair_buy - 1:
			
		toReturn.append({"type": "add", "order_id": order_id, "symbol": "XLK", "dir": "BUY", "price": xlk_buy_price+1, "size": xlk_buy_size})

			#return {"type": "add", "order_id": order_id, "symbol": "XLK", "dir": "BUY", "price": xlk_buy_price+1, "size": xlk_buy_size}
			
		# What we can buy XLK for if we buy XLK's underlying stocks
		xlk_fair_sell = ((3 * bond_sell_price) + (2 * aapl_sell_price) + (3 * msft_sell_price) + (2 * goog_sell_price))/10

		#if xlk_sell_price > xlk_fair_buy + 5:

		toReturn.append({"type": "add", "order_id": order_id, "symbol": "XLK", "dir": "SELL", "price": xlk_sell_price-1, "size": xlk_sell_size})

			#return {"type": "add", "order_id": order_id, "symbol": "XLK", "dir": "SELL", "price": xlk_sell_price-1, "size": xlk_sell_size}

		return toReturn
