import pandas as pd
import numpy as np
from datetime import datetime, timedelta

#Get COVID DATA from Our World Data and save it like dataframe:
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
df_DATA = pd.read_csv(url,index_col=0)
df_DATA.to_csv("data/UpdataCOVID19Data.csv",index=False)

#Read ISO CODES and give a format:
df_ISOCodes=pd.DataFrame(columns=['Country names'],index=pd.read_excel("data/country_iso_code.xlsx")['ISO 3166-1 .1'])
df_ISOCodes['Country names']=list(pd.read_excel("data/country_iso_code.xlsx")['Country name'])

#Create a list with dates:

startDate=datetime(2020,1,3)
#we have to ensure that you have data on the final date, that is why the current date is not taken but 10 days before:
finalDate=datetime.today().date()-timedelta(days=10) 