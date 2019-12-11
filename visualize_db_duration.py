# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 09:36:10 2019

@author: pengrui
"""
import matplotlib.dates as dt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import glob
import time
import csv
#path1='/home/zdong/PENGRUI/summary/'
csv_list = glob.glob('*_Summary.csv') #打开文件夹下全部的CSV文件
print('%s csvfiles searched in total'% len(csv_list))
#time.sleep(2)
print('processing............')
fig =plt.figure()
color=['g','r','m','brown','b','gray','peru']
k=0
for i in csv_list: #i既是正在处理的文件名
    df = pd.read_csv(i)
    ptt = df['PTT']
    tracks=df['length_of_track']
    start = df['start_date']
    end = df['end_date']
    for j in df.index:
        s = datetime.strptime(start[j], '%Y-%m-%d %H:%M:%S').date()
        e = datetime.strptime(end[j], '%Y-%m-%d %H:%M:%S').date()
        ss = dt.date2num(s)
        ee = dt.date2num(e)
        plt.plot([ss,ee],[j,j], marker = ".",color=color[k])
    a=csv_list[k].find('_')
    plt.text(ss,j,csv_list[k][0:a],size=14,color=color[k])       
    k+=1

ax = plt.gca()
formatter = dt.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(formatter)
ax.xaxis.grid(True)  
ax.yaxis.grid(True)
firstdays=dt.MonthLocator() # 获取每月第一日数据
locate=dt.MonthLocator(range(1, 13), bymonthday=1, interval=6) # 获取每3个月第一日数据

ax.xaxis.set_major_locator(locate) # 设定主刻度
ax.xaxis.set_minor_locator(firstdays) # 设定次刻度
plt.yticks([-1,26],['',''])
fig.autofmt_xdate() # 自动旋转xlabel 
plt.tick_params(axis='y', which='both', labelright='on')
plt.title('database_duration_comparison')
plt.savefig('visualize_db_duration.png',dpi=200)
print('Finish！')
