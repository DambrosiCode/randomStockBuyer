import Trader

joe = Trader(1000, {'ABC': 0, 'AAPL': 0},
             [[2020, 1, 3], [2022, 11, 21]])

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