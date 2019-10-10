# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 11:53:16 2019
@author: pengrui

merge two csv files from turtles including 1) "CTD" and 2) "GPS"
"""

import pandas as pd
import numpy as np


#Read the selected columns
df1 = pd.read_csv("/home/zdong/PENGRUI/original_data/tu102_ctd.csv",\
usecols=['PTT','END_DATE','MAX_DBAR','N_TEMP','lat','lon'])
df2 = pd.read_csv("/home/zdong/PENGRUI/original_data/tu102_gps.csv",\
usecols=['PTT','D_DATE','LAT','LON'])

#merge columns on 'PTT'
df3=pd.merge(df1,df2,on='PTT',how='left')


#Create a new CSV file
df3.to_csv('combined_ctd_gps_.csv')
