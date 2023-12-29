def GETCOVID19DataAndCleaning():

    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    from scipy.signal import savgol_filter

    #Get COVID DATA from Our World Data and save it like dataframe:

    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
    df_DATA = pd.read_csv(url,index_col=0)
    df_DATA.to_csv("data/UpdataCOVID19Data.csv",index=False)

    #Read ISO CODES and give a format:

    df_ISOCodes=pd.DataFrame(columns=['Country names'],index=pd.read_excel("data/country_iso_code.xlsx")['ISO 3166-1 .1'])
    df_ISOCodes['Country names']=list(pd.read_excel("data/country_iso_code.xlsx")['Country name'])

    #Create a list with dates:

    startDate=datetime(2020,1,10).date()
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

    def getDataCountry(CountryName):
        totalCasesList=[]
        newCasesList=[]
        totalDeathsList=[]
        newDeathsList=[]

        for i in range(len(df_DATA)):
            if df_DATA['location'][i]==CountryName:
                    totalCasesList.append(df_DATA['total_cases'][i])
                    newCasesList.append(df_DATA['new_cases'][i])
                    totalDeathsList.append(df_DATA['total_deaths'][i])
                    newDeathsList.append(df_DATA['new_deaths'][i])

        df_country=pd.DataFrame(columns=('Date','TotalCases','NewCases','TotalDeaths','NewDeaths'))

        # Now the idea is to generate DataFrames with the same number of data (to avoid key errors in the graph)
        # the columns of the country's DF will be taken from date n (where the first record is) with the data
        # of the previous lists and the data prior to date n will be taken as 0 (cases, deaths, total cases, total deaths).

        n=len(listDate)-len(newCasesList)
        df_country['Date']=listDate.copy()

        for i in range(len(newCasesList)):
            df_country['TotalCases'][i+n]=totalCasesList[i]
            df_country['NewCases'][i+n]=newCasesList[i]
            df_country['TotalDeaths'][i+n]=totalDeathsList[i]
            df_country['NewDeaths'][i+n]=totalDeathsList[i]
        
        #Smoothing data and numerical diff data:
                
        df_country['NewCasesSmoothed']=savgol_filter(df_country['NewCases'],51,3)
        df_country['NewDeathsSmoothed']=savgol_filter(df_country['NewDeaths'],51,3)
        df_country['NewCasesRate']=numercialDiff(df_country['NewCasesSmoothed'])
        df_country['NewDeathsRate']=numercialDiff(df_country['NewDeathsSmoothed'])
        df_country['NewCasesRateSmoothed']=savgol_filter(df_country['NewCasesRate'],51,3)
        df_country['NewDeathsRateSmoothed']=savgol_filter(df_country['NewDeathsRate'],51,3)

        return(df_country)

    # Get df to every country:
    # A dictionary is generated that saves all the df of each country with the key equal to the ISO 3166-1 of the respective country.

    try:
        countryList=list(set(df_DATA['location']))
        countryList.remove('Lower middle income')
        countryList.remove('Upper middle income')
        countryList.remove('Low income')
        countryList.remove('High income')
        countryList.remove('World')
        countryList.remove('Europe')
        countryList.remove('Western Sahara')
        countryList.remove('Asia')
        countryList.remove('North America')
        countryList.remove('South America')
        countryList.remove('European Union')

        #countryList.remove('Africa')
        #countryList.remove('South America')
        #countryList.remove('Europe')
        #countryList.remove('Oceania')

    except:
        countryList=list(set(df_DATA['location']))

        
    dic_countriesDF={}

    # Here it takes a few seconds since there is high data processing:
    for i in countryList:
        dic_countriesDF[i]=getDataCountry(i)
        print(i," info was uploaded",  round(100*(countryList.index(i)+1)/len(countryList)), " %" )
        
    # Now summary dataframes will be created:
        
    summaryDeathsList=[]
    summaryCasesList=[]

    for i in dic_countriesDF:
        summaryCasesList.append(dic_countriesDF[i]['TotalCases'][len(listDate)-2])
        summaryDeathsList.append(dic_countriesDF[i]['TotalDeaths'][len(listDate)-2])

    df_summaryCOVID19=pd.DataFrame(columns=('Country Name','Total Cases', 'Total Deaths'))
    df_summaryCOVID19['Country Name']=list(dic_countriesDF.keys())
    df_summaryCOVID19['Total Cases']=summaryCasesList
    df_summaryCOVID19['Total Deaths']=summaryDeathsList

    df_summaryCOVID19descendent =df_summaryCOVID19.sort_values('Total Cases', ascending=False)
    df_summaryCOVID19ascendent =df_summaryCOVID19.sort_values('Total Cases', ascending=True)
    df_summaryCOVID19descendent.to_csv("data/summaryCOVID19ascendent.csv",index=False)




