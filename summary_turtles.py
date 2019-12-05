# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 09:37:53 2019

summary specified data by pandas

@author: pengrui
"""
from datetime import datetime
import pandas as pd
import numpy as np
import csv

db= 'tu73' #tu73,tu74,tu94,tu98,tu99,tu102
path1 = '/home/zdong/PENGRUI/merge/'
path2 = '/home/zdong/PENGRUI/summary/'
#input csv file,
df = pd.read_csv(path1+db+"_merge_td_gps.csv")# modify the name of file
df['argos_date'] = pd.to_datetime(df['END_DATE'])
#a = df.set_index('PTT')

#Count the number of turtles and times each turtle transmits data
'''
ptt = pd.Series(df['PTT'])     
nums_ptt = ptt.value_counts() 
nums_ptt.count()
'''
#date = pd.Series(df['argos_date'])
#nums_date = date.value_counts()
count_ptt = df['PTT'].groupby(df['PTT']).count()

#date
df['argos_date']=df['argos_date']
grouped1 = df['argos_date'].groupby(df['PTT'])
date_max = grouped1.max()
date_min = grouped1.min()
delta_date = grouped1.max() - grouped1.min()

#lat
grouped2 = df['lat'].groupby(df['PTT'])
lat_max = grouped2.max()
lat_min = grouped2.min()
delta_lat = grouped2.max() - grouped2.min()

#lon
grouped3 = df['lon'].groupby(df['PTT'])
lon_max = grouped3.max()
lon_min = grouped3.min()
delta_lon = grouped3.max() - grouped3.min()
'''
#gps
gps = df['LAT'].groupby(df['PTT']).mean()
r=gps.notnull()
'''
#Create a DataFrame with multiple Series
c = pd.DataFrame()
c['count_ptt']=pd.Series(count_ptt)
c['start_date']=pd.Series(date_min)
c['end_date']=pd.Series(date_max)
c['length_of_track']=pd.Series(delta_date)
c['lat_min']=pd.Series(lat_min)
c['lat_max']=pd.Series(lat_max)
c['lon_min']=pd.Series(lon_min)
c['lon_max']=pd.Series(lon_max)
c['delta_lat']=pd.Series(delta_lat)
c['delta_lon']=pd.Series(delta_lon)
#c['if_with_gps']=pd.Series(r)

c.to_csv(path2+db+'_Summary.csv')
