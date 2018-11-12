#!/usr/bin/env python
# coding: utf-8

# In[151]:


import json
import pandas as pd
import time
import csv
from pandas.io.json import json_normalize
  
with open ('C:/Users/tanli/Desktop/firebase_data.json') as f:
    d = json.load(f)
    
data = json_normalize(d["CO2 1"])
data1 = json_normalize(d["VOC 1"])
data2 = json_normalize(d["PM10 1"])
data3 = json_normalize(d["PM25 1"])
data4 = json_normalize(d["Temperature 1"])
data5 = json_normalize(d["Humidity 1"])
data6 = json_normalize(d["eCO2 1"])

co2 = []
voc = []
pm10 = []
pm25 = []
temperature = []
humi = []
eco2 = []

time_co2 = []
time_voc = []
time_pm10 = []
time_pm25 = []
time_temperature = []
time_humi = []
time_eco2 = []


def parsedata (inData, out1, out2):
    for x in range (inData.size):
        if((x%2)==0):
            out1.append(inData.iloc[0, x])
        elif((x%2)==1):        
            temp = inData.iloc[0, x]/1000
            readable = time.ctime(temp)
            out2.append(readable)

parsedata(data, co2, time_co2)
parsedata(data1, voc, time_voc)
parsedata(data2, pm10, time_pm10)
parsedata(data3, pm25, time_pm25)
parsedata(data4, temperature, time_temperature)
parsedata(data5, humi, time_humi)
parsedata(data6, eco2, time_eco2)

def savedata (name, in1, in2):
    myfile = open('C:/sensor data/'+ name+'.csv', 'w')
    with myfile:
        myfields = ['Time', name]
        writer = csv.DictWriter(myfile, fieldnames = myfields)
        writer.writeheader()
    
        for a in range (len(in1)):
            writer.writerow({name:in1[a], 'Time':in2[a]})

savedata('co2', co2, time_co2)
savedata('voc', voc, time_voc)
savedata('pm10', pm10, time_pm10)
savedata('pm25', pm25, time_pm25)
savedata('temperature', temperature, time_temperature)
savedata('humi', humi, time_humi)
savedata('eco2', eco2, time_eco2)


