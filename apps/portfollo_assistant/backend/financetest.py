import FinanceDataReader as fdr

def getKrx():
    df_krx = fdr.StockListing('KRX')
    return df_krx

def getKosdaq():
    df_kosdaq = fdr.StockListing('KOSDAQ')
    return df_kosdaq

def getNasdaq():
    df_us = fdr.StockListing('NASDAQ')
    return df_us

def getDow():
    df_us = fdr.StockListing('DOW')
    return df_us

def getSP500():
    df_us = fdr.StockListing('S&P500')
    return df_us

def getAmerica():
    df_us = fdr.StockListing('AMEX')
    return df_us
