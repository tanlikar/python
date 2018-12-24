
import matplotlib.pyplot as plt
import datetime as dt
import time
import csv
import math
import itertools

import numpy as np
import pandas as pd

sensor = ['temperature', 'humi', 'voc', 'eco2','co2', 'pm10', 'pm25']
dataframe_collection = {}
month_day = []
df_all = pd.DataFrame()

for x in range (len(sensor)):
    dataframe_collection[x] = pd.read_csv('C:/sensor data/' + sensor[x] + '.csv')
    dataframe_collection[x].columns = ['Time', sensor[x]]
    dataframe_collection[x] = dataframe_collection[x].sort_values(by='Time')
    dataframe_collection[x].Time = pd.to_datetime(dataframe_collection[x].Time)
    
    #remove invalid data
    if(x==0):
        dataframe_collection[x] = dataframe_collection[x][dataframe_collection[x].temperature <= 100]
    elif(x==1):
        dataframe_collection[x] = dataframe_collection[x][dataframe_collection[x].humi != 0]
    elif(x==4):
        dataframe_collection[x] = dataframe_collection[x][dataframe_collection[x].co2 <= 10000]
            

for x in range(len(sensor)):
    a =pd.DatetimeIndex(dataframe_collection[x]['Time']).month
    b = pd.DatetimeIndex(dataframe_collection[x]['Time']).day
    
    month_day.append([a[0], b[0]])
    for y in range (len(a)):
        try:
            if((a[y] != a[y+1]) and (b[y] != b[y+1])):
                month_day.append([a[y+1], b[y+1]])
            elif((a[y] == a[y+1]) and (b[y] != b[y+1])):
                month_day.append([a[y], b[y+1]])
           
        except:
            pass

month_day.sort()
month_day = list(month_day for month_day,_ in itertools.groupby(month_day))     


##########################################################################################################
def plotGraph (name,month, date, df):
    global df_all     
    
    df = df.drop_duplicates(subset='Time', keep='last')
    
    #filter by date
    df.set_index('Time', inplace=True)    
    df =  df.loc[(month + ' ' + date + ' '+ '08:00:00 2018'): (month + ' ' + date + ' '+ '17:30:00 2018')]
   
    df[name].plot(figsize=(20,10), linewidth =2, fontsize=14)
    plt.xlabel('Time', fontsize=20);
    plt.ylabel(name, fontsize=20);
    df.reset_index(inplace=True)
        
        
    if df_all.empty:
        df_all = df
    else:
        df_all = pd.merge(df_all, df, on='Time', how='outer')
        
###################################################################################################################
#cal PMV
def calPMV (temp, humi): #iso7730 standard
    Ta = Tr = temp
    v=0.1 #assume air velocity constant
    rh=humi
    Icl=1.2 #assume 1.2 col for clothes insulation (long sleeves and long pants)
    W=0
    M=70.0 #assume metabolic rate of office work

    Balance = 0
    E=0
    Ediff=0
    Hres = 0
    R=0
    C=0

    Icl = Icl*0.155
    Tsk = 35.7-0.0285*M

    Pa = (rh/100.0)*0.1333*math.exp(18.6686-4030.183/(Ta+235))

    Tcl = Ta
    hr = 3
    S = 0
    ArAdu = 0.77
    factor = 500
    Iclr = Icl

    while (True):
        fcl=1.05+0.65*Icl
        E=0.42*((M-W)-58)
        Ediff=3.05*(0.255*Tsk-3.36-Pa)
        Hres=1.73E-2*M*(5.867-Pa)+1.4E-3*M*(34-Ta)
        Tcl=Tsk-Icl*(M-W-E-Ediff-Hres-S)      
        hr=5.67E-8*0.95*ArAdu*(math.exp(4*math.log(273+Tcl))- math.exp(4*math.log(273+Tr)))/(Tcl-Tr)
        hc=12.1*math.pow(v,0.5)
        R=fcl*hr*(Tcl-Tr)
        C=fcl*hc*(Tcl-Ta)
        Balance=M-W-E-Ediff-Hres-R-C-S  
        if(Balance>0):
            S=S+factor
            factor=factor/2
        else:
            S=S-factor
        
        if(not(abs(Balance) > 0.01)):
            break


    S=M-W-E-Ediff-Hres-R-C
    PMV=(0.303*math.exp(-0.036*M)+0.028)*S
    return (PMV)

