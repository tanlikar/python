#!/usr/bin/env python
# coding: utf-8

# In[16]:


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
df.reset_index(level=0, inplace=True)
df = df.drop_duplicates(subset='Time', keep='last')

df_humi = pd.read_csv('C:/sensor data/humi.csv')
df_humi.columns = ['Time', 'humi']
df_humi.Time = pd.to_datetime(df_humi.Time)
df_humi.set_index('Time', inplace=True)

#filter by date
df_humi =  df_humi.loc[(month + ' ' + date + ' '+ '08:00:00 2018'): (month + ' ' + date + ' '+ '17:30:00 2018')]
df_humi.reset_index(level=0, inplace=True)
df_humi = df_humi.drop_duplicates(subset='Time', keep='last')

df_co2 = pd.read_csv('C:/sensor data/co2.csv')
df_co2.columns = ['Time', 'co2']
df_co2.Time = pd.to_datetime(df_co2.Time)
df_co2.set_index('Time', inplace=True)

#filter by date
df_co2 =  df_co2.loc[(month + ' ' + date + ' '+ '08:00:00 2018'): (month + ' ' + date + ' '+ '17:30:00 2018')]
df_co2.reset_index(level=0, inplace=True)
df_co2 = df_co2.drop_duplicates(subset='Time', keep='last')

df_voc = pd.read_csv('C:/sensor data/voc.csv')
df_voc.columns = ['Time', 'voc']
df_voc.Time = pd.to_datetime(df_voc.Time)
df_voc.set_index('Time', inplace=True)

#filter by date
df_voc =  df_voc.loc[(month + ' ' + date + ' '+ '08:00:00 2018'): (month + ' ' + date + ' '+ '17:30:00 2018')]
df_voc.reset_index(level=0, inplace=True)
df_voc = df_voc.drop_duplicates(subset='Time', keep='last')

df_eco2 = pd.read_csv('C:/sensor data/eco2.csv')
df_eco2.columns = ['Time', 'eco2']
df_eco2.Time = pd.to_datetime(df_eco2.Time)
df_eco2.set_index('Time', inplace=True)

#filter by date
df_eco2 =  df_eco2.loc[(month + ' ' + date + ' '+ '08:00:00 2018'): (month + ' ' + date + ' '+ '17:30:00 2018')]
df_eco2.reset_index(level=0, inplace=True)
df_eco2 = df_voc.drop_duplicates(subset='Time', keep='last')


df_pm10 = pd.read_csv('C:/sensor data/pm10.csv')
df_pm10.columns = ['Time', 'pm10']
df_pm10.Time = pd.to_datetime(df_pm10.Time)
df_pm10.set_index('Time', inplace=True)

#filter by date
df_pm10 =  df_pm10.loc[(month + ' ' + date + ' '+ '08:00:00 2018'): (month + ' ' + date + ' '+ '17:30:00 2018')]
df_pm10.reset_index(level=0, inplace=True)
df_pm10 = df_voc.drop_duplicates(subset='Time', keep='last')

df_pm25 = pd.read_csv('C:/sensor data/pm25.csv')
df_pm25.columns = ['Time', 'pm25']
df_pm25.Time = pd.to_datetime(df_pm25.Time)
df_pm25.set_index('Time', inplace=True)

#filter by date
df_pm25 =  df_pm25.loc[(month + ' ' + date + ' '+ '08:00:00 2018'): (month + ' ' + date + ' '+ '17:30:00 2018')]
df_pm25.reset_index(level=0, inplace=True)
df_pm25 = df_pm25.drop_duplicates(subset='Time', keep='last')

a = pd.merge(left=df, right=pd.merge(left=df_humi, right=pd.merge(left=df_voc, right=pd.merge(left=df_voc, right=pd.merge(left=df_co2, right=pd.merge(left=df_pm10, right=df_pm25,  on=['Time'], how='outer'), on=['Time'], how='outer'), on=['Time'], how='outer'), on=['Time'], how='outer'), on=['Time'], how='outer'), on=['Time'], how='outer')
#sort by time
a = a.sort_values(by='Time')

myfile = open('C:/sensor data/'+ month + '-' + date+ '-' + 'all' + '.csv', 'w')
with myfile:
    myfields = ['Time', 'temperature', 'humi', 'voc', 'eco2', 'co2', 'pm10', 'pm25']
    writer = csv.DictWriter(myfile, fieldnames = myfields)
    writer.writeheader()
    
    for x in range (len(a)):
        writer.writerow({'Time':a.iloc[x][0], 'temperature':a.iloc[x][1], 'humi':a.iloc[x][2], 'voc':a.iloc[x][3], 'eco2':a.iloc[x][4], 'co2':a.iloc[x][5], 'pm10':a.iloc[x][6], 'pm25':a.iloc[x][7]})


# In[17]:


len(a)


# In[12]:


len(df)


# In[13]:


len(df_humi)


# In[14]:


len(df_voc)


# In[8]:


len(df_co2)


# In[9]:


len(df_eco2)


# In[20]:


len(df_pm10)


# In[21]:


len(df_pm25)

