# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 09:37:53 2019

Summary specified data by pandas

@author: pengrui
"""

import pandas as pd
import numpy as np
import csv

#input csv file,
df = pd.read_csv("combined_td_gps.csv")#,usecols=['PTT','argos_date','argos_time','lat_argos','lon_argos']
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
delta_date = grouped1.max() - grouped1.min()

#lat
grouped2 = df['lat_argos'].groupby(df['PTT'])
lat_max = grouped2.max()
lat_min = grouped2.min()
delta_lat = grouped2.max() - grouped2.min()

#lon
grouped3 = df['lon_argos'].groupby(df['PTT'])
lon_max = grouped3.max()
lon_min = grouped3.min()
delta_lon = grouped3.max() - grouped3.min()

#gps
gps = df['lat_gps'].groupby(df['PTT']).mean()
r=gps.notnull()

#Create a DataFrame with multiple Series
c = pd.DataFrame()
c['nums_ptt']=pd.Series(nums_ptt)
c['start_date']=pd.Series(date_min)
c['end_date']=pd.Series(date_max)
c['length_of_track']=pd.Series(delta_date)
c['lat_min']=pd.Series(lat_min)
c['lat_max']=pd.Series(lat_max)
c['lon_min']=pd.Series(lon_min)
c['lon_max']=pd.Series(lon_max)
c['delta_lat']=pd.Series(delta_lat)
c['delta_lon']=pd.Series(delta_lon)
c['if_with_gps']=pd.Series(r)


c.to_csv('Summary.csv')
