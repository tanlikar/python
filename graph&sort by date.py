#!/usr/bin/env python
# coding: utf-8

# In[76]:


import matplotlib.pyplot as plt
import datetime as dt
import time
import csv

import numpy as np
import pandas as pd

import plotly.plotly as py
import plotly.tools as tls 

sensor = ['temperature', 'humi', 'pm10', 'pm25', 'eco2', 'voc', 'co2', ]
df_all = pd.DataFrame()
month = 'Nov'
date = '8'

def plotGraph (name, month, date):
    global df_all
    df = pd.read_csv('C:/sensor data/' + name + '.csv')
    df.columns = ['Time', name]
 
    #parse Time column to datetime
    df.Time = pd.to_datetime(df.Time)
    df.set_index('Time', inplace=True)

    #filter by date
    df =  df.loc[(month + ' ' + date + ' '+ '08:00:00 2018'): (month + ' ' + date + ' '+ '17:30:00 2018')]
    df[name].plot(figsize=(20,10), linewidth =2, fontsize=14)
    plt.xlabel('Time', fontsize=20);
    plt.ylabel(name, fontsize=20);
   # plt.show()
    
    df.reset_index(level=0, inplace=True)
    df = df.drop_duplicates(subset='Time', keep='last')
    
    if df_all.empty:
        df_all = df
    else:
        df_all = pd.merge(df_all, df, on='Time', how='outer')

def plotDate(month, date):
    for x in sensor:
        plt.figure(x)
        plotGraph(x, month, date)
        plt.savefig('C:/sensor data/sensor graph/' + x + ' ' + month + ' ' + date + '.png')
        

plotDate(month, date)

df_all = df_all.sort_values(by='Time')

for x in range (len(df_all)):
    try:
        if((df_all.iloc[x+1][0]-df_all.iloc[x][0])==dt.timedelta(seconds=1)):
            df_all.iloc[x]=df_all.iloc[x].combine_first(df_all.iloc[x+1])
    except:
        pass

df_all = df_all.dropna()
    
myfile = open('C:/sensor data/'+ month + '-' + date+ '-' + 'all' + '.csv', 'w')
with myfile:
    myfields = ['Time', 'temperature', 'humi', 'voc', 'eco2', 'co2', 'pm10', 'pm25']
    writer = csv.DictWriter(myfile, fieldnames = myfields)
    writer.writeheader()
    
    for x in range (len(df_all)):
        writer.writerow({'Time':df_all.iloc[x][0], 'temperature':df_all.iloc[x][1], 'humi':df_all.iloc[x][2], 'voc':df_all.iloc[x][3], 'eco2':df_all.iloc[x][4], 'co2':df_all.iloc[x][5], 'pm10':df_all.iloc[x][6], 'pm25':df_all.iloc[x][7]})
    


# In[28]:


df_all.sort_values(by='Time')


# In[77]:


df_all

