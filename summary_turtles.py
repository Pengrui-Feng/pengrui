# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 09:37:53 2019

Collect specified data by pandas

@author: pengrui
"""

import pandas as pd
import numpy as np
import csv

#input csv file,
path = '/home/zdong/PENGRUI/data_process/'
df = pd.read_csv(path + "combined_td_gps.csv")#,usecols=['PTT','argos_date','argos_time','lat_argos','lon_argos']
df['argos_date'] = pd.to_datetime(df['argos_date'])
#a = df.set_index('PTT')


#Count the number of turtles and times each turtle transmits data
'''
ptt = pd.Series(df['PTT'])     
nums_ptt = ptt.value_counts() 
nums_ptt.count()
'''
#date = pd.Series(df['argos_date'])
#nums_date = date.value_counts()
nums_ptt = df['PTT'].groupby(df['PTT']).count()

#date
grouped1 = df['argos_date'].groupby(df['PTT'])
date_max = grouped1.max()
date_min = grouped1.min()
dalta_date = grouped1.max() - grouped1.min()
#dalta_date.rename(index={'PTT':'ptt', ' ':'dalta'}, inplace = True)
#lat
grouped2 = df['lat_argos'].groupby(df['PTT'])
lat_max = grouped2.max()
lat_min = grouped2.min()
dalta_lat = grouped2.max() - grouped2.min()

#lon
grouped3 = df['lon_argos'].groupby(df['PTT'])
lon_max = grouped3.max()
lon_min = grouped3.min()
dalta_lon = grouped3.max() - grouped3.min()

#gps
gps = df['lat_gps'].groupby(df['PTT']).mean()
r=gps.notnull()

#Create a DataFrame with multiple Series
c = pd.DataFrame(dalta_date)
c.rename(columns={ '0':'dalta'}, inplace = True)
c.insert(0,'start_date',date_min)
c.insert(1,'end_date',date_max)
c.insert(3,'lat_min',lat_min)
c.insert(4,'lat_max',lat_max)
c.insert(5,'lon_min',lat_min)
c.insert(6,'lon_max',lat_max)
c.insert(7,'delta_lat',dalta_lat)
c.insert(8,'delta_lon',dalta_lon)
c.insert(9,'if_with_gps',r)
#c.insert(9,'gps',gps)
c.insert(0,'nums_ptt',nums_ptt)


c.to_csv('Summary.csv')


#modify the name of columns
d = pd.read_csv('Summary.csv')
d.columns = ['ptt','nums_ptt','start_date','end_date','length_of_track','lat_min','lat_max','lon_min','lon_max',
             'delta_lat','delta_lon','if_with_gps']
d.to_csv('Summary.csv')
