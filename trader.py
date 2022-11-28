from datetime import datetime
from datetime import timedelta, date

import numpy
import yfinance as yf
import pandas as pd
from random import randint
import matplotlib as plt
import pickle

from tqdm import tqdm
class Trader():
    def __init__(self, cash, stocks_owned, time_frame=None, redown=False):
        """params:
        cash(int) = cash on hand to buy stock
        stocks_owned(array) = ticker names of stocks currently owned
        time_frame(array) = timeframe of stock data, if null then all time
        stock_data(dict of dataframes) = dict of dataframes of owned stock open and closing prices"""

        self.cash = cash
        self.stocks_owned = stocks_owned
        self.time_frame = time_frame

        if time_frame is not None:
            time = time_frame
            self.time_frame[0] = datetime(time[0].year, time[0].month, time[0].day)
            self.time_frame[1] = datetime(time[1].year, time[1].month, time[1].day)
            # set the first day of transactions
            self.first_day = self.time_frame[0]
        else:
            self.time_frame = [None, date]
            self.first_day = None


        # setup stockdata dict
        self.stock_data = dict()
        # read saved stock data
        self.readStockData()
        #if there is new time data
        for stock in self.stocks_owned:
            if self.stock_data[stock].index[0] != self.first_day or stock not in self.stock_data.keys() or redown:
                # download any newly instantiated stock data
                self.downloadStocksOwned(True)

        # save stock data to text file
        self.writeStockData()


    def __str__(self):
        return "Cash: " + str(self.cash) + " " + str(self.stocks_owned)

    def writeStockData(self):
        # save stock data to text file
        with open("stock_data.txt", "wb") as myFile:
            pickle.dump(self.stock_data, myFile)

    def readStockData(self):
        # read saved stock data
        with open("stock_data.txt", "rb") as myFile:
            self.stock_data = pickle.load(myFile)

    def netWorth(self, date):
        netWorth = self.cash
        for stock in self.stocks_owned:
            stock_value = self.stock_data[stock]['Close'].loc[date] * self.stocks_owned[stock]
            netWorth = netWorth + stock_value
        return netWorth

    def downloadStocksOwned(self, redown=False):
        # download data for stocks owned
        for stock in self.stocks_owned.keys():
            if stock not in self.stock_data.keys() or redown:
                self.stock_data[stock] = yf.download(stock, progress=True,
                                                     start=self.time_frame[0],
                                                     end=self.time_frame[1])[['Open', 'Close']]
                #write newly donwloaded data
                self.writeStockData()

    def buyNewStock(self, symbol, cost, shares):
        #if cost is less than or equal to funds availible
        if cost > self.cash:
            #print("Can't buy more stocks than you have funds for")
            return None
        else:
            # buy new stock and then subtract the cost from cash
            if symbol not in self.stocks_owned:  # if there is no stock then create a new dict object with the shares bought
                self.stocks_owned[symbol] = shares
            else:  # otherwise add the new shares to shares
                self.stocks_owned[symbol] = self.stocks_owned[symbol] + shares

            # subtract spent cash
            self.cash = self.cash - cost
            self.downloadStocksOwned()

    def buyShare(self, stocks_buying, shares_buying, purchaseDate, date_exact=True):
        # buy shares at a given time at market value
        if date_exact:  # if true, will only buy stocks with date chosen is exact
            try:
                share_cost = self.stock_data[stocks_buying].loc[purchaseDate]['Open']
                cost = shares_buying * share_cost
                self.buyNewStock(stocks_buying, cost, shares_buying)
            except KeyError:
                pass
                #print('markets not opened today for: ' + stocks_buying)
                #print(purchaseDate)
        else:
            purchaseDate = self.getClosestDate(stocks_buying, purchaseDate)
            share_cost = self.stock_data[stocks_buying].loc[purchaseDate]['Open']
            cost = shares_buying * share_cost
            self.buyNewStock(stocks_buying, cost, shares_buying)

    def sellNewStock(self, symbol, cost, shares):
        #if selling more shares than owned
        if shares > self.stocks_owned[symbol]:
            #print("Can't sell more stocks than you own")
            return None
        else:
            # sell stocks owned
            self.stocks_owned[symbol] = self.stocks_owned[symbol] - shares

            # if all shares are sold remove stock from owned stocks
            #if self.stocks_owned[symbol] == 0:
            #    self.stocks_owned = self.stocks_owned.pop(symbol, None)

            # add money from sale
            self.cash = self.cash + cost


    def sellShare(self, stocks_selling, shares_selling, sell_date, date_exact=True):
        # buy shares at a given time at market value
        if date_exact:  # if true, will only buy stocks with date chosen is exact
            try:
                share_cost = self.stock_data[stocks_selling].loc[sell_date]['Close']
                cost = shares_selling * share_cost
                self.sellNewStock(stocks_selling, cost, shares_selling)
            except KeyError:
                pass
                #print('markets not opened today for: ' + stocks_selling)
        else:
            sell_date = self.getClosestDate(stocks_selling, sell_date)
            share_cost = self.stock_data[stocks_selling].loc[sell_date]['Close']
            cost = shares_selling * share_cost
            self.buyNewStock(stocks_selling, cost, shares_selling)


    def getClosestDate(self, ticker, test_date):
        # get closest ddate to target date
        test_date_list = self.stock_data[ticker].index
        closest_time = min(test_date_list, key=lambda sub: abs(sub - test_date))
        return closest_time

# buy one share of ABC at the market value of the first day the markets were opened in 2020
#joe.buyShare('ABC', 1, joe.first_day)
#print(joe)
# find the next day the markets were opened for ABC and buy a share on that day's open value
#next_day = joe.getClosestDate('ABC', joe.first_day) + timedelta(days=1)
#joe.buyShare('ABC', 1, next_day)
#print(joe)
# data = yf.download(tickers="MSFT",
#                   start=None,
#                   end=None)[['Open','Close']]
# print(data)