#########################################################################################################################

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
        
########################################################################################################################

def myFunc(month, date):
    global df_all
    df_all = df_all[0:0]
    
    for x in range (len(sensor)):
        try:
            plt.figure()
            plotGraph(sensor[x], month, date, dataframe_collection[x])
            plt.savefig('C:/data/sensor graph/'+ sensor[x] + '-' + month + '-' + date + '.png')
            plt.cla()
            plt.clf()
            plt.close()
        except:
            pass
    
    df_all = df_all.sort_values(by='Time')

    for x in range (len(df_all)):
        try:
            if((df_all.iloc[x+1][0]-df_all.iloc[x][0])==dt.timedelta(seconds=1)):
                df_all.iloc[x]=df_all.iloc[x].combine_first(df_all.iloc[x+1])
        except:
            pass

    df_all = df_all.dropna()
    

    #cal PMV for each temp and humi
    b = []    
    for x in range (len(df_all)):
        b.append(calPMV((df_all.iloc[x][1]), (df_all.iloc[x][2])))

    df_pmv = pd.DataFrame()
    df_pmv['Time'] = df_all['Time']
    df_pmv['PMV'] = b
    df_all = pd.merge(left=df_all, right=df_pmv, on=["Time"], how='outer')
    
    myfile = open('C:/data/'+ month + '-' + date+ '-' + 'all' + '.csv', 'w')
    with myfile:
        myfields = ['Time', 'temperature', 'humi', 'voc', 'eco2', 'co2', 'pm10', 'pm25', 'PMV']
        writer = csv.DictWriter(myfile, fieldnames = myfields)
        writer.writeheader()
    
        for x in range (len(df_all)):
            writer.writerow({'Time':df_all.iloc[x][0], 'temperature':df_all.iloc[x][1], 'humi':df_all.iloc[x][2], 'voc':df_all.iloc[x][3], 'eco2':df_all.iloc[x][4], 'co2':df_all.iloc[x][5], 'pm10':df_all.iloc[x][6], 'pm25':df_all.iloc[x][7], 'PMV':df_all.iloc[x][8]})
    



    #plot PMV  with temp and humi on same axis
    fig, host = plt.subplots(figsize=(15,15))
    fig.subplots_adjust(right=0.75)

    par1 = host.twinx()
    par2 = host.twinx()

    par2.spines['right'].set_position(('axes', 1.2))

    make_patch_spines_invisible(par2)
    par2.spines['right'].set_visible(True)

    p1, = host.plot(df_all['Time'], df_all['PMV'], 'b-', label='PMV')
    p2, = par1.plot(df_all['Time'], df_all['humi'], 'r-', label='Humidity')
    p3, = par2.plot(df_all['Time'], df_all['temperature'], 'g-', label='Temperature')

    host.set_xlabel('Time')
    host.set_ylabel('PMV')
    par1.set_ylabel('Humidity')
    par2.set_ylabel('Temperature')

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())

    tkw = dict(size=4, width=1.5)
    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)

    lines = [p1,p2,p3]
    host.legend(lines, [l.get_label() for l in lines])
    plt.savefig('C:/data/sensor graph/'+month+'-'+date +'-'+'PMV.png')
    plt.cla()
    plt.clf()
    plt.close()
    #plt.show()
 ######################################################################################################

for x in range (len(month_day)):
    myFunc(str(month_day[x][0]), str(month_day[x][1]))
    

        


