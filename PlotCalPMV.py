#!/usr/bin/env python
# coding: utf-8

# In[69]:


import pandas as pd
import math
import matplotlib.pyplot as plt

df = pd.read_csv('C:/sensor data/temperature.csv')
df.columns = ['Time', 'temperature']
 
#parse Time column to datetime & convert to index for filtering
df.Time = pd.to_datetime(df.Time)
df.set_index('Time', inplace=True)

#filter by date
df =  df.loc[('Nov' + ' ' + '8' + ' '+ '08:00:00 2018'): ('Nov' + ' ' + '8' + ' '+ '17:30:00 2018')]
#convert back to column
df.reset_index(level=0, inplace=True)
#remove duplicate
df = df.drop_duplicates(subset='Time', keep='last')


df_humi = pd.read_csv('C:/sensor data/humi.csv')
df_humi.columns = ['Time', 'humi']
df_humi.Time = pd.to_datetime(df_humi.Time)
df_humi.set_index('Time', inplace=True)

#filter by date
df_humi =  df_humi.loc[('Nov' + ' ' + '8' + ' '+ '08:00:00 2018'): ('Nov' + ' ' + '8' + ' '+ '17:30:00 2018')]
#convert back to column
df_humi.reset_index(level=0, inplace=True)
df_humi = df_humi.drop_duplicates(subset='Time', keep='last')


a = pd.merge(left=df, right=df_humi, on=['Time'], how='inner')
#sort by time
a = a.sort_values(by='Time')

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
    Tsk = 35.7-0.0283*M

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

#cal PMV for each temp and humi
b = []    
for x in range (len(a)):
    b.append(calPMV((a.iloc[x][1]), (a.iloc[x][2])))

df_pmv = pd.DataFrame()
df_pmv['Time'] = a['Time']
df_pmv['PMV'] = b
c = pd.merge(left=a, right=df_pmv, on=["Time"], how='inner')



#plot graph
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
        
fig, host = plt.subplots(figsize=(15,15))
fig.subplots_adjust(right=0.75)

par1 = host.twinx()
par2 = host.twinx()

par2.spines['right'].set_position(('axes', 1.2))

make_patch_spines_invisible(par2)
par2.spines['right'].set_visible(True)

p1, = host.plot(c['Time'], c['PMV'], 'b-', label='PMV')
p2, = par1.plot(c['Time'], c['humi'], 'r-', label='Humidity')
p3, = par2.plot(c['Time'], c['temperature'], 'g-', label='Temperature')

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
plt.savefig('C:/sensor data/sensor graph/Nov-8-PMV.png')
plt.show()


# In[67]:


print(c)


# In[19]:


a.iloc[0][0]


# In[47]:


c['humi']


# In[51]:


c.iloc[a][0]


# In[68]:


myfile = open('C:/sensor data/a.csv', 'w')
with myfile:
    myfields = ['Time', 'Temperature', 'humidity', 'PMV']
    writer = csv.DictWriter(myfile, fieldnames = myfields)
    writer.writeheader()
    
    for d in range (len(c)):
        writer.writerow({'Time':c.iloc[d][0], 'Temperature':c.iloc[d][1], 'humidity':c.iloc[d][2], 'PMV':c.iloc[d][3]})


# In[49]:


import csv


# In[63]:


myfile = open('C:/sensor data/b.csv', 'w')
with myfile:
    myfields = ['Time', 'Temperature']
    writer = csv.DictWriter(myfile, fieldnames = myfields)
    writer.writeheader()
    
    for d in range (len(df)):
        writer.writerow({'Time':df.iloc[d][0], 'Temperature':df.iloc[d][1]})


# In[66]:


len(c)

