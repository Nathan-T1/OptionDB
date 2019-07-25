import scipy.stats as ss
from decimal import Decimal
import math as m
import numpy as np
from datetime import date,timedelta
import requests
import json
import pandas as pd
import time
import datetime as dt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sqlalchemy import select, create_engine, MetaData, Table, Column, Integer, String
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import colors
from matplotlib import cm

def call_bsm (S0,K,r,T,Otype,sig):
        d1 = (np.log(S0 / K) + (r + 0.5 * sig ** 2) * T) / (sig * np.sqrt(T))
        d2 = (np.log(S0 / K) + (r - 0.5 * sig ** 2) * T) / (sig * np.sqrt(T))
        
        if (Otype == "Call"):
            price = (S0 * ss.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * ss.norm.cdf(d2, 0.0, 1.0))
            return (price)
        
        elif (Otype == "Put"):
            price = (K * np.exp(-r * T) * ss.norm.cdf(-d2, 0.0, 1.0) - S0 * ss.norm.cdf(-d1, 0.0, 1.0))
            return (price)
        
def vega (S0,K,r,T,sig):

    d1 = float(m.log(S0/K))/(sig*float(m.sqrt(T))) + float((r+ (sig*sig)/2)*T/(sig*float(m.sqrt(T))))
    vega = S0*float(ss.norm.pdf(np.float(d1)))*float(m.sqrt(T))
    return(vega)

def imp_vol(S0, K, T, r, market,flag):
        
    e = .00000001; x0 = float(1);   
    def newtons_method(S0, K, T, r, market,flag,x0, e):
        delta = call_bsm (S0,K,r,T,flag,x0) - market
        max_iter = 1
        
        while delta > e and max_iter <= 100:
            vega_data = vega (S0,K,r,T,x0)
            
            if vega_data <= .000000001:
                max_iter = max_iter+1
                return(0)
            else:
                x0 = float(x0 - (call_bsm (S0,K,r,T,flag,x0) - market)/vega_data)
                delta = abs(call_bsm (S0,K,r,T,flag,x0) - market)
                max_iter = max_iter+1
                
        return(float(x0))

    sig = newtons_method(S0, K, T, r, market,flag,x0 , e)   
    return(sig*100)

def get_dates(key,ticker):
    global dates 
    response = requests.get('https://sandbox.tradier.com/v1/markets/options/expirations',
    params={'symbol': ticker},
    headers={'Authorization': 'Bearer ' + key, 'Accept': 'application/json'})

    j = json.loads(response.text)

    dates = []
    for date in j['expirations']['date']:
        dates.append(date)
    return dates

def data(key,date,ticker,quote):           
    def Get_DTE(expiration_data):

        e_year = int(expiration_data[0:4])
        e_month = int(expiration_data[5:7])
        e_day = int(expiration_data[8:10])
        now = dt.datetime.now()
        year = int(now.year)
        month = int(now.month)
        day = int(now.day)

        now = dt.date(year,month,day)
        exp = dt.date(e_year,e_month,e_day)
        days_data = np.busday_count(now,exp)
        return days_data
    
    response = requests.get('https://sandbox.tradier.com/v1/markets/options/chains',
    params={'symbol': ticker, 'expiration': date},
    headers={'Authorization': 'Bearer ' + key, 'Accept': 'application/json'})

    j = json.loads(response.text)
   
    symbols = []
    last = []
    ask = []
    bid = []
    change = []
    expiration = []
    volume = []
    open_interest =[]
    strike = []
    DTE = []
    delta = []
    flag = []
    weighted_volume = []
    low = []
    high = []
    time = []
    Underlying = []
    iv = []
      
    for option in j['options']['option']:
        Underlying_data = quote       
        symbol = option['symbol']
        last_data = option['last']
        ask_data = option['ask']
        bid_data = option['bid']
        change_data =option['change']
        expiration_data = option['expiration_date']
        volume_data = option['volume']
        open_interest_data = option['open_interest']
        strike_data = option['strike']
        low_data = option['low']
        high_data = option['high']
        
        dte_data = Get_DTE(expiration_data)
        dte_float = float(dte_data)
        time_data = dt.datetime.now()

        

        if last_data is None:
            weighted_volume_data = 0
        elif last_data >= 0:
            if high_data is None or low_data is None:
                weighted_volume_data = float(last_data)*float(volume_data)*100
            else:
                scalar = float((high_data+low_data)/2)
                weighted_volume_data = float(scalar)*float(volume_data)*100
       

        if len(ticker) == 4:
            j = 10
        elif len(ticker) == 3:
            j = 9
        elif len(ticker) == 2:
            j = 8
        else:
            j = 7
            
        if symbol[j] == 'C':
            flag_data = "Call"
            flag.append(flag_data)
        else: 
            flag_data = 'Put'  
            flag.append(flag_data)

                
        T = dte_float + 1
        S0 = float(Underlying_data)
        K = float(strike_data)
        r = float(0.0225)
        market = float(ask_data)
        call_put = flag_data
        

        if market is not None:
            iv_data = imp_vol(S0, K, T/365, r, market,flag_data)

        else:
            iv_data = 0
        

        symbols.append(symbol)
        last.append(last_data)
        ask.append(ask_data)
        bid.append(bid_data)
        change.append(change_data)
        expiration.append(expiration_data)
        volume.append(volume_data)
        open_interest.append(open_interest_data)
        DTE.append(dte_data)
        strike.append(strike_data)
        weighted_volume.append(weighted_volume_data)
        low.append(low_data)
        high.append(high_data)
        time.append(time_data)
        Underlying.append(Underlying_data)
        iv.append(iv_data)
    
       
    data = pd.DataFrame()
    data['contract'] = symbols
    data['last']= last
    data['ask'] = ask
    data['bid'] = bid
    data['change'] = change
    data['expiration'] = expiration
    data['volume'] = volume
    data['open_interest'] = open_interest
    data['DTE'] = DTE
    data['strike'] = strike
    data['flag'] = flag
    data['weighted_volume'] = weighted_volume
    data['IV'] = iv
    data['time'] = time
    data['Ticker'] = Underlying
    
    call_df = pd.DataFrame(columns = data.columns)
    
    put_df = pd.DataFrame(columns = data.columns)
    for index, row in data.iterrows():

        if row['flag'] == 'Call':
            call_df.loc[len(call_df)] = row
        else:
            put_df.loc[len(put_df)] = row

    frame = [call_df, put_df]
    global df
    df = pd.concat(frame)

