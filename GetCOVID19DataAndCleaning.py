import pandas as pd
import numpy as np

url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
df_DATA = pd.read_csv(url,index_col=0)

df_DATA.to_csv("UpdataCOVID19Data.csv",index=False)