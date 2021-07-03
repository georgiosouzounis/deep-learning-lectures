#
# NASDAQ stock data
# by Georgios Ouzounis, June 2021
#

# import the relevant libraries
import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import io

# get the companies listed in NASDAQ
def getStockTickerSymbols():
	# access the URL containing a CSV file with the company names and 
	# their stock symbol listed on NASDAQ, and convert it to a pandas dataframe.
	url="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
	s = requests.get(url).content
	companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
	return companies

def searchBySymbol(companies, symbol):
	newdf = companies.loc[companies['Symbol'] == symbol]
	if newdf.empty:
		print("Symbol not found in NASDAQ")
	return newdf

def getStockPriceHistory(companies, start_date, end_date):
	# create empty dataframe
	stock_final = pd.DataFrame()
	# check for empty input dataframe
	if companies.empty:
		print("invalid company list")
		return stock_final
	# get the symbols of the listed companies in a list
	Symbols = companies['Symbol'].tolist()
	# iterate over the symbols list
	for i in Symbols:  
		# print the symbol which is being downloaded
		print( str(Symbols.index(i)) + str(' : ') + i, sep=',', end=',', flush=True)  
		try:
			# download the stock price 
			stock = []
			stock = yf.download(i, start=start_date, end=end_date, progress=False)
			# append the individual stock prices 
			if len(stock) == 0:
				None
			else:
				stock['Name']=i
				stock_final = stock_final.append(stock, sort=False)
		except Exception:
			None
	return stock_final

def getDateTime(year, month, day):
	return datetime.datetime(year, month, day)
	