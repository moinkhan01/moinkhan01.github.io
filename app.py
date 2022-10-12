# Module Imports
from flask import Flask, request, session, redirect, render_template, url_for
import json
from bson.objectid import ObjectId

# File Imports
from config import def_username, def_password, app_sec, webhook_pass
from database import *
from exchange_api import initiate_order
from symbols import symbols

# App Setup
app = Flask(__name__)
app.secret_key = app_sec

# user & pass

def_username = def_username
def_password = def_password


# Login Route
@app.route("/", methods = ["GET", "POST"])
def root_route():

    if request.method == "POST":

        req_data = request.form

        user_email = req_data.get("email")
        user_password = req_data.get("password")

        if user_email == def_username:
            if user_password == def_password:

                session['user'] = user_email

                return redirect(url_for("dashboard"))
            else:
                return render_template("./pages/login.html", flash_msg=[True, "Email or Password is wrong, Please try again"])
        else:      
            return render_template("./pages/login.html", flash_msg=[True, "Email or Password is wrong, Please try again"])

    return render_template("./pages/login.html", flash_msg=[False, ""])

# Dashboard Route
@app.route('/dashboard/', methods = ["GET", "POST"])
def dashboard():

    if "user" in session:

        if request.method == "POST":
            
            form_data = request.form

            bot_params = {

                'scrip_name' : form_data["scrip_name"],
                'amount' : form_data["qty"],
                'leverage' : form_data["leverage"],
                'timeframe' : form_data["timeframe"].upper(),
                "buy-type" : form_data["buy-type"],
                "process" : "stop" #stop, running

            }

            new_bot = db.bots.insert_one(bot_params)

            return redirect(url_for("bots"))

        return render_template("pages/dashboard.html", exchanges=[], usdt_pairs=symbols)

    return redirect(url_for("root_route"))

# Scrips route
@app.route('/bots/', methods = ["GET", "POST"])
def bots():

    if "user" in session:


        if request.method == "POST":
            
            form_data = request.form
            bot_id = form_data['scripID']
            bot_details = db.bots.find_one({"_id" : ObjectId(bot_id)})


            db.bots.delete_one({'_id' : ObjectId(form_data['scripID'])})
            return redirect(url_for("bots"))


        # scrip_list = fetch_table("scrip_list")

        bots = list(db.bots.find())

        return render_template("pages/bots.html", bots=bots)

    return redirect(url_for("root_route"))

# Setup Exchange
@app.route('/exchange/', methods = ["GET", "POST"])
def exchange():

    if "user" in session:

        if request.method == "POST":
            
            form_data = request.form

            exch_details = {
                "name" : form_data['name'],
                "api_key" : form_data['api_key'],
                "api_sec" : form_data['api_sec']
            }

            db.exchange.drop()
            db.exchange.insert_one(exch_details)

            return redirect(url_for("exchange"))

        exchange = list(db.exchange.find())

        exchange = exchange[0] if len(exchange) > 0 else []

        return render_template("pages/exchange.html", exchange=[len(exchange), exchange])

    return redirect(url_for("root_route"))

# Start/ Stop Bot
@app.route('/start_bot/', methods = ["POST"])
def start_bot():

    if "user" in session:

        form_data = request.form
        bot_id = form_data['botID']
        bot_details = db.bots.find_one({"_id" : ObjectId(bot_id)})

        if bot_details['process'] == "stop":

            # Start the new bot and update record
        
                updateRes = db.bots.update_one({
                        "_id" : ObjectId(bot_id)
                    }, {
                        "$set" : {"process" : "running"}
                    })

                return redirect(url_for("bots"))


        elif bot_details['process'] == "running":

            

            updateRes = db.bots.update_one({
                "_id" : ObjectId(bot_id)
            }, {
                "$set" : {"process" : "stop"}
            })

            return redirect(url_for("bots"))


    return redirect(url_for("root_route"))

# Scrips route
@app.route('/recent_orders/', methods = ["GET"])
def recent_orders():

    if "user" in session:

        orders = list(db.orders.find())

        return render_template("pages/orders.html", orders=orders)

    return redirect(url_for("root_route"))

# Webhook Route to recieve post requests
@app.route('/webhook/', methods = ["POST"])
def webhook():

    new_request = json.loads(request.data)

    print("New Request Recived --> ", new_request)

    if new_request["pass"] == webhook_pass:

        signal_side = new_request["alert"]["name"] 

        trade_side = "buy" if signal_side.upper() == "LONG" else "sell"
        symbol = (new_request["alert"]["symbol"]).upper()
        price = float(new_request["alert"]["price"])
        tf = new_request["alert"]["timeframe"].upper()


        initiate_order(trade_side, symbol, price, tf)

        return "Request Recived"

    else:
        print("Wrong Auth Key From Tradingview")
        return "Wrong Auth Code"




if __name__ == "__main__":

    # Strat Flask Server

    app.run(host='0.0.0.0')

    

    

    

    

    
    




