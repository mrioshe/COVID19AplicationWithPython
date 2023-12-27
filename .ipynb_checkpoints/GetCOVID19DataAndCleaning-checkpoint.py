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

startDate=datetime(2020,1,3).date()
#we have to ensure that you have data on the final date, that is why the current date is not taken but 10 days before:
finalDate=datetime.today().date()-timedelta(days=10) 
# The datetime type data is taken to the Y-m-d form
listDate=[(startDate+timedelta(days=d)).strftime("%Y-%m-%d") for d in range((finalDate-startDate).days +1)]

def numercialDiff(list):
    DiffList=np.zeros(len(list))
    h=1 #constant step

    for i in range(len(list)):
        if i<=1:
            # Forward numerical difference
            DiffList[i] = (-list[i+2]+4*list[i+1]-3*list[i])/2*h
        elif i>= (len(list)-2):
            # Backward numerical difference
            DiffList[i]=(3*list[i]-4*list[i-1]+list[i-2])/2*h
        else:
            # Centered numerical difference
            DiffList[i]=(-list[i+2]+8*list[i+1]-8*list[i-1]+list[i-2])/12*h
    return(DiffList)

# Function to get df with determinated country info 