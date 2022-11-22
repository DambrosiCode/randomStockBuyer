from datetime import datetime as dt
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
        super().__init__()
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
            self.time_frame[0] = dt(time[0][0], time[0][2], time[0][2])
            self.time_frame[1] = dt(time[1][0], time[1][1], time[1][2])
            # set the first day of transactions
            self.first_day = self.time_frame[0]
        else:
            self.time_frame = [None, date]
            self.first_day = None


        # setup stockdata dict
        self.stock_data = dict()
        # read saved stock data
        self.readStockData()
        # download any newly instantiated stock data
        self.downloadStocksOwned(redown)
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
            stock_value = self.stock_data[stock]['Close'][date] * self.stocks_owned[stock]
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
                share_cost = self.stock_data[stocks_buying]['Open'].loc[purchaseDate]
                cost = shares_buying * share_cost
                joe.buyNewStock(stocks_buying, cost, shares_buying)
            except KeyError:
                pass
                #print('markets not opened today for: ' + stocks_buying)
        else:
            purchaseDate = self.getClosestDate(stocks_buying, purchaseDate)
            share_cost = self.stock_data[stocks_buying]['Open'].loc[purchaseDate]
            cost = shares_buying * share_cost
            joe.buyNewStock(stocks_buying, cost, shares_buying)

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
                share_cost = self.stock_data[stocks_selling]['Close'].loc[sell_date]
                cost = shares_selling * share_cost
                joe.sellNewStock(stocks_selling, cost, shares_selling)
            except KeyError:
                pass
                #print('markets not opened today for: ' + stocks_selling)
        else:
            sell_date = self.getClosestDate(stocks_selling, sell_date)
            share_cost = self.stock_data[stocks_selling]['Close'].loc[sell_date]
            cost = shares_selling * share_cost
            joe.buyNewStock(stocks_selling, cost, shares_selling)


    def getClosestDate(self, ticker, test_date):
        # get closest ddate to target date
        test_date_list = self.stock_data[ticker].index
        closest_time = min(test_date_list, key=lambda sub: abs(sub - test_date))
        return closest_time


def randStockBuyer(trader_class, iter):
    #randomly buy and sell stock for one month 100 times
    funds = []
    for i in tqdm(range(0,iter-1)):
        trader = Trader(1000, {'ABC': 0},
                     [[2020, 1, 3], [2022, 11, 21]])
        # start trader out with one stock: ABC, and no shares (0)
        # only buy shares between 2020 and today
        for day in range(0,30):
            #buy between 1 and 10 stocks randomly
            stocks_to_move = randint(1,10)
            buy_or_sell = randint(0,2)
            #if 0 then buy
            if buy_or_sell == 0:
                trader.buyShare('ABC', stocks_to_move, trader.first_day + timedelta(day))
            #if 1 then sell
            elif buy_or_sell == 1:
                trader.sellShare('ABC', stocks_to_move, trader.first_day + timedelta(day))
            #otherwise do nothing
            else:
                pass
        try:
            funds.append(trader.netWorth(trader.first_day + timedelta(day)))
        except:
            pass
    average_rand = numpy.mean(funds)
    start_price = trader.stock_data['ABC']['Open'][trader.first_day]
    end_price = trader.stock_data['ABC']['Close'][trader.first_day+timedelta(31)]
    print(average_rand/1000)
    print(end_price/start_price)
    print(average_rand)
    print(str(start_price) +' '+ str(end_price))



joe = Trader(1000, {'ABC': 0, 'AAPL': 0},
             [[2020, 1, 3], [2022, 11, 21]])

print(joe.stock_data['AAPL'])

#randStockBuyer(joe, 99)

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
