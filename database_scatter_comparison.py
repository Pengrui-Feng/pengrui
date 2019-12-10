# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 14:04:05 2019

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

path1='/home/zdong/PENGRUI/merge/'
path2='/home/zdong/PENGRUI/visualize/'

color=['g','darkviolet','orange','b','hotpink','c','peru','lime','brown','orangered','k','magenta','r','cyan','gray','y','pink','olive','indigo','coral','plum','violet','salmon','tan','navy','maroon','blue','peachpuff','slateblue','khaki','gold','chocolate',
'g','darkviolet','orange','b','hotpink','c','peru','lime','brown','orangered','k','magenta','r','cyan','gray','y','pink','olive','indigo','coral','plum','violet','salmon','tan','navy','maroon','blue','peachpuff','slateblue','khaki','gold','chocolate',
'g','darkviolet','orange','b','hotpink','c','peru','lime','brown','orangered','k','magenta','r','cyan','gray','y','pink','olive','indigo','coral','plum','violet','salmon','tan','navy','maroon','blue','peachpuff','slateblue','khaki','gold','chocolate',
'g','darkviolet','orange','b','hotpink','c','peru','lime','brown','orangered','k','magenta','r','cyan','gray','y','pink','olive','indigo','coral','plum','violet','salmon','tan','navy','maroon','blue','peachpuff','slateblue','khaki','gold','chocolate',
'g','darkviolet','orange','b','hotpink','c','peru','lime','brown','orangered','k','magenta','r','cyan','gray','y','pink','olive','indigo','coral','plum','violet','salmon','tan','navy','maroon','blue','peachpuff','slateblue','khaki','gold','chocolate',
'g','darkviolet','orange','b','hotpink','c','peru','lime','brown','orangered','k','magenta','r','cyan','gray','y','pink','olive','indigo','coral','plum','violet','salmon','tan','navy','maroon','blue','peachpuff','slateblue','khaki','gold','chocolate']
t_ids=[118940, 118941, 118944, 118947, 118948, 118951, 118943, 118945,118946, 118942, 118952, 118949, 118950, 118953, 118954, #tu_73
       118884, 118894, 118896, 118885, 118887, 118888, 118889, 118890,118886, 118891, 118893, 118892, 118899, 118901, 118903, 118897,118898, 118900, 118902, 118895, 118906, 118905, 118904, 118913, #tu74
       118905, 149443, 149448, 149449, 149445, 149446, 149447, 151557,151558, 151561, 149450, 151559, 151560,  #tu94
       159795, 159796, 159797, 161305, 161444, 161868, 161293, 161302,161441, 161443, 172178, 172180, 172184, 161442, 161445, 172193,172181, 172189, 172177, 172182, 172183, 172185, 172186, 172187,172190, 172192, 172194, 172196, #tu98
       161426, 161427, 161428, 161432, 161433, 161435, 161429, 161436,161437, 161430, 161434, 161439, 161431, 161438, 161440, #tu_99
       161291, 161292, 161296, 172191, 175934, 175935, 161295, 175939,161299, 161303, 161294, 161297, 161298, 161300, 161301, 161304,172179, 172188, 175938, 175932, 175936, 175940] #tu_102

lonsize = [-78.8, -63.8]#tu99
latsize = [32.8, 42.8]#tu199
csv_list =[glob.glob(path1+'*_merge_td_gps.csv')
print('%s csvfiles searched in total'% len(csv_list))
fig =plt.figure()
ax = fig.add_subplot(111)
k=0
for g in csv_list: #g既是正在处理的文件名
    obsdata = pd.read_csv(g)
    obstime =  pd.Series((datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in obsdata['argos_date']))
    obsLat=obsdata['lat_argos']
    obsLon=obsdata['lon_argos']
    obsturtle_id=obsdata['PTT']
    ids=obsturtle_id.unique() # this is the interest turtle id  
    for j in range(len(ids)):
        indx=[]  # this indx is to get the specifical turtle all index in obsData ,if we use the "where" function ,we just get the length  of tf_index.
        for i in obsdata.index:
            if obsturtle_id[i]==ids[j]:   
                indx.append(i)
            Time = obstime[indx]
            lat = obsLat[indx]
            lon = obsLon[indx]
            for i in range(len(t_ids)): 
                if ids[j]==t_ids[i]:
                    plt.scatter(lon, lat,s=15,c=color[k],linewidths=None)#,label='id:'+str(ids[j]))  #  
    k+=1
draw_basemap(fig, ax, lonsize, latsize, interval_lon=2, interval_lat=2)    

'''
df = pd.read_csv('/home/zdong/PENGRUI/summary/Summary_tu99.csv',parse_dates=['start_date','end_date'])
latmin= df['lat_min'].min()
lonmin= df['lon_min'].min()
latmax= df['lat_max'].max()
lonmax= df['lon_max'].max()
plt.plot([lonmin,lonmax,lonmax,lonmin,lonmin],[latmin,latmin,latmax,latmax,latmin])    
'''  

#plt.title('%s_scatterplot'%db)#('%s profiles(%s~%s)'% (e,obsTime[0],obsTime[-1]))
plt.legend(loc='lower right',ncol=2,fontsize = 'xx-small')
#plt.savefig(path2+'%s_ScatterPlot.png'%db,dpi=200)
plt.show()            
