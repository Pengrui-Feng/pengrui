'''
created on Nov 14 2019
plot
@author: pengrui
'''
import os
import csv
import matplotlib.pyplot as plt

path = ""
shift=4 # offset of profiles in degC
maxdepth = 70
ppt_dict = {}
with open(path+"combined_td_gps.csv","r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if not row["PTT"] in ppt_dict.keys():
            ppt_dict[row["PTT"]] = {}

        if not row["dive_num"] in ppt_dict[row["PTT"]].keys():
            ppt_dict[row["PTT"]][row["dive_num"]] = [[],[]]
        ppt_dict[row["PTT"]][row["dive_num"]][0].append(row["depth"])
        ppt_dict[row["PTT"]][row["dive_num"]][1].append(row["temp"])

for ptt,values in ppt_dict.items():
    fig=plt.figure("%sImage"%ptt)  
    i = 0
    for dive,depth_temp in values.items():
        #plt.gca().invert_yaxis()
        depth_temp[1] = [float(t)+i for t in depth_temp[1]]
        depth_temp[0] = [int(t) for t in depth_temp[0]]
        plt.plot(depth_temp[1],depth_temp[0])
        plt.xticks([])
        i += shift
    plt.gca().invert_yaxis()
    #plt.ylim([maxdepth,1])    
    plt.xticks([])
    plt.xlabel( 'Temperature by time(4 degree offset)',fontsize=14)
    plt.ylabel('Depth(m)', fontsize=14)            
    plt.title('%s'%ptt)
    #plt.savefig(path+'Image/%s#turtle.png'%ptt,dpi=200)
    plt.show()