def get_quote(key,ticker):
        
    response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
    params={'symbols': ticker},
    headers={'Authorization': 'Bearer ' + key, 'Accept': 'application/json'})
    j = json.loads(response.text)

    global quote
    quote = j["quotes"]["quote"]["last"]
    return quote 
      
def Single_Pull(ticker, csv, sql):
    
    engine = create_engine('sqlite:///C:\\OptionDB\\MAIN.db', echo = True)
    conn = engine.connect()

    meta = MetaData(engine,reflect=True)
    dict_keys = meta.tables.keys()
    list_tables = list(dict_keys)
    
    table = meta.tables['User_Account']
    my_select = select([table])

    res = conn.execute(my_select)
    for row in res:
        key = str(row)
        key = key[2:]
        key = key[:-3]
        
        
    
    get_quote(key, ticker)
    get_dates(key, ticker)
    main_df = pd.DataFrame()
    for date in dates:
        print(date)
        data(key,date,ticker,quote)
        frames = [main_df, df]
        main_df = pd.concat(frames)
        
    print(main_df)
    
    if sql == 'yes':
        if ticker in list_tables:
            main_df.to_sql(ticker,engine, if_exists = 'append')
            
        else:
            main_df.to_sql(ticker,engine)
    else:
        print("Skip SQL update")
        
    if csv == 'yes':
        main_df.to_csv("Data.csv")
    else:
        print("Skip CSV export")
    
    
def Custom_Pull(tickers, expirations, strikes, csv, sql):
    
    engine = create_engine('sqlite:///C:\\OptionDB\\MAIN.db', echo = True)
    conn = engine.connect()

    meta = MetaData(engine,reflect=True) 
    table = meta.tables['User_Account']
    my_select = select([table])

    res = conn.execute(my_select)
    for row in res:
        key = str(row)
        key = key[2:]
        key = key[:-3]
        print(key)

    tickers = tickers.replace(' ','').split(',') 
    if expirations != "0":
        expirations = expirations.replace(' ','').split(',')
    else:
        expirations = get_dates(key, tickers[0])    
    if strikes != "0":
        strikes = strikes.replace(' ','').split(',')
    
    for ticker in tickers:
        csv_link = str(ticker) + ".csv"
        get_quote(key, ticker)
        main_df = pd.DataFrame()
        
        for date in expirations:
            print(date)
            data(key,date,ticker,quote)
            frames = [main_df, df]
            main_df = pd.concat(frames)

        if strikes != "0":
            for index,row in main_df.iterrows():
                strike = row['strike']
                
                if strike not in strikes:
                    
                    df.drop(index, inplace = True)
           
        print(main_df)
   
        if sql == 'yes':
            if ticker in list_tables:
                main_df.to_sql(ticker,engine, if_exists = 'append')
                
            else:
                main_df.to_sql(ticker,engine)
        else:
            print("Skip SQL update")
            
        if csv == 'yes':
            main_df.to_csv(csv_link)
        else:
            print("Skip CSV export")


