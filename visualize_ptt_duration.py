# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:42:22 2019
plot and display ptt-date
@author: pengrui
"""
import matplotlib.dates as dt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

db= 'tu73' #tu73,tu74,tu94,tu98,tu99,tu102
path1='/home/zdong/PENGRUI/summary/'
path2='/home/zdong/PENGRUI/visualize/'

df = pd.read_csv(path1+db+'_Summary.csv')
ptt = df['PTT']
tracks=df['length_of_track']
start = df['start_date']
end = df['end_date']

fig =plt.figure()
for i in df.index:
    s = datetime.strptime(start[i], '%Y-%m-%d %H:%M:%S').date()
    e = datetime.strptime(end[i], '%Y-%m-%d %H:%M:%S').date()
    ss = dt.date2num(s)
    ee = dt.date2num(e)
    plt.plot([ss,ee],[i,i], marker = ".")
    #plt.text(ss,i,tracks[i],size=6)
ax = plt.gca()
formatter = dt.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(formatter)
ax.xaxis.grid(True)  
ax.yaxis.grid(True)
firstdays=dt.MonthLocator() # 获取每月第一日数据
locate=dt.MonthLocator(range(1, 13), bymonthday=1, interval=3) # 获取每3个月第一日数据

ax.xaxis.set_major_locator(locate) # 设定主刻度
ax.xaxis.set_minor_locator(firstdays) # 设定次刻度

fig.autofmt_xdate() # 自动旋转xlabel 
plt.tick_params(axis='y', which='both', labelright='on') # 
#tu73,tu74,tu94,tu98,tu99,tu102
plt.yticks([-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],['PTT','118940','118941','118942','118943','118944','118945','118946','118947','118948','118949','118950','118951','118952','118953','118954']) #tu_73
#plt.yticks([-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],['PTT','118884','118885','118886','118887','118888','118889','118890','118891','118892','118893','118894','118895','118896','118897','118898','118899','118900','118901','118902','118903','118904','118905','118906','118913']) #tu74
#plt.yticks([-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13],['PTT','118905','149443','149445','149446','149447','149448','149449','149450','151557','151558','151559','151560','151561']) #tu94
#plt.yticks([-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],['PTT','159795','159796','161293','161302','161305','161441','161442','161443','161444','161445','172177','172178','172180','172181','172182','172183','172184','172185','172186','172187','172189','172190','172192','172193','172194','172196'])#tu98
#plt.yticks([-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],['PTT','161426','161427','161428','161429','161430','161431','161432','161433','161434','161435','161436','161437','161438','161439','161440'])#tu99
#plt.yticks([-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21],['PTT','161291','161292','161295','161296','161297','161298','161299','161300','161301','161303','161304','172179','172188','172191','175932','175934','175935','175936','175938','175939','175940'])#tu102

plt.title('%s_ptt_duration'%db)
plt.savefig(path2+db+'_ptt_duration.png',dpi=200)
plt.show()
