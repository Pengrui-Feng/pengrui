# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 11:53:16 2019
@author: pengrui

merge two csv files from turtles including 1) "CTD" and 2) "GPS"
"""

import pandas as pd
import numpy as np

path= '/home/zdong/PENGRUI/original_data/'
#Read the selected columns
dftd  = pd.read_csv(path + "tu102_ctd.csv",usecols=['PTT','END_DATE','TEMP_DBAR','TEMP_VALS','lat','lon'])
#dfgps = pd.read_csv(path + "tu102_gps.csv",usecols=['PTT','D_DATE','LAT','LON'])


s = dftd['TEMP_DBAR'].str.split(',').apply(pd.Series, 1).stack()
#s.index = s.index.droplevel(-1)
#s.name = 'TEMP_DBAR'

t = dftd['TEMP_VALS'].str.split(',').apply(pd.Series, 1).stack()
#t.index = t.index.droplevel(-1)


s.to_csv('s.csv')
t.to_csv('t.csv')




'''
#merge columns on 'PTT'
df=pd.merge(dftd,dfgps,on='PTT',how='left')


#output a new CSV file
df.to_csv('merge_realtime_turtle_td.csv')
'''
