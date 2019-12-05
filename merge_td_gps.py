# -*- coding: utf-8 -*-
'''
Extract data file ctd_extract_good.csv, add new column "TF".
If TF==True, data is good.
If TF==False, data is bad.
'''
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from turtleModule import mon_alpha2num, np_datetime, dist

db= 'tu102' #tu73,tu74,tu94,tu98,tu99,tu102
path1= '/home/zdong/PENGRUI/get_original_data/'
path2= '/home/zdong/PENGRUI/merge/'
r = 3                           # the ctd position that has gps position within (r) kilometers might be considered as good data.
hour = 3                        # the ctd time that has gps time within (hour) hours might be considered as good data.

ctd = pd.read_csv(path1+db+'_ctd.csv') # original data file
ctd.rename(columns = {"LAT": "lat",'LON':'lon'},inplace=True) #tu73,tu74
ctdlat = ctd['lat']
ctdlon = ctd['lon']

ctdtime = np_datetime(ctd['END_DATE'])
gps = pd.read_csv(path1+db+'_gps.csv') # orginal data file

gpslat = gps['LAT']
gpslon = gps['LON']
gpstime = np_datetime(gps['D_DATE'])
lonsize = [np.min(ctdlon), np.max(ctdlon)]
latsize = [np.min(ctdlat), np.max(ctdlat)]


index = []
i = 0
for lat, lon, ctdtm in zip(ctdlat, ctdlon, ctdtime):
    l = dist(lon, lat, gpslon, gpslat)
    p = np.where(l<r)
    maxtime = ctdtm+timedelta(hours=hour)
    mintime = ctdtm-timedelta(hours=hour)
    mx = gpstime[p[0]]<maxtime
    mn = gpstime[p[0]]>mintime
    #print mx,mn
    TF = mx*mn
    if TF.any():
        index.append(i)
    i += 1
    #print(i)
ctd_TF = pd.Series([True]*len(index), index=index)
ctd['TF'] = ctd_TF
#print(ctd)
print('{0} is OK(including "null" lon and lat values.).'.format(len(ctd_TF)/28975.0))#28975 is the length of ctd csv
print('{0} is OK.'.format(len(ctd_TF)/15657.0))
print("save as '%s_merge_td_gps.csv'"%db)
ctd.to_csv(path2 + db+'_merge_td_gps.csv')
