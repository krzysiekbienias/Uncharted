from uncharted.domain.yahooDataExtractor import YahooDataExtractor
from uncharted.toolkit.IOToolKit import XlWingsTools

import pandas as pd
import numpy as np
import xlwings as xw
from typing import TypeVar,Iterable,Tuple,Dict,List,Generic,NewType

HM=TypeVar("HM",bound=Dict)


class FinancialInstrument:
    def __init__(self,yahoo_data_handler:YahooDataExtractor,xw_book:xw.Book) -> None:
        """__init__ _summary_

        Parameters
        ----------
        yahoo_data_handler : YahooDataExtractor
            object where we store prices, as a data frame extracted from YahooFinance.
        xw_book : xw.Book
            Book object to present and store basic analysis for instrument chosen from the market.
        """

        self._yahoo_data_handler=yahoo_data_handler
        self._xw_book=xw_book

        close_prices=self._yahoo_data_handler.close_prices_df
        log_returns_df=self.get_log_returns(df_prices=close_prices)

        self.instruments_map=dict()
        
        for instrument in close_prices:
            print(f"We are calculating performance for {instrument}")
            price_and_returns_df=self.get_log_returns(df_prices=close_prices,instrument_name=instrument)
            self.instruments_map.update({instrument:price_and_returns_df})
        self.generateBasicReport(data_container=self.instruments_map,
                                 returns_df=log_returns_df)


    def normalize(self, df:pd.DataFrame)->pd.DataFrame:
        """normalize
        Description
        -----------
        Normalizing different data prices. Please note that that absolute prices are meaningless.
        This is because higher price does not imply a higher value.
        This performance is calculated for entire scope.

        Parameters
        ----------
        df : pd.DataFrame
            Raw data frame with absolute prices.

        Returns
        -------
        pd.DataFrame
            Data Frame with normalized prices
        """
        norm = df.div(df.iloc[0]).mul(100)
        return norm 

    def resample_price(self,
                       
                       df:pd.DataFrame,
                       asset_name:str,
                       freq:str="M",
                       rolling:str="last"):
        """resample_price
        Description
        -----------
        This function returns modified data frame according to new frequency and rolling convention.
        Possible frequency are :
        * 'D' - daily,
        * 'W' - weekly,
        * 'M' - monthly,
        * 'Q'- quarterly,
        * 'A' - annualy
        
        Rolling refers to the way how to chose date after sampling. We may take first value, last value or mean from chosen period. 

        Parameters
        ----------
        df : pd.DataFrame
            _description_
        asset_name : str
            _description_
        freq : str, optional
            _description_, by default "M"
        refer_to : str, optional
            _description_, by default "last"
        """
        if rolling=="last":
            return df.resample("freq").last()
        elif rolling=="first":
            return df.resample("freq").first()
        elif rolling=="mean":
            return df.resample("freq").mean()    
        
        


    def get_log_returns(self,
                        df_prices:pd.DataFrame,
                        instrument_name:str=None)->pd.DataFrame:
        """get_log_returns
        Description
        This method calculates log return rates for chosen instrument.

        Parameters
        ----------
        df_prices : pd.DataFrame
        Data Frame with close prices.
        
        facility_name : str
            name of instrument

        Returns
        -------
        pd.DataFrame
            Data Frame with price and risk returns
        """
        if instrument_name is None:
            log_returns_all=np.log(df_prices/df_prices.shift(1))
            return log_returns_all

        if instrument_name not in df_prices.columns:
            raise ValueError(f"There is no price available for instrument {instrument_name}")
        df_per_instrument=df_prices[[instrument_name]]
        
        df_per_instrument["log_returns"]=np.log(df_per_instrument/df_per_instrument.shift(1))
        return df_per_instrument


    def statisticOfRates(self,
                         df_rates:pd.DataFrame,
                         period:str='daily'):
        """statisticOfRates
        Description
        -----------
        This function calculates basic statistics of rates. It might be scale on annual values.

        Parameters
        ----------
        df_rates : pd.DataFrame data frame rates of return
        period : str, optional
            frequency for calculating mean and standard deviations , by default 'daily'

        Returns
        -------
        tuple
            Tuples of floats that represents mean, and standard deviation of interest rates. It might be expressed as daily or annually numbers.
        Note
        ----
        To express annual measures 252 days scaling factor is used.    
        Examples
        --------
        >>>     FinancialDataToolKid.statisticOfRates(df=data_frame_of_interest_rates,)
        >>>                                            period='daily'


        """

        if period == 'daily':
            mean_returns = df_rates.mean()
            var_returns = df_rates.var()
            st_dev_returns = np.sqrt(var_returns)
            return (mean_returns, st_dev_returns)
        elif period == 'annually':
            ann_mean_returns = df_rates.mean()*252
            st_dev_returns = np.sqrt(var_returns)
            ann_std_dev=st_dev_returns*np.sqrt(252)
            return (ann_mean_returns, ann_std_dev)

    def get_mean(self,instrument_name:str,freq:str=None):

        if freq is None:
            return self.get_log_returns(df_prices=self.close_prices,instrument_name=instrument_name).mean()
        else:
            rolled_price=self.resample_price(asset_name=instrument_name,freq="M",rolling="last")
            
            return np.log(rolled_price/rolled_price.shift(1)).mean()

    def covarianceMatrix(self,data_df):
        """covarianceMatrix 
        Description
        -----------
        This static method calculates data frame of covariance matrix of prices

        Parameters
        ----------
        data_df : data frame
            Data frame of closing price.

        Returns
        -------
        pd.DataFrame
            Covariance matrix obtained from equities.
        """
        return data_df.cov()    


        
    def correlationMatrix(self,data_df):
        """correlationMatrix
        Description
        -----------
        This static method calculates data frame of correlation matrix obtained from close prices of equities.

        Parameters
        ----------
        data_df : pd.DataFrame
            

        Returns
        -------
        pd.DataFrame
            correlation matrix between chosen financial instruments
        """
        return data_df.corr()


    def generateBasicReport(self,data_container:HM,
                            returns_df):
        instruments_summary=self._yahoo_data_handler.df_info(df=self._yahoo_data_handler.close_prices_df)
        covariance_matrix=self.correlationMatrix(data_df=returns_df)
        XlWingsTools.insertDF(xw_book=self._xw_book,
                            df=instruments_summary,
                            sheet_name="Summary",
                            anchor="A1")
        
        XlWingsTools.insertDF(xw_book=self._xw_book,
                                df=covariance_matrix,
                                sheet_name="Summary",
                                anchor="K1")
        for instrument in data_container.keys():
            XlWingsTools.insertDF(xw_book=self._xw_book,
                                  df=data_container[instrument],
                                  sheet_name=instrument,
                                  anchor="A1")
        self._xw_book.save()

        
        




        










        


        