def ExportDayPull(ticker, day):
    
    engine = create_engine('sqlite:///C:\\OptionDB\\MAIN.db')
    conn = engine.connect()

    meta = MetaData(engine,reflect=True)
    dict_keys = meta.tables.keys()
    list_tables = list(dict_keys)
    print(list_tables)
    
    df = pd.read_sql_table(str(ticker), engine)
    
    for index, row, in df.iterrows():
        string = str(row['time'])
        date = string[:10]
        if date != day:
            df.drop(index, inplace=True)
            
    string = str(ticker) + ".csv"
    df.to_csv(string)
    print("CSV exported to root directory")

def ExportCustomPull(ticker, days, strikes, expirations):

    if days != "0":
        days = days.replace(' ','').split(',')
        day_string = str(days)
        day_string = day_string[1:-1]
        day_string = '(' + day_string + ')'

    if strikes != "0":
        strikes = strikes.replace(' ','').split(',')
        strike_string = str(strikes)
        strike_string = strike_string[1:-1]
        strike_string = '(' + strike_string + ')'
        
    if expirations != "0":
        expirations = expirations.replace(' ','').split(',')
        expiration_string = str(expirations)
        expiration_string = expiration_string[1:-1]
        expiration_string = '(' + expiration_string + ')'
        
    engine = create_engine('sqlite:///C:\\OptionDB\\MAIN.db', echo = True)
    conn = engine.connect()

    if days == '0' and strikes == '0' and expirations == '0':
                                 
            statement = '''SELECT * FROM {}'''.format(ticker)
                         
    if days == '0' and strikes == '0' and expirations != '0':
                      
            statement = '''SELECT * FROM {} WHERE expiration IN {} '''.format(ticker, expiration_string)

    if days == '0' and strikes != '0' and expirations == '0':
                      
            statement = '''SELECT * FROM {} WHERE strike IN {} '''.format(ticker, strike_string)

    if days == '0' and strikes != '0' and expirations != '0':
                      
            statement = '''SELECT * FROM {} WHERE strike IN {} and
                        expiration IN {} '''.format(ticker, strike_string, expiration_string)

                
                        
                         
    df = pd.read_sql(statement, engine)


    string = str(ticker) + ".csv"
    df.to_csv(string)
    print("CSV exported to root directory")


def mesh(df,target,dates):

    global main_call_df
    global main_put_df
    main_call_df = pd.DataFrame()
    main_put_df = pd.DataFrame()

    for date in dates:
        call_date_df = pd.DataFrame()
        put_date_df = pd.DataFrame()
        
        calls_strikes = []
        puts_strikes = []

        calls_data = []
        puts_data = []
        
        for index, row in df.iterrows():
            
            if row['flag'] == 'Call':
                if row['expiration'] == date:
     
                    strike = row['strike']
                    data = row[target]
                    

                    calls_strikes.append(strike)
                    calls_data.append(data)
                        
            elif row['flag'] == 'Put':
                if row['expiration'] == date:
                    strike = row['strike']
                    data = row[target]

                    puts_strikes.append(strike)
                    puts_data.append(data)
                    
        call_date_df[date] = calls_strikes
        call_date_df[date+'Data'] = calls_data
        
        put_date_df[date] = puts_strikes
        put_date_df[date+'Data'] = puts_data

        main_call_df = pd.concat([main_call_df.reset_index(drop=True)
                                            , call_date_df.reset_index(drop=True)], axis=1)
        main_put_df = pd.concat([main_put_df.reset_index(drop=True)
                                            , put_date_df.reset_index(drop=True)], axis=1)
                         
def poly(inputs,outputs,df, target, min_strike, max_strike):
    lin = LinearRegression()
    y_df = pd.DataFrame()

    global lower_bound
    global upper_bound
    date = dates[0]
    lower_bound = min_strike
    upper_bound = max_strike


    new_strikes = np.arange(lower_bound,upper_bound,1)
    new_strikes = new_strikes[np.logical_not(np.isnan(new_strikes))]
    strikes = new_strikes.reshape(-1,1)


    n_rows = int(len(inputs))
    gap_df = pd.DataFrame(np.zeros((n_rows,1)))
    gap_df.index = inputs
    gap_df['Data'] = outputs
    

    del gap_df[0]
    data_list = []
    
    for strike in new_strikes:

        if strike in gap_df.index and target is not "IV":
            y = float(gap_df.loc[strike].sum())
            data_list.append(y)
        else:
            if target == 'IV':
                X = inputs[np.logical_not(np.isnan(inputs))]
                X = X.reshape(-1,1)
                Y = outputs[np.logical_not(np.isnan(outputs))]
                Y = Y.reshape(-1,1)

                poly = PolynomialFeatures(degree = 4)
                X_poly = poly.fit_transform(X)
                poly.fit(X_poly, Y)


                lin2 = LinearRegression() 
                lin2.fit(X_poly, Y)
                x = strike
                strike = x.reshape(-1,1)
                y = lin2.predict(poly.fit_transform(strike))
                y_float = y.astype(float)
                data_list.append(y_float)
            else:
                y_float = 0
                data_list.append(y_float)
            
    [float(i) for i in data_list]
    appended_data.append(data_list)

    
def plot3d(Otype, target, min_strike, max_strike, dates, csv):
    
    date_list = []
    for date in dates:
                         
        if Otype == 'Call':
                         
            print('Solving for ' + date)
            data = main_call_df[date+'Data'].values
            df = main_call_df
            poly(main_call_df[date].values,data,df, target, min_strike, max_strike)
        else:
                         
            data = main_put_df[date+'Data'].values
            print('Solving for ' + date)
            df = main_put_df
            poly(main_put_df[date].values,data,df, target, min_strike, max_strike)
            
        date_list.append(date)
    dte_list = []
                         
    for date in dates:
        e_year = int(date[0:4])
        e_month = int(date[5:7])
        e_day = int(date[8:10])

        now = dt.datetime.now()
        year = int(now.year)
        month = int(now.month)
        day = int(now.day)

        now = dt.date(year,month,day)
        exp = dt.date(e_year,e_month,e_day)
        days_data = int(np.busday_count(now,exp))
        dte_list.append(days_data)
        
    new_strikes = np.arange(lower_bound,upper_bound,1)
    new_strikes = new_strikes[np.logical_not(np.isnan(new_strikes))]
    df = pd.DataFrame(appended_data,columns=new_strikes)
    df = df.T
    df = df.astype(float)

    if target == 'IV':
            for column in df:
                lin = LinearRegression()
                y_df = pd.DataFrame()


                X = df.index.values
                X = X.reshape(-1,1)

                Y = df[column].values
                Y = Y.reshape(-1,1)

                pol = PolynomialFeatures(degree = 3)
                X_pol = pol.fit_transform(X)
                pol.fit(X_pol, Y)

                lin2 = LinearRegression() 
                lin2.fit(X_pol, Y)
                
                y = lin2.predict(pol.fit_transform(X))

                df[column] = y

    X,Y = np.meshgrid(df.columns.astype(float), df.index)
    
    df.columns = dates
    if csv == 'yes':
            df.to_csv('Mesh.csv')
    
    Z = df.values
    title = str(target + ' ' + str(Otype) + " " + str(target))
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z,cmap=cm.coolwarm,label = title, antialiased=True)
    
    ax.set_zlabel(target)
    ax.set_ylabel('Strike')
    ax.set_xlabel('Time')
    fig.set_title = (target + ' ' + str(Otype) + " " + str(target))

def Create_Mesh(ticker, day, target, csv, flag, min_strike, max_strike):
    global appended_data
    appended_data = []
    engine = create_engine('sqlite:///C:\\OptionDB\\MAIN.db', echo = True)
    conn = engine.connect()
    
    print('Gathering Data from sqlite:///C:\\OptionDB\\MAIN.db...')

    
    year = day[0:4]
    month = day[5:7]
    today = day[8:10]
    statement = '''SELECT * FROM {} WHERE strftime('%d', time) = '{}'
                AND strftime('%m', time) = '{}'
                AND strftime('%Y', time) = '{}' '''.format(ticker, today, month, year)
    df = pd.read_sql(statement, engine)
    
        
    


    meta = MetaData(engine,reflect=True)
    dict_keys = meta.tables.keys()
    list_tables = list(dict_keys)

    table = meta.tables['User_Account']
    my_select = select([table])

    
    res = conn.execute(my_select)
    for row in res:
        key = str(row)
        key = key[2:]
        key = key[:-3]
    get_dates(key, ticker)

    mesh(df, target, dates)
    plot3d(str(flag), target, int(min_strike), int(max_strike), dates, csv)
    plt.show()
    
    
