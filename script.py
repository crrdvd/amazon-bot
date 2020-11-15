import requests
import bs4
import pandas as pd
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import time
import logging

logging.basicConfig(filename="bot.log", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)

spreadsheet_url = "db.csv"

with open("MY_CHAT_ID", "r") as f:
	c_id = str(f.read())

HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

def start(update, context):
	context.bot.send_message(chat_id=c_id, text="BOT avviato. Inizio a controllare.")
	
	check(context)
	context.job_queue.run_repeating(check, interval=600, context=update.message.chat_id)
	
def stop(update, context):
	context.bot.send_message(chat_id=c_id, text="BOT fermato.")
	
	context.job_queue.stop()

def tracker(url, TrackingPrice):
    res = requests.get(url, headers = HEADERS)
    soup = bs4.BeautifulSoup(res.content, features="lxml")
    
    time.sleep(10)
    
    title = soup.find(id="productTitle").get_text().strip()
    amount = float(soup.find(id="priceblock_ourprice").get_text().replace("€","").replace("&nbsp;","").replace(",",".").strip())
    if amount <= float(TrackingPrice):
        return "Hai un'offerta per {0}.\n\nPrezzo: {1} €.\n\nLink:\n{2}".format(title, amount, url)
    else:
        return "Non hai nessuna offerta"

def check(context):
	
	df = pd.read_csv(spreadsheet_url)

	for i in range(0, len(df["URL"])):
		msg = tracker(df["URL"][i], df["TrackingPrice"][i])
		if msg != "Non hai nessuna offerta":
		    context.bot.send_message(chat_id=c_id, text=msg)
		    
def add_item(update, context):
	try:
		pn = str(context.args[0])
		price = int(context.args[1])
		
		df = pd.read_csv(spreadsheet_url)
		l = len(df["URL"])
		
		df.loc[l, ["URL"]] = "https://www.amazon.it/gp/product/" + pn
		df.loc[l, ["TrackingPrice"]] = price
		
		df.to_csv(spreadsheet_url, index=False)
		
	except (IndexError, ValueError):
		update.message.reply_text("Usage: /additem <amazon part number> <prezzo>")
		    
def debug_connection(update, context):
	msg = "Sto funzionando"
	context.bot.send_message(chat_id=c_id, text=msg)
	
def debug_tracking(update, context):
	df = pd.read_csv(spreadsheet_url)
	msg = tracker(df["URL"][0], 500)
	context.bot.send_message(chat_id=c_id, text=msg)

def help(update, context):
	msg = """
	/start
	Start the BOT
	
	/stop
	Stop the BOT
	
	/help
	This message
	
	/additem <amazon part number> <prezzo>
	To add a new item to the database 
	
	/debugconnection
	Check if the bot is still running
	
	/debugtracking
	Check if the scraping is running
	"""
	
	context.bot.send_message(chat_id=c_id, text=msg)

def main():
	u = Updater(token="1431872649:AAE0CmcJMDjQKA5PFDKlgkFfQ-_FP2hAxUg", use_context=True)
    
	u.dispatcher.add_handler(CommandHandler("start", start, pass_job_queue=True))
	u.dispatcher.add_handler(CommandHandler("stop", stop, pass_job_queue=True))
	u.dispatcher.add_handler(CommandHandler("help", help))
	u.dispatcher.add_handler(CommandHandler("debugconnection", debug_connection))
	u.dispatcher.add_handler(CommandHandler("debugtracking", debug_tracking))
	u.dispatcher.add_handler(CommandHandler("additem", add_item))

	u.start_polling()
	
	u.idle()
	
if __name__ == "__main__":
	main()
