from trader import Trader
from tqdm import tqdm
from random import randint
from datetime import timedelta, datetime
import numpy as np
import copy
import pandas as pd

ticker_list = pd.read_csv('nasdaq_ticker_list.csv')

#TODO: record stocks owned
#TODO: record networth

def randStockBuyer(starting_funds, starting_stocks, date_range, iter, min_stock_move, max_stock_move, days_run=30):
    funds = []

    #randomly buy and sell stock for one month 100 times
    if days_run == 'All':
        days_run = date_range[1]-date_range[0]
        days_run = days_run.days

    for i in tqdm(range(0,iter-1)):
        stocks = starting_stocks.copy() #copy the starting amount of stocks again
        trader = Trader(starting_funds,
                        stocks,
                        date_range,
                        redown=False)

        # start trader out with one stock: ABC, and no shares (0)
        # only buy shares between 2020 and today
        for day in range(0, days_run):
            current_day = trader.first_day + timedelta(days_run)

            #for each stocks owned decide what to do
            for stock in stocks:

                #buy/sell between n and m stocks randomly
                stocks_to_move = randint(min_stock_move, max_stock_move)

                #decide to buy, sell, or pass
                buy_or_sell = randint(0,2)

                #if 0 then buy
                trader.buyShare(stock, 1, trader.first_day + timedelta(day))

                if buy_or_sell == 0:
                    trader.buyShare(stock, stocks_to_move, trader.first_day + timedelta(day))
                #if 1 then sell
                elif buy_or_sell == 1:
                    trader.sellShare(stock, stocks_to_move, trader.first_day + timedelta(day))
                #otherwise do nothing
                else:
                    pass
        funds.append(trader.netWorth(trader.getClosestDate(list(stocks.keys())[0], current_day)))

    average_rand = np.mean(funds)

    start_price = []
    end_price = []
    for stock in stocks:
        start_price.append(trader.stock_data[stock]['Open'].loc[trader.getClosestDate(stock, trader.first_day)])
        end_price.append(trader.stock_data[stock]['Close'].loc[trader.getClosestDate(stock, current_day)])

    start_price_total = np.sum(start_price)
    end_price_total = np.sum(end_price)
    print("Percent Profit from Random Trading")
    print(average_rand/starting_funds)
    print('Percent Profit from Holding')
    print(end_price_total/start_price_total)
    print('---')
    print('Average Random Profit')
    print(average_rand)
    print("Start and End Average Holding")
    print(str(start_price_total) + ' ' + str(end_price_total))
    return funds
#


funds = randStockBuyer(starting_funds=1000,
                       starting_stocks={'ABC':0, 'AAPL':0},
                       date_range=[datetime(2007, 3, 30), datetime.today()],
                       iter=99,
                       min_stock_move=1,
                       max_stock_move=10,
                       days_run='All')



#import matplotlib.pyplot as plt
#plt.hist(funds)
#plt.show()
