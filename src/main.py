from uncharted.domain.yahooDataExtractor import YahooDataExtractor

yahoo_data=YahooDataExtractor(tickers=['AAPL',
                                        "BA",
                                        "KO",
                                        "IBM",
                                        "DIS",
                                        "MSFT"],
                                        start_period="2010-01-01",
                                        end_period="2022-10-30")
yahoo_data.dfInfo(df=yahoo_data.close_prices_df)


