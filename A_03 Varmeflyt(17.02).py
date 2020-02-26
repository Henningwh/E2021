# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 16:52:41 2020

@author: henninwh
"""

#Modellerer varmetap med newtons varmetaps likning

#dT/dt=-k(T-Ta) --> T(t) = Ce^-(kt)+Ta
#T_r1 = Reell innrtemperatur målt av sensor ved tidspunkt 1
#T_r2 = Reell innrtemperatur målt av sensor ved tidspunkt 2
#T_e = estimert innetemperatur fra x minnutter før
#T_u = utetemperatur
#dt = tidsintervall mellom tidspunkt 1 og tidspunkt 2
#C regnes enkelt ut
#k regnes ut


###################################################################################################################
from yr.libyr import Yr
import json
info = {}
weather = Yr(location_name='Norway/Oslo/Oslo/Oslo', forecast_link='forecast_hour_by_hour')
for forecast in weather.forecast(str): #for alle 'forecast i weather.forecastene
        data = json.loads(forecast) #Last inn værdata
        print(data['symbol'])
        tempStr = data['temperature']['@value'] #henter ut verdien temp verdien som streng
        tempInt = int(tempStr) #gjør til int
        rtime = data['@from'] #Tar ut tidsstempelet fra timen som blir gitt ut til neste time
               
        info[rtime] =  {'@time': rtime, '@temp' : tempInt} #markerer hvert data sett med unik datokode og Legger tidsdataen i et dict og tar med all tidsdata for neste 24t i et stort dict
        
                
                
######################################################################################################################        

import math
import time
import pendulum

roof = 23 #maksimal temperatur i bygget (kan endres fra webside)
floor = 17 #min temperatur i bygget ( kan endres fra webside)

CList = []
kList = []

#Finner T_u
now = pendulum.now() #Finner nå-tid
now1 = now.to_atom_string()
now2 = pendulum.parse(now1)
for rtime in info.items():
    tid = rtime[1]['@time'] #Leter gjennom alle tidene i værmeldingen
    tid = pendulum.parse(tid)
    if tid.hour == now2.hour: #Hvis programmet finner riktig time settes T_u lik den korresponderende temperaturen og stopper å lete.
        T_u = rtime[1]['@temp']
        break
    
        
    
     

#T_r1s = {'13.02.2020 kl:10:00': {'dato': '13.02.2020', 'kl': '12:20', 'temp' : '18.4'}}
T_r1s = {0: {'@time': '2020-02-14T13:55:00', '@temp': 23},
 1: {'@time': '2020-02-14T14:00:00', '@temp': 22},
 2: {'@time': '2020-02-14T14:05:00', '@temp': 19},
 3: {'@time': '2020-02-14T14:10:00', '@temp': 18},
 4: {'@time': '2020-02-14T14:15:00', '@temp': 16},
 5: {'@time': '2020-02-14T14:20:00', '@temp': 13},
 6: {'@time': '2020-02-14T14:25:00', '@temp': 10},
 7: {'@time': '2020-02-14T14:30:00', '@temp': 8},
 8: {'@time': '2020-02-14T14:35:00', '@temp': 7},
 9: {'@time': '2020-02-14T14:40:00', '@temp': 7}} #test array for målte temp
T_r2s =  {0: {'@time': '2020-02-14T14:00:00', '@temp': 22},
 1: {'@time': '2020-02-14T14:05:00', '@temp': 19},
 2: {'@time': '2020-02-14T14:10:00', '@temp': 18},
 3: {'@time': '2020-02-14T14:15:00', '@temp': 16},
 4: {'@time': '2020-02-14T14:20:00', '@temp': 13},
 5: {'@time': '2020-02-14T14:25:00', '@temp': 10},
 6: {'@time': '2020-02-14T14:30:00', '@temp': 8},
 7: {'@time': '2020-02-14T14:35:00', '@temp': 7},
 8: {'@time': '2020-02-14T14:40:00', '@temp': 7},
 9: {'@time': '2020-02-14T14:45:00', '@temp': 6}} #test array for målte temp



i = 0

#T_r1 = 20 
#T_r2 = 18
T_e = 0
om_min = 5
dtList = [] #liste over alle  


while(i<10):
    T_r1 = T_r1s[i]['@temp'] #tar temp verdien i hver måling 1
    T_r2 = T_r2s[i]['@temp'] #tar temp verdien i hver måling 2
    
    TS_r1 = pendulum.parse(T_r1s[0]['@time']) #Henter tidsstempelet til måling 1, 1.måling
    TS_r2 = pendulum.parse(T_r2s[i]['@time']) #Henter tidsstempelet til måling 2
    
    dt = (TS_r2.timestamp()-TS_r1.timestamp())/60 #tid mellom første måling i måling 1 og hver enkelt måling i måling 2 i min
    dtList.append(dt) #legger tidsdeltaene i liste
    print('dt :',dt)
    time.sleep(dt/100) #ganger minnutter
    
    C = roof-T_u
    
    if T_u == T_r2: #unngår math error ved å sette k=0 hvis T_u = T_r2
        k = 0
        print('0 :', k)
    elif T_u < T_r2: # negativ k senker gradene når det er kaldere utenfor enn inne ved måling 2 (nå)
        k = -(math.log2((abs(T_r2-T_u))/C))/dt
        print('k1 :', k)
    else:
        k = (math.log2((abs(T_r2-T_u))/C))/dt
        print('k2 :' ,k)
    CList.append(C) #legger alle verdiene av C i en liste
    kList.append(k)#legger alle verdiene av k i en liste

    T_e = C*(math.e**-(k*dt))+T_u
    i = i+1
#    
#    print('C: ', C)
#    print('k: ', k)
    #print('Estimert temp: ',T_e)
    
CKal = sum(CList)/len(CList)     
kKal = sum(kList)/len(kList)
print('Ckal :', CKal)
print('kKal :', kKal)
a = 0
T_eList = []
while(a<10):
    time.sleep(dt/100)
    T_e = CKal*(math.e**-(kKal*int(dtList[a])))+T_u
    T_eList.append(T_e)
    a+=1
    print(a )
    print(T_e)