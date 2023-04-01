from uncharted.domain.yahooDataExtractor import YahooDataExtractor
from uncharted.toolkit.IOToolKit import XlWingsTools
from uncharted.domain.basicFinancialAnalysis import FinancialInstrument

import os

# ------------------
# Region: User customization
# ------------------ 
working_directory="/Users/krzysiekbienias/Documents/GitHub"
output_directory="Uncharted/io"
report_file_name="basic_analysis.xlsx"

# -----------------------
# Region: Input Output location
# -----------------------
io_path=os.path.join(working_directory,output_directory)
if not os.path.isdir(io_path):
        raise ValueError("Path you chosen does not exists!")
# -----------------------
# Region: Input Output location
# -----------------------

instruments=['AAPL',
            "BA",
            "KO",
            "IBM",
            "DIS",
            "MSFT"]

# ---------------------
# Region: User customization
# ---------------------

report_book=XlWingsTools.createNewExcelFile(save_path=os.path.join(io_path,report_file_name),
                                sheet_names=instruments)
XlWingsTools.clearAllSpreadSheet(os.path.join(io_path,report_file_name))

        


print("File for presenting results has been prepared.")


yahoo_data=YahooDataExtractor(tickers=instruments,
                                        start_period="2010-01-01",
                                        end_period="2022-10-30")


basic_financial_analysis=FinancialInstrument(yahoo_data_handler=yahoo_data,
                                             xw_book=report_book
                                             )

print("THE END")





