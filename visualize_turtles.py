#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 14:26:35 2019

@author: pengrui
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from turtleModule import np_datetime

obsData = pd.read_csv('/home/zdong/PENGRUI/data_process/combined_td_gps.csv')
obsturtle_id=pd.Series(obsData['PTT'])
obsturtle_ids=obsturtle_id.unique()   

ids=[]    #collect all indexes of each turtle
for i in range(len(obsturtle_ids)):
    ids.append([])
    for j in range(len(obsturtle_id)):
        if obsturtle_id[j]==obsturtle_ids[i]:
            ids[i].append(j)  






















fig=plt.figure()
plt.figure(xnew,ynew,align="center",width=width,color='green')
plt.xlim([0,700])
plt.ylim([0,12]) 
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.xlabel('number of days',fontsize=10)
plt.ylabel('Number of turtle',fontsize=10)
plt.title(str(ave_day)+'  average #day of profile with standard deviation of '+str(std_day),fontsize=12)
plt.savefig('days of profile_try(all data).png')
plt.show()
