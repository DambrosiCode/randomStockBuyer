from trader import Trader
from tqdm import tqdm
from random import randint
from datetime import timedelta, datetime
import numpy
import copy

def randStockBuyer(starting_funds, starting_stocks, date_range, iter, min_stock_move, max_stock_move, days_run=30):
    #randomly buy and sell stock for one month 100 times
    funds = []
    for i in tqdm(range(0,iter-1)):
        stocks = starting_stocks.copy() #copy the starting amount of stocks again
        trader = Trader(starting_funds,
                        stocks,
                        date_range,
                        redown=False)
        print(stocks)
        # start trader out with one stock: ABC, and no shares (0)
        # only buy shares between 2020 and today
        for day in range(0,days_run):

            #buy between 1 and 10 stocks randomly
            stocks_to_move = randint(min_stock_move,max_stock_move)
            buy_or_sell = randint(0,2)
            #if 0 then buy
            trader.buyShare(list(stocks.keys())[0], 1, trader.first_day + timedelta(day))
            if buy_or_sell == 0:
                trader.buyShare(list(stocks.keys())[0], stocks_to_move, trader.first_day + timedelta(day))
            #if 1 then sell
            elif buy_or_sell == 1:
                trader.sellShare(list(stocks.keys())[0], stocks_to_move, trader.first_day + timedelta(day))
            #otherwise do nothing
            else:
                pass
        funds.append(trader.netWorth(trader.getClosestDate(list(stocks.keys())[0],
                                                           trader.first_day  + timedelta(days_run))))

    average_rand = numpy.mean(funds)
    start_price = trader.stock_data[list(stocks.keys())[0]]['Open'].loc[trader.getClosestDate(list(stocks.keys())[0],trader.first_day)]
    end_price =   trader.stock_data[list(stocks.keys())[0]]['Close'].loc[trader.getClosestDate(list(stocks.keys())[0],trader.first_day+timedelta(days_run))]
    print(average_rand/starting_funds)
    print(end_price/start_price)
    print('---')
    print(average_rand)
    print(str(start_price) +' '+ str(end_price))
#
randStockBuyer(starting_funds=1000,
                       starting_stocks={'ABC':0},
                       date_range=[datetime(2020, 1, 3), datetime(2022, 11, 21)],
                       iter=9,
                       min_stock_move=1,
                       max_stock_move=10,
                       days_run=30)



import matplotlib.pyplot as plt
#plt.hist(funds)
#plt.show()
