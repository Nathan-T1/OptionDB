# -*- coding: utf-8 -*-
"""STORE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PwNGxCVSsLp6GAkkIzTcWIkvzo5gMMTA
"""

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries
import backtrader as bt
import itertools
import os
import time
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt
import datetime as dt

def main(db_path, key):

    def create_db(db_path):

        if os.path.exists(db_path):
       
            print("{} already exists".format(db_path))
            conn_string = "sqlite:///" + db_path

        else:
            conn_string = "sqlite:///" + db_path
            Base = declarative_base()

            engine = create_engine(conn_string, echo = False)
            Base.metadata.create_all(engine)

    def pull_data(api_key, extent, db_path):

        conn_string = "sqlite:///" + db_path
        engine = create_engine(conn_string, echo = False)
       
        tickers_df = pd.read_sql_table("Tickers", engine)
        tickers = tickers_df['Tickers'].values
        tickers = tickers.tolist()
        tickers.append("SPY")
        tickers.append("QQQ")
        tickers.append("IWM")
       
        for ticker in tickers:
           
            print(ticker)  

            df = pd.read_sql_table(ticker, engine)
            now = dt.datetime.now()
            current_day = int(now.day)
           
            last_timestamp = df['date'].iloc[-1]
            last_day = int(last_timestamp.day)
           
            if last_day == current_day:
                print("Table already up to date")
                a=1
               
            if last_day != current_day:
                time.sleep(10)
               
                try:
                   
                    ts = TimeSeries(key = api_key, output_format = 'pandas')
                    data, meta_data = ts.get_intraday(symbol = ticker, interval = '5min', outputsize = extent)

                except:
             
                    api_key = "Q3Y60U32XTGAR2N8"
                    ts = TimeSeries(key = api_key, output_format = 'pandas')
                    data, meta_data = ts.get_intraday(symbol = ticker, interval = '5min', outputsize = extent)
                   
                data.reset_index(inplace = True)
                   
                data['date'] = pd.to_datetime(data['date'],format = '%Y-%m-%d %H:%M:%S')
                data_time =  data['date'].iloc[-1]

                try:
                   
                    db_table = pd.read_sql_table(ticker.upper(), engine)
                    current_end =  db_table['date'].iloc[-1]
                       
                    data_date_range = (data['date'] > current_end)
                    data_insert = data.loc[data_date_range]

                    if data_insert.empty:
                        print("Table Already Updated... \n")

                    else:
                       
                        data_insert.to_sql(ticker, engine, if_exists = 'append')
                        print("Database Appended \n")

                except:
                   
                    print("Creating table... \n")
                    data.to_sql(ticker, engine, if_exists = 'append')
                    print("Table Created... \n")
               
   
         
       
         
    pull_data(key, "full", db_path)

if __name__ == "__main__":

    db_path = "C:\OptionDB\INTRA_DAY.db"
    key = "Alpha Vantage Key"

    main(db_path, key)