import pandas as pd
import numpy as np
import pandas_datareader as pdr
from datetime import datetime
import time

class Portfolio():
    
    def __init__(self,basket,start_date,end_date, benchmark):
        """
            Constructor
            
            paramters:
                basket: Dictionary with keys: type: String for Stock Ticker and values: int for num shares
                start_date: datetime
                end_date: datetime that must be greater than start_date
                benchmark: ticker name for the portfolio benchmark type: String
        """
        self.__basket = basket
        
        if start_date > end_date:
            raise ValueError(f"start_date: {start_date} cannot be greater than end_date: {end_date}")
        
        self.start_date = start_date
        self.end_date = end_date
        self.benchmark = benchmark
        self.total_stocks = sum(basket.values())
        self.weights = np.asfarray(list(map(lambda x: x/self.total_stocks,list(basket.values()))))
        self.stock_returns = []
        # appending returns for each stock to the stock_returns list
        start_date_string =  self.start_date.strftime("%m/%d/%Y")
        end_date_string =  self.end_date.strftime("%m/%d/%Y")
        for stock in basket.keys():
            stock_prices = pdr.get_data_yahoo(stock, start = start_date_string, end = end_date_string)
            self.stock_returns.append(stock_prices["Adj Close"].pct_change()[1:].to_numpy(dtype = 'float')) #the first element is NaN so no point in appending that
#            print(type(stock_prices["Adj Close"].pct_change())) #type pandas.core.series
        self.stock_returns = np.array(self.stock_returns, dtype=object)
        self.benchmark_returns = pdr.get_data_yahoo(benchmark, start = start_date_string, \
                                    end = end_date_string)["Adj Close"].pct_change()[1:].to_numpy(dtype = 'float')
        
    def averageDailyReturn(self):
        """
            
            Returns the average daily percent return of the portfolio as a float
            
            We first calculate the mean of each stock return series in the for loop and multiply the weights
            to the corresponding stock means. Then we sum up these values to get the average daily return.
            (Note: the multiplication and summation is done using dot product with one function call)
            
        """
#        print(len(self.__basket)) #checking to see if this shows the number of keys
        average_daily_returns = np.zeros(len(self.__basket))
        for z in range(self.stock_returns.shape[0]):
            average_daily_returns[z] = np.mean(self.stock_returns[z])
            
        return np.dot(self.weights, average_daily_returns)
        
    def volatility(self):
        """
            
            Returns the portfolio’s volatility over the lifespan of the portfolio
            
            Implementation:
                element wise multiplication first by using python multiplication b/w self.weights and self.stock_returns.T
                this multiplies each stock returns series with the corresponding portfolio weight
                then we do a row sum which gives us portfolio weighted daily return for each row
                lastly we calculate the standard deviation of this weighted daily return series
        """
      
#        begin = time.time()
#        diag_weight_matrix = np.diag(self.weights)
#        scaled_stock_returns = np.dot(self.stock_returns.T.reshape(-1,self.weights.shape[0]),diag_weight_matrix)
#        matrix_mult_answer = np.std(np.sum(scaled_stock_returns, axis = 0))
#        end = time.time()
#        print(end-begin)
#        begin = time.time()
#        broadcasting_answer = np.std(np.sum(self.weights*self.stock_returns.T, axis = 0))
#        end = time.time()
#        print(end - begin)
        return np.std(np.sum(self.weights*self.stock_returns.T, axis = 0))
        
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
            
        """
        num_stocks = self.total_stocks*self.weights #Python broadcasting
        tickr_index = list(self.__basket.keys()).index(tickr) #self.weights is in the same order as the keys
        num_stocks[tickr_index] += shares
        new_total_shares = self.total_stocks + shares
        new_weights = np.asfarray(list(map(lambda x: x/new_total_shares,num_stocks)))
        return self.volatility() - np.std(np.sum(new_weights*self.stock_returns.T, axis = 0))
        
    
    def maxDrawDown(self):
        """
            Returns the maximum drawdown of your portfolio (the largest drop from peak to trough in the lifespan of your portfolio).
            If there are multiple, returns the largest drop
        """
        portfolio_returns = np.sum(self.weights*self.stock_returns.T, axis = 0)
        drawdowns = [portfolio_returns[0]]
        for z in range(1,portfolio_returns.shape[0]):
            drawdowns.append(portfolio_returns[z] + drawdowns[z-1])
        
        return min(drawdowns)
        
        

if __name__ == "__main__":
    basket = {"AAPL": 50, "GME": 150, "TSLA": 5, "AAL": 200, "AMZN": 1, "GOOGL": 20, "AAPL": 15}
    basket2 = {"AMZN": 1, "GOOGL":2, "IDXX":2, "ILMN":2, "ISRG":2, "LRCX": 2, "MLM":2, "MTD":2, "MHK":2, "TMO":1, "PYPL":2}
    start =  datetime.fromisoformat('2020-03-09')
    end =  datetime.fromisoformat('2021-03-05')
    benchmark = "^GSPC"
    begin = time.time()
    portfolio = Portfolio(basket2,start,end, benchmark)
    print(f"Constructor time: {time.time() - begin}")
    print(f"Weights: {portfolio.weights}")
#    print(portfolio.stock_returns)
#    print(portfolio.averageDailyReturn())
    print(f"Volatility: {portfolio.volatility()}")
    print(f"Risk Ratio: {portfolio.riskRatio()}")
    print(f"Marginal Volatility: {portfolio.marginalVolatility('AMZN',2)}")
    print(f"maxDrawDown: {portfolio.maxDrawDown()}")
        
