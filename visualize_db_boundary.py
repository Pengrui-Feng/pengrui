# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 11:08:58 2019

@author: pengrui
"""
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
from turtleModule import draw_basemap
from matplotlib.mlab import griddata
import glob
import time
import csv
lonsize = [-90, 0]
latsize = [25, 70]
color=['g','darkviolet','orange','b','hotpink','r','peru','lime']
fig =plt.figure()
ax = fig.add_subplot(111)
csv_list = glob.glob('*_Summary.csv') #
print('%s csvfiles searched in total'% len(csv_list))
k=0
for g in csv_list: #
    df = pd.read_csv(g)
    #df = pd.read_csv('/home/zdong/PENGRUI/summary/Summary_tu99.csv',parse_dates=['start_date','end_date'])
    latmin= df['lat_min'].min()
    lonmin= df['lon_min'].min()
    latmax= df['lat_max'].max()
    lonmax= df['lon_max'].max()
    plt.plot([lonmin,lonmax,lonmax,lonmin,lonmin],[latmin,latmin,latmax,latmax,latmin],color=color[k])    
    plt.text(lonmax,latmax,csv_list[k],size=13,color=color[k])
    k+=1
draw_basemap(fig, ax, lonsize, latsize, interval_lon=20, interval_lat=10)    
plt.title('database_boundary_comparison')
plt.savefig('database_boundary_comparison.png',dpi=200)
plt.show() 
