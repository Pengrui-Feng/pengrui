# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:04:05 2019
scatterplot of every database
@author: pengrui
"""
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
from turtleModule import draw_basemap
from matplotlib.mlab import griddata


lonsize = [-78.2, -67.8]#tu102
latsize = [33.1, 42.0]#tu102
#lonsize = [-77.2, -64.8]#tu99
#latsize = [33.8, 42.8]#tu199

color=['g','darkviolet','orange','b','hotpink','c','peru','lime','brown','orangered','k','magenta','r','cyan','gray','y','pink','olive','indigo','coral','plum','violet','salmon','tan','navy','maroon','blue','peachpuff','slateblue','khaki','gold','chocolate',
       'g','darkviolet','orange','b','hotpink','c','peru','lime','brown','orangered','k','magenta','r','cyan','gray','y','pink','olive','indigo','coral','plum','violet','salmon','tan','navy','maroon','blue','peachpuff','slateblue','khaki','gold','chocolate',
       'g','darkviolet','orange','b','hotpink','c','peru','lime','brown','orangered','k','magenta','r','cyan','gray','y','pink','olive','indigo','coral','plum','violet','salmon','tan','navy','maroon','blue','peachpuff','slateblue','khaki','gold','chocolate']
t_ids=[161291, 161292, 161296, 172191, 175934, 175935, 161295, 175939,161299, 161303, 161294, 161297, 161298, 161300, 161301, 161304,172179, 172188, 175938, 175932, 175936, 175940, #tu_102
       118940, 118941, 118944, 118947, 118948, 118951, 118943, 118945,118946, 118942, 118952, 118949, 118950, 118953, 118954, #tu_73
       161426, 161427, 161428, 161432, 161433, 161435, 161429, 161436,161437, 161430, 161434, 161439, 161431, 161438, 161440] #tu_99
path1='/home/zdong/PENGRUI/merge/'
path2='/home/zdong/PENGRUI/summary/'

obsdata = pd.read_csv(path1+'tu102_merge_td_gps.csv') # has both observed and modeled profiles
obstime =  pd.Series((datetime.strptime(x, '%m/%d/%y %H:%M:%S') for x in obsdata['END_DATE']))
obsLat=obsdata['lat']
obsLon=obsdata['lon']
obsturtle_id=obsdata['PTT']
ids=obsturtle_id.unique() # this is the interest turtle id
  
fig =plt.figure()
ax = fig.add_subplot(111)
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
            plt.scatter(lon, lat,s=20,c=color[i],linewidths=None,label='id:'+str(ids[j]))  #  
draw_basemap(fig, ax, lonsize, latsize, interval_lon=2, interval_lat=2)    
    
#lon_is = np.linspace(lonsize[0],lonsize[1],150)
#lat_is = np.linspace(latsize[0],latsize[1],150)  #use for depth line
plt.title('tu102_scatterplot')#('%s profiles(%s~%s)'% (e,obsTime[0],obsTime[-1]))
plt.legend(loc='upper left',ncol=2,fontsize = 'xx-small')
plt.savefig(path2+'tu102_ScatterPlot.png',dpi=200)
plt.show()            
