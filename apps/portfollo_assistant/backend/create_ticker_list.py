import pandas as pd
import yfinance as yf
import pykrx as stock
import FinanceDataReader as fdr


# The functions in this file should run every 1 Day or 1 Week

def get_krx_ticker_list():
    return fdr.StockListing('KRX')

def get_kospi_ticker_list():
    return fdr.StockListing('KOSPI')

def get_kosdaq_ticker_list():
    return fdr.StockListing('KOSDAQ')

def get_nasdaq_ticker_list():
    return fdr.StockListing('NASDAQ')

def get_nyse_ticker_list():
    return fdr.StockListing('NYSE')

def get_amex_ticker_list():
    return fdr.StockListing('AMEX')

def get_kor_company_names(fdr_ticker_list):
    print(fdr_ticker_list.columns)
    data = []
    for index,row in fdr_ticker_list.iterrows():
        if index % 100 == 0:
            print(index)
        ticker = row['Code']
        if row['Market'] == "KOSPI":
            ticker = ticker + ".KS"
            try:
                tmp_info = yf.ticker.Ticker(ticker).get_info()
                if tmp_info.get('sector') is None:
                    data.append('Etc')
                else:
                    data.append(tmp_info.get('sector'))
            except:
                data.append('Etc')
                continue
        else:
            #TODO : currently KOSDAQ and KONEX stock's section data not working
            data.append('Etc')

    company_names_and_symbols = fdr_ticker_list[['Name','Code']]
    company_names_and_symbols['Sector'] = data
    return company_names_and_symbols

def get_usa_company_names(fdr_ticker_list):
    print(fdr_ticker_list.columns)
    data = []
    for index,row in fdr_ticker_list.iterrows():
        if index % 100 == 0:
            print(index)
        ticker = row['Symbol']
        try:
            tmp_info = yf.ticker.Ticker(ticker).get_info()
            if tmp_info.get('sector') is None:
                data.append('Etc')
            else:
                data.append(tmp_info.get('sector'))
        except:
            data.append('Etc')
            continue
    company_names_and_symbols = fdr_ticker_list[['Name','Symbol']]
    company_names_and_symbols.rename(columns={'Symbol':'Code'}, inplace=True)
    company_names_and_symbols['Sector'] = data
    return company_names_and_symbols
def save_kor_ticker_list_to_csv():
    company_names = get_kor_company_names(get_krx_ticker_list())
    company_names.to_csv("../resources/kor_ticker_list.csv")

def save_usa_ticker_list_to_csv():
    nasdaq_company_names = get_usa_company_names(get_nasdaq_ticker_list())
    nyse_company_names = get_usa_company_names(get_nyse_ticker_list())
    company_names = pd.concat([nasdaq_company_names, nyse_company_names])
    company_names.to_csv("../resources/usa_ticker_list.csv")


# main function
if __name__ == "__main__":
    print("Generate Stock base data files for Korea and USA")
    save_kor_ticker_list_to_csv()
    save_usa_ticker_list_to_csv() # TODO : Takes 40 minutes , execution time should be reduced
