#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import math
import matplotlib.pyplot as plt
import csv

month = 'Nov'
date = '8'

df = pd.read_csv('C:/sensor data/temperature.csv')
df.columns = ['Time', 'temperature']
 
#parse Time column to datetime
df.Time = pd.to_datetime(df.Time)
df.set_index('Time', inplace=True)

#filter by date
df =  df.loc[(month + ' ' + date + ' '+ '08:00:00 2018'): (month + ' ' + date + ' '+ '17:30:00 2018')]

df_humi = pd.read_csv('C:/sensor data/humi.csv')
df_humi.columns = ['Time', 'humi']
df_humi.Time = pd.to_datetime(df_humi.Time)
df_humi.set_index('Time', inplace=True)

#filter by date
df_humi =  df_humi.loc[(month + ' ' + date + ' '+ '08:00:00 2018'): (month + ' ' + date + ' '+ '17:30:00 2018')]

df_co2 = pd.read_csv('C:/sensor data/co2.csv')
df_co2.columns = ['Time', 'co2']
df_co2.Time = pd.to_datetime(df_co2.Time)
df_co2.set_index('Time', inplace=True)

#filter by date
df_co2 =  df_co2.loc[(month + ' ' + date + ' '+ '08:00:00 2018'): (month + ' ' + date + ' '+ '17:30:00 2018')]

df_voc = pd.read_csv('C:/sensor data/voc.csv')
df_voc.columns = ['Time', 'voc']
df_voc.Time = pd.to_datetime(df_voc.Time)
df_voc.set_index('Time', inplace=True)

#filter by date
df_voc =  df_voc.loc[(month + ' ' + date + ' '+ '08:00:00 2018'): (month + ' ' + date + ' '+ '17:30:00 2018')]

df_eco2 = pd.read_csv('C:/sensor data/eco2.csv')
df_eco2.columns = ['Time', 'eco2']
df_eco2.Time = pd.to_datetime(df_eco2.Time)
df_eco2.set_index('Time', inplace=True)

#filter by date
df_eco2 =  df_eco2.loc[(month + ' ' + date + ' '+ '08:00:00 2018'): (month + ' ' + date + ' '+ '17:30:00 2018')]

df_pm10 = pd.read_csv('C:/sensor data/pm10.csv')
df_pm10.columns = ['Time', 'pm10']
df_pm10.Time = pd.to_datetime(df_pm10.Time)
df_pm10.set_index('Time', inplace=True)

#filter by date
df_pm10 =  df_pm10.loc[(month + ' ' + date + ' '+ '08:00:00 2018'): (month + ' ' + date + ' '+ '17:30:00 2018')]

df_pm25 = pd.read_csv('C:/sensor data/pm25.csv')
df_pm25.columns = ['Time', 'pm25']
df_pm25.Time = pd.to_datetime(df_pm25.Time)
df_pm25.set_index('Time', inplace=True)

#filter by date
df_pm25 =  df_pm25.loc[(month + ' ' + date + ' '+ '08:00:00 2018'): (month + ' ' + date + ' '+ '17:30:00 2018')]

a = pd.merge(df, pd.merge(df_humi, pd.merge(df_voc, pd.merge(df_eco2, pd.merge(df_co2, pd.merge(df_pm10, df_pm25,  on=['Time']), on=['Time']), on=['Time']), on=['Time']), on=['Time']), on=['Time'])
#sort by time
a = a.sort_values(by='Time')

myfile = open('C:/sensor data/'+ month + '-' + date+ '-' + 'all' + '.csv', 'w')
with myfile:
    myfields = ['Time', 'temperature', 'humi', 'voc', 'eco2', 'co2', 'pm10', 'pm25']
    writer = csv.DictWriter(myfile, fieldnames = myfields)
    writer.writeheader()
    
    for x in range (len(a)):
        writer.writerow({'Time':a.index[x], 'temperature':a.iloc[x][0], 'humi':a.iloc[x][1], 'voc':a.iloc[x][2], 'eco2':a.iloc[x][3], 'co2':a.iloc[x][4], 'pm10':a.iloc[x][5], 'pm25':a.iloc[x][6]})



