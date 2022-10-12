
from currencycom.client import Client, OrderSide, OrderType
import time
from database import db

global exchange, api_key, api_sec


exchange_deatils = list(db.exchange.find())
exchange_deatils = exchange_deatils[0] if len(exchange_deatils) > 0 else {}

# fetch API keys
api_key = exchange_deatils['api_key'] if len(exchange_deatils) > 0 else ""
api_sec = exchange_deatils['api_sec'] if len(exchange_deatils) > 0 else ""

# Setting up Client
exchange  = Client(api_key, api_sec)

# To Fetch Balalnce of a COIN
def fetch_balance(coin):

    balances = exchange.get_account_info()['balances']

    for bal in balances:

        if bal["asset"] == coin.upper():

            fund = bal["free"]

            return fund

    else:

        return None

# To Place market Buy or Sell Order
def place_order(side, ticker, amount, price, lvg):

    order_side = OrderSide("BUY") if side.upper() == "BUY" else OrderSide("SELL")

    volume = round(amount / price, 4)

    order = exchange.new_order(ticker, order_side, OrderType("MARKET"), volume, leverage=lvg)

    db.orders.insert_one(order)

    return order

# To START the Order 
def initiate_order(trade_side, symbol, price, tf):

    bot = db.bots.find_one({"scrip_name" : symbol, "timeframe" : tf})

    print(bot)

    if bot != None:

        procsss  = bot["process"]
        
        if procsss.upper() != "STOP":

            buy_type = bot['buy-type']
            balance = None

            if buy_type.upper() == "PERCENT":

                base, quote = symbol.split("/")

                wal_bal = fetch_balance(quote)

                if not wal_bal == None:

                    balance = round(float(wal_bal) * (float(bot["amount"]) / 100), 4)

            else:
                balance = bot["amount"]

            
            leverage = bot["leverage"]

            place_order(trade_side, symbol, balance, price, leverage)


        else:

            print(f"Bot is offline for {symbol}")


    else:
        print(f"Not Bots running for {symbol}")


