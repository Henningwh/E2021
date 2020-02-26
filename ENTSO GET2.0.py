# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 16:02:33 2020

@author: Preben
"""

import numpy as np
import pendulum
import pandas as pd
from yr.libyr import Yr
import json



########################################################################################################################
#ENTSOE GET
def Currency_Rate(InCur,OutCur):
    
    import requests

# Where USD is the base currency you want to use
    url = 'https://api.exchangerate-api.com/v4/latest/'+InCur

# Making our request
    response = requests.get(url)
    data = response.json()

# Your JSON object
    rates=data['rates']
    WantedRate=rates[OutCur]
    return WantedRate

def Day_Ahead_Prices():

    from entsoe import EntsoePandasClient
    import pandas as pd
    import os
    import pendulum


    today=      pendulum.today().strftime('%Y-%m-%d')
    tomorrow =  pendulum.tomorrow().add(days=1).strftime('%Y-%m-%d')


    client = EntsoePandasClient(api_key='bd39354a-6404-40d1-b289-90a2d8135862')

    start = pd.Timestamp(today, tz='Europe/Oslo')
    end = pd.Timestamp(tomorrow, tz='Europe/Oslo')
    country_code = 'NO-3'  #Trondheim


    ts = client.query_day_ahead_prices(country_code, start=start, end=end)

    pris=[]

    for x in range(0, 48):
        pris.append(ts[x])
        
    return pris
        
    
InCur= 'EUR'
OutCur= 'NOK'

Multiple=Currency_Rate(InCur,OutCur)
Price=Day_Ahead_Prices()
    
PriceOutCur=np.array(Price)*Multiple    #liste med pris i 48 timer

#########################################################################################################################
#YR GET

info = {}
weather = Yr(location_name='Norway/Telemark/Skien/Skien', forecast_link='forecast_hour_by_hour')
for forecast in weather.forecast(str): #for alle 'forecast i weather.forecastene
        data = json.loads(forecast) #Last inn værdata
        tempStr = data['temperature']['@value'] #henter ut verdien temp verdien som streng
        tempInt = int(tempStr) #gjør til int
        rtime = data['@from'] #Tar ut tidsstempelet fra timen som blir gitt ut til neste time
               
        info[rtime] =  {'@time': rtime, '@temp' : tempInt} #markerer hvert data sett med unik datokode og Legger tidsdataen i et dict og tar med all tidsdata for neste 24t i et stort dict

###########################################################################################################################
#Sortete de neste 24 timene
        
#lager timestamps for 2 neste døgn,1. døgn er nåværende
timestamp=[]
for x in range(0,48):
    timestamp.append(pendulum.today().add(hours=x).strftime('%Y-%m-%dT%H:%M:%S'))
   
#Setter 48 timer i dictionary
dataut={}
for i in range(0,48):   
    dataut[timestamp[i]] ={'pris': PriceOutCur[i]}
    
#plukker ut prisene for neste 24 timer
    
priceOutNext24=[]
for i in range(0,24):
    time=pendulum.now().add(hours=i+1).strftime('%Y-%m-%dT%H:00:00')
    priceOutNext24.append(dataut[time]['pris'])
    
#lager liste for over og under gjennomsnittet de neste 24
averagePrice= np.average(priceOutNext24)
averageList=[]
for x in range(0,24):
    if priceOutNext24[x] < averagePrice:
        averageList.append(-1)
    elif priceOutNext24[x] > averagePrice:
        averageList.append(1)
    else:
        averageList.append(0)

#rangerer priser de neste 24 timene
        
SortedList=sorted(priceOutNext24)
    
ScoreBoard=[]
for x in range(0,24):
    for y in range(0,24):
        if priceOutNext24[x] == SortedList[y]:
            ScoreBoard.append(y)

#liste med temperatur neste 24
tempList=[]
for i in range(0,24):
    time=pendulum.now().add(hours=i+1).strftime('%Y-%m-%dT%H:00:00')
    tempList.append(info[time]['@temp'])
    
#sette all infor om de neste 24 timer inn i samme dictionary
#temperatur, pris, gjennomsnitt, rangering
            
            
main24={}
for i in range(0,24):
    time=pendulum.now().add(hours=i+1).strftime('%Y-%m-%dT%H:00:00')
    main24[time]={'pris': priceOutNext24[i],'gjennomsnitt':averageList[i],'rangering':ScoreBoard[i],'temperatur': tempList[i]}

#all info tatt inn fra nett
##############################################################################################################################


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    