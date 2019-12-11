'''
Created on 11 Oct  2019
@author: pengrui

merge two csv files from turtles including 1) 'CTD' and 2) 'GPS'
'''
import pandas as pd
from datetime import datetime,timedelta
import csv
#from tqdm import tqdm
db= 'tu99' #tu73,tu74,tu94,tu98,tu99,tu102
path1 = '/home/zdong/PENGRUI/get_original_data/'
path2 = '/home/zdong/PENGRUI/merge/'

#convert time format
df = pd.read_csv(path1 + db+'_ctd.csv')
df['END_DATE'] = pd.to_datetime(df['END_DATE'])
df.rename(columns = {"LAT": "lat",'LON':'lon'},inplace=True) #tu73,tu74
df.to_csv(path2 + db+'_ctd.csv')

df = pd.read_csv(path1 + db+'_gps.csv')
df['D_DATE'] = pd.to_datetime(df['D_DATE'])
df.to_csv(path2 + db+'_gps.csv')

#read ctd and gps csv files
dict_ctd = {}
dict_ctd['PTT'] = []
dict_ctd['argos_date'] = []
dict_ctd['TEMP_DBAR'] = []
dict_ctd['TEMP_VALS'] = []
dict_ctd['lat'] = []
dict_ctd['lon'] = []

with open( path2 + db+'_ctd.csv','r') as csvfile:
    reader1 = csv.DictReader(csvfile)
    for row in reader1:
        dict_ctd['PTT'].append(row['PTT'])
        dict_ctd['argos_date'].append(row['END_DATE'])
        dict_ctd['TEMP_DBAR'].append(row['TEMP_DBAR'])
        dict_ctd['TEMP_VALS'].append(row['TEMP_VALS'])
        dict_ctd['lat'].append(row['lat'])
        dict_ctd['lon'].append(row['lon'])        

dict_gps = {}
dict_gps['PTT'] = []
dict_gps['gps_date'] = []
dict_gps['LAT'] = []
dict_gps['LON'] = []

with open( path2 + db+'_gps.csv','r') as csvfile:
    reader2 = csv.DictReader(csvfile)
    for row in reader2:
        dict_gps['PTT'].append(row['PTT'])
        dict_gps['gps_date'].append(row['D_DATE'])
        dict_gps['LAT'].append(row['LAT'])
        dict_gps['LON'].append(row['LON'])


#create a new final dictionary
final_dict = {}
final_dict['num'] = []
final_dict['PTT'] = []
final_dict['argos_date'] = []
final_dict['TEMP_DBAR'] = []
final_dict['TEMP_VALS'] = []
final_dict['lat'] = []
final_dict['lon'] = []
final_dict['gps_date'] = []
final_dict['LAT'] = []
final_dict['LON'] = []

#compute min time diffirence to avoid multiple iterations
print("\n%s min time computing,about 2 minites: "%db)
time_dict = {}
for ctd_ptt,argos_date in zip(dict_ctd['PTT'],dict_ctd['argos_date']):
    diff_time = []
    for gps_ptt,gps_date in zip(dict_gps['PTT'],dict_gps['gps_date']):
        if(ctd_ptt == gps_ptt and  abs((datetime.strptime(argos_date, "%Y-%m-%d %H:%M:%S") - datetime.strptime(gps_date, "%Y-%m-%d %H:%M:%S")).total_seconds()) < 3600*3):
            timediff = abs((datetime.strptime(argos_date, "%Y-%m-%d %H:%M:%S") -  datetime.strptime(gps_date, "%Y-%m-%d %H:%M:%S")).total_seconds())
            diff_time.append(timediff)
    if ctd_ptt not in time_dict.keys():
        time_dict[ctd_ptt] = {}
    time_dict[ctd_ptt][argos_date]=diff_time


print("\n%s merging csv,about 2 minites: "%db)
num=0
tmp_ptt = dict_ctd['PTT'][0]
for i,(ctd_ptt,argos_date) in enumerate(zip(dict_ctd['PTT'],dict_ctd['argos_date'])):
    if ctd_ptt != tmp_ptt:
        num = 0
        tmp_ptt = ctd_ptt
    for j,(gps_ptt,gps_date) in enumerate(zip(dict_gps['PTT'],dict_gps['gps_date'])):
        if(ctd_ptt == gps_ptt and  abs((datetime.strptime(argos_date, "%Y-%m-%d %H:%M:%S") - datetime.strptime(gps_date, "%Y-%m-%d %H:%M:%S")).total_seconds()) < 3600*3):
            timediff = abs((datetime.strptime(argos_date, "%Y-%m-%d %H:%M:%S") - datetime.strptime(gps_date, "%Y-%m-%d %H:%M:%S")).total_seconds())
            min_timediff = min(time_dict[ctd_ptt][argos_date])
            if timediff != min_timediff:
                continue         
            #list_dbar = dict_ctd['TEMP_DBAR'][i]#.split(',')
            #list_vals = dict_ctd['TEMP_VALS'][i]#.split(',')
            num += 1
            #for dbar, vals in zip(list_dbar,list_vals):
            final_dict['num'].append(num)
            final_dict['PTT'].append(ctd_ptt)
            final_dict['argos_date'].append(dict_ctd['argos_date'][i])
            final_dict['TEMP_DBAR'].append(dict_ctd['TEMP_DBAR'][i])
            final_dict['TEMP_VALS'].append(dict_ctd['TEMP_VALS'][i])
            final_dict['LAT'].append(dict_gps['LAT'][j])
            final_dict['LON'].append(dict_gps['LON'][j])
            final_dict['gps_date'].append(dict_gps['gps_date'][j])
            final_dict['lat'].append(dict_ctd['lat'][i])
            final_dict['lon'].append(dict_ctd['lon'][i])

print("\n%s outputting file: "%db)
with open(path2 +db+'_merge_td_gps.csv','w') as csvfile:
    fieldnames = ['dive_num','PTT', 'argos_date', 'depth', 'temp','lat_argos', 'lon_argos','gps_date','lat_gps', 'lon_gps']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
   
    for num,ptt,argos_date,dbar,vals,lat1,lon1,gps_date,lat,lon in zip(final_dict['num'],final_dict['PTT'],final_dict['argos_date'],
    final_dict['TEMP_DBAR'],final_dict['TEMP_VALS'] ,final_dict['LAT'] ,final_dict['LON'] ,final_dict['gps_date'],final_dict['lat'],
    final_dict['lon']) :
        writer.writerow({'dive_num':num,'PTT': ptt, 'argos_date':argos_date, 'depth':dbar, 'temp':vals, 'lat_argos':lat, 'lon_argos':lon, 'gps_date':gps_date,'lat_gps':lat1, 'lon_gps':lon1 })

