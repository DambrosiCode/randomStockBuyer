from datetime import datetime as dt
from datetime import timedelta
import yfinance as yf
import pandas as pd


class trader:
    def __init__(self, cash, stocks_owned, time_frame=None):
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
            self.time_frame = [None, None]
            self.first_day = None
        self.stock_data = dict()

        # download any instantiated stock data
        self.downloadStocksOwned()

    def __str__(self):
        return f"{self.cash, self.stocks_owned}"

    def downloadStocksOwned(self):
        # download data for stocks owned
        for stock in self.stocks_owned.keys():
            if stock not in self.stock_data.keys():
                self.stock_data[stock] = yf.download(stock,
                                                     start=self.time_frame[0],
                                                     end=self.time_frame[1])[['Open', 'Close']]

    def buyNewStock(self, symbol, cost, shares):
        # buy new stock and then subtract the cost from cash
        if symbol not in self.stocks_owned:  # if there is no stock then create a new dict object with the shares bought
            self.stocks_owned[symbol] = shares
        else:  # otherwise add the new shares to shares
            self.stocks_owned[symbol] = self.stocks_owned[symbol] + shares

        # subtract spent cash
        self.cash = self.cash - (cost * shares)
        self.downloadStocksOwned()

    def buyShare(self, stocks_buying, shares_buying, purchaseDate):
        # buy shares at a given time at market value
        purchaseDate = self.getClosestDate(stocks_buying, purchaseDate)
        share_cost = self.stock_data[stocks_buying]['Open'].loc[purchaseDate]

        cost = shares_buying * share_cost
        joe.buyNewStock(stocks_buying, cost, shares_buying)

    def getClosestDate(self, ticker, test_date):
        #get closest ddate to target date
        test_date_list = self.stock_data[ticker].index
        closest_time = min(test_date_list, key=lambda sub: abs(sub - test_date))
        return closest_time


joe = trader(1000, {'ABC': 0}, [[2020, 12, 10], [2020, 12, 20]])
joe.buyShare('ABC', 1, joe.first_day)
print(joe)
next_day = joe.getClosestDate('ABC', joe.first_day)+timedelta(days=1)
joe.buyShare('ABC', 1, next_day)
print(joe)
# data = yf.download(tickers="MSFT",
#                   start=None,
#                   end=None)[['Open','Close']]
# print(data)
