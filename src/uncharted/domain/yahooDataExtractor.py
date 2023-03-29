import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from typing import TypeVar, Iterable, Tuple, Dict, List



class YahooDataExtractor:
    def __init__(self, tickers:List[str],
                 start_period:str,
                 end_period:str):
        """__init__
        Description
        -----------
        This class extract equities historical time series for defined scope of stocks and provide basic statistics of time series.


        Parameters
        ----------
        tickers : List[str]
            names of stocks 
        """

        self._tickers = tickers
        self._start_period=start_period
        self._end_period=end_period

        self.close_prices_df=self.extract_data(tickers=self._tickers,
                                               start_period=self._start_period,
                                               end_period=self._end_period)

    def extract_data(self,
                    tickers,
                    start_period,
                    end_period,
                    column_name="Close"):
        """extract_data
        Description
        -----------
        This function retrieves close price of equities for defined scope of trades.


        Parameters
        ----------
        tickers : list of strings
            Tickers available on Yahoo Finance
        start_period : string (Year-Month-Day)
            beginning of the period
        end_period : string (Year-Month-Day)
            _description_
        column_name : str, optional
             by default "Close"

        Returns
        -------
        pandas.DataFrame
        
        Examples
        --------
        >>> extract_data(tickers=["AAPL",
        >>>                      "BA",
        >>>                      "KO",
        >>>                      "IBM",
        >>>                      "DIS",
        >>>                      "MSFT"],
        >>>                      start_period="2010-01-01",
        >>>                      end_period="2022-10-30")    
        """

        df_equities = yf.download(tickers=tickers,
                                  start=start_period,
                                  end=end_period)
        df_equities.swaplevel(axis=1).sort_index(axis=1)
        one_column_ts = df_equities.loc[:, column_name].copy()
        return one_column_ts

    def dfInfo(self, df):
        print(df.describe())

    def normalize(self, df):
        norm = df.div(df.iloc[0]).mul(100)
        return norm

    def basicStatistic(self, df):

        print(df.info())

