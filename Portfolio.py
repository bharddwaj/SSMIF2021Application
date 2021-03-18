import pandas as pd
import numpy as np
import pandas_datareader as pdr
from datetime import datetime
import time

class Portfolio():

    def __init__(self,basket,start_date,end_date, benchmark):
        """
            Constructor

            parameters:
                basket: Dictionary with keys: type: String for Stock Ticker and values: int for num shares
                start_date: datetime
                end_date: datetime that must be greater than start_date
                benchmark: ticker name for the portfolio benchmark type: String

            Implementation:
                Save the parameters to instance variables. Then queries data from yahoo finance using the pandas_datareader.
                Next computes the portfolio_prices by scaling each stock price by num shares (using broadcasting) and adding these stock_prices
                together using numpy row sum (denoted by axis = 1).


        """
        self.__basket = basket

        if start_date > end_date:
            raise ValueError(f"start_date: {start_date} cannot be greater than end_date: {end_date}")


        self.benchmark = benchmark

        # appending returns and prices for each stock to the stock_returns list
        self.start_date_string =  start_date.strftime("%m/%d/%Y")
        self.end_date_string =  end_date.strftime("%m/%d/%Y")

        self.closing_prices = pdr.get_data_yahoo(list(self.__basket.keys()), start = self.start_date_string, end = self.end_date_string)["Adj Close"]


        self.portfolio_prices = np.sum(np.asfarray(list(self.__basket.values())).reshape(1,-1)*self.closing_prices,axis = 1)
        self.portfolio_returns = self.portfolio_prices.pct_change()[1:].to_numpy(dtype = 'float')
        self.portfolio_prices = self.portfolio_prices.to_numpy()

        self.benchmark_returns = pdr.get_data_yahoo(benchmark, start = self.start_date_string, \
                                    end = self.end_date_string)["Adj Close"].pct_change()[1:].to_numpy(dtype = 'float')

    def averageDailyReturn(self):
        """

            Returns the average daily percent return of the portfolio as a float

            Implementation:
                uses numpy to calculate the mean of the portfolio_returns

        """
        return np.mean(self.portfolio_returns)

    def volatility(self):
        """

            Returns the portfolio’s volatility over the lifespan of the portfolio

            Implementation:
                uses numpy to calculate the standard deviation of the portfolio_returns
        """

        return np.std(self.portfolio_returns)



    def riskRatio(self):
        """
            Returns the volatility ratio of the portfolio compared to the volatility of the benchmark over the lifetime of the portfolio.

            Implementation:
                Divide portfolio volatility by the standard deviation of the chosen benchmark
        """
        return self.volatility()/np.std(self.benchmark_returns)

    def marginalVolatility(self,tickr: str, shares: int) -> float:
        """
            Returns the difference in volatility of the portfolio if one were to add the specified number of shares of the ticker passed into the method.

            *NOTE* function returns current volatility - hypothetical. If negative that means vol has increased and if positive it has decreased. I did not want to return
            abs(current volatility - hypothetical), because the lack of the sign does not give us this information.

            Implementation:
                Case 1:
                    If the tickr is in the basket already, then the function simply adds the number of shares to its corresponding value. Then it computes the hypothetical
                    portfolio prices and returns the same way it did in the constructor.
                Case 2:
                    If the tickr is not in the basket, then the function initializes 2 lists. One list of tickers and one list of corresponding number shares. The function then
                    queries data from yahoo_finance using pandas_datareader and computes the portfolio prices and returns as done in constructor

        """
        if tickr in self.__basket.keys():
            self.__basket[tickr] += shares
            hypothetical_portfolio_prices = np.sum(np.asfarray(list(self.__basket.values())).reshape(1,-1)*self.closing_prices,axis = 1)
            hypothetical_portfolio_returns = hypothetical_portfolio_prices.pct_change()[1:].to_numpy(dtype = 'float')
            hypothetical_volatility = np.std(hypothetical_portfolio_returns)
            self.__basket[tickr] -= shares #subtract those hypothetical shares
            return self.volatility() - hypothetical_volatility
        else:

            tickers = list(self.__basket.keys())
            tickers.append(tickr)
            num_shares = list(self.__basket.values())
            num_shares.append(shares)
            closing_prices = pdr.get_data_yahoo(tickers, start = self.start_date_string, end = self.end_date_string)["Adj Close"]
            hypothetical_portfolio_prices = np.sum(np.asfarray(num_shares).reshape(1,-1)*closing_prices,axis = 1)
            hypothetical_portfolio_returns = hypothetical_portfolio_prices.pct_change()[1:].to_numpy(dtype = 'float')
            hypothetical_volatility = np.std(hypothetical_portfolio_returns)

            return self.volatility() - hypothetical_volatility


    def maxDrawDown(self):
        """
            Returns the maximum drawdown of your portfolio (the largest drop from peak to trough in the lifespan of your portfolio).
            If there are multiple, returns the largest drop

            Implementation:
                Iterates through the portfolio_prices. checks if a price is a peak and changes peak value accordingly. Then computes
                drawdown and checks if drawdown is less than the maxdrawdown. If so, change the maxdrawdown, otherwise continue.
        """

        maxdrawdown = 0
        peak = self.portfolio_prices[0]
        for price in self.portfolio_prices:
            if price > peak:
                peak = price
            drawdown = price/peak-1
            if drawdown < maxdrawdown: #the most negative drawdown is the maximum
                maxdrawdown = drawdown
        return maxdrawdown

# if __name__ == "__main__":
    # basket = {"AAPL": 50, "GME": 150, "TSLA": 5, "AAL": 200, "AMZN": 1, "GOOGL": 20, "AAPL": 15}
    # basket2 = {"AMZN": 1, "GOOGL":2, "IDXX":2, "ILMN":2, "ISRG":2, "LRCX": 2, "MLM":2, "MTD":2, "MHK":2, "TMO":1, "PYPL":2}
    # basket3 = {"AAPL": 3,"AMZN": 1}
    # basket4 = {"AAPL": 3,"AMZN": 4}
    # test= {"AAPL": 50, "GME": 150, "TSLA": 5, "AAL": 200, "AMZN": 1}
    # start =  datetime.fromisoformat('2016-01-01')
    # end =  datetime.fromisoformat('2017-12-31')
    # benchmark = "^GSPC"
    # begin = time.time()
    # portfolio = Portfolio(test,start,end, benchmark)
    #
    # print(f"Constructor time: {time.time() - begin}")
    # print(f"Avg Daily Return: {portfolio.averageDailyReturn()}")
    # print(f"Volatility: {portfolio.volatility()}")
    # print(f"Risk Ratio: {portfolio.riskRatio()}")
    # begin = time.time()
    # print(f"Marginal Volatility: {portfolio.marginalVolatility('AMZN',3)}")
    #
    # # print(time.time() - begin)
    # print(f"maxDrawDown: {portfolio.maxDrawDown()}")
