#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import datetime as dt

import numpy as np
import pandas as pd

import plotly.plotly as py
import plotly.tools as tls 

sensor = ['co2', 'voc', 'temperature', 'humi', 'pm10', 'pm25', 'eco2']

def plotGraph (name, month, date):
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

def plotDate(month, date):
    for x in sensor:
        plt.figure(x)
        plotGraph(x, month, date)
        plt.savefig('C:/sensor data/sensor graph/' + x + ' ' + 'month' + ' ' + 'date' + '.png')
        
def plotDateOverall(month, date):
    plt.figure('p')
    for x in sensor:
        plotGraph(x, month, date)
    plt.legend()
    plt.ylabel('')
    plt.savefig('C:/sensor data/sensor graph/all' + month+ ' ' + date + ' ' + '.png')


plt.close("all")    
        
plotDate('Nov', '8')
plotDateOverall('Nov', '8')
    




