# import yfinance
#
# def get_stock_price(ticker):
#     return yfinance.Ticker(ticker).info['regularMarketPrice']
#
#
# def get_stock_name(ticker):
#     return yfinance.Ticker(ticker).info['shortName']
#
# def get_stock_info(ticker):
#     return yfinance.Ticker(ticker).info
#
# print(get_stock_info("AAPL"))

import pandas as pd
import yfinance as yf
import FinanceDataReader as fdr

df_krx = fdr.StockListing('KRX')
print(len(df_krx))

df_nasdaq = fdr.StockListing('NASDAQ')
print(len(df_nasdaq))

df = fdr.DataReader('AAPL', '2023-06-02', '2023-06-02')
print(df)

# 기본적으로 finance data reader가 빠른듯.
# 회사종류만 yfinance로 가져오고 나머지는 finance data reader로 가져오기