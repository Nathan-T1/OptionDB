from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
import sys
import pandas as pd

def InitDB():
        engine = create_engine('sqlite:///C:\\OptionDB\\MAIN.db', echo = True)
        Base = declarative_base()
        Base.metadata.create_all(engine)
def InitArchive():
        engine = create_engine('sqlite:///C:\\OptionDB\\ARCHIVE.db', echo = True)
        Base = declarative_base()
        Base.metadata.create_all(engine)
        
def Add_Tradier(key):
        from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
        engine = create_engine('sqlite:///C:\\OptionDB\\MAIN.db', echo = True)
        meta = MetaData()
        User_Account = Table(
           'User_Account', meta, 
           Column('Key', String, primary_key = True), 
        )
        meta.create_all(engine)

        ins = User_Account.insert().values(Key = key)
        conn = engine.connect()
        result = conn.execute(ins)
                
        
        

