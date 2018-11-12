# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 09:44:16 2018

@author: tanli
"""

import json
import pandas as pd
from pandas.io.json import json_normalize
  
with open ('C:/Users/tanli/Desktop/iot-with-firebase-Group 1-export (1).json') as f:
    d = json.load(f)
    
data = json_normalize(d["CO2 1"])
#print(data.head())

print(data.items)
