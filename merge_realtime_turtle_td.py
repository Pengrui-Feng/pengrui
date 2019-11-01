'''
Created on 11 Oct  2019
@author: pengrui

merge two csv files from turtles including 1) 'CTD' and 2) 'GPS'
'''
import pandas as pd
from datetime import datetime,timedelta
import csv
from tqdm import tqdm

path1 = '/home/zdong/PENGRUI/get_original_data/'
path2 = '/home/zdong/PENGRUI/data_process/'

df = pd.read_csv(path1 + 'tu102_ctd.csv')
df['END_DATE'] = pd.to_datetime(df['END_DATE'])
df.to_csv(path2 + 'tu102_ctd.csv')

df = pd.read_csv(path1 + 'tu102_gps.csv')
df['D_DATE'] = pd.to_datetime(df['D_DATE'])
df.to_csv(path2 + 'tu102_gps.csv')


dict_ctd = {}
dict_ctd['PTT'] = []
dict_ctd['argos_date'] = []
dict_ctd['TEMP_DBAR'] = []
dict_ctd['TEMP_VALS'] = []
dict_ctd['lat'] = []
dict_ctd['lon'] = []

with open( path2 + 'tu102_ctd.csv','r') as csvfile:
    reader1 = csv.DictReader(csvfile)
    for row in reader1:
        dict_ctd['PTT'].append(row['PTT'])
        dict_ctd['argos_date'].append(row['END_DATE'])
        dict_ctd['TEMP_DBAR'].append(row['TEMP_DBAR'])
        dict_ctd['TEMP_VALS'].append(row['TEMP_VALS'])
        dict_ctd['lat'].append(row['lat'])
        dict_ctd['lon'].append(row['lon'])
        #print(row['PTT'], row['END_DATE'])         
        #argos_date,argos_time = row['END_DATE'].split(' ')
        #argo_date,argo_time = row['END_DATE'].split(' ')
        #dict_ctd['argos_date'].append(argo_date)
        #dict_ctd['argos_time'].append(argo_time)


dict_gps = {}
dict_gps['PTT'] = []
dict_gps['gps_date'] = []
dict_gps['LAT'] = []
dict_gps['LON'] = []

with open( path2 + 'tu102_gps.csv','r') as csvfile:
    reader2 = csv.DictReader(csvfile)
    for row in reader2:
        dict_gps['PTT'].append(row['PTT'])
        dict_gps['gps_date'].append(row['D_DATE'])
        dict_gps['LAT'].append(row['LAT'])
        dict_gps['LON'].append(row['LON'])
        #print(row['PTT'], row['D_DATE'], row['LAT'], row['LON'])
        #gps_date, gps_time = row['D_DATE'].split(' ')
        #dict_gps['gps_date'].append(gps_date)
        #dict_gps['gps_time'].append(gps_time)


 
#create a new dictionary
final_dict = {}
final_dict['PTT'] = []
final_dict['argos_date'] = []
final_dict['TEMP_DBAR'] = []
final_dict['TEMP_VALS'] = []
final_dict['lat'] = []
final_dict['lon'] = []
final_dict['gps_date'] = []
final_dict['LAT'] = []
final_dict['LON'] = []
num=0
#split cols to get one row for each depth
for i,(ctd_ptt,argos_date) in enumerate(tqdm(zip(dict_ctd['PTT'],dict_ctd['argos_date']))):
    for j,(gps_ptt,gps_date) in enumerate(zip(dict_gps['PTT'],dict_gps['gps_date'])):
        if(ctd_ptt == gps_ptt and abs((datetime.strptime(argos_date,"%Y-%m-%d %H:%M:%S") - datetime.strptime(gps_date,"%Y-%m-%d %H:%M:%S")).total_seconds()) < 3600*3) :
            list_dbar = dict_ctd['TEMP_DBAR'][i].split(',')
            list_vals = dict_ctd['TEMP_VALS'][i].split(',')
            num += 1
            #print('split result',list_dbar,list_vals)
            for dbar, vals in zip(list_dbar,list_vals):
                final_dict['PTT'].append(ctd_ptt)
                final_dict['argos_date'].append(dict_ctd['argos_date'][i])
                #final_dict['argos_time'].append(dict_ctd['argos_time'][i])
                final_dict['TEMP_DBAR'].append(dbar)
                final_dict['TEMP_VALS'].append(vals)
                final_dict['LAT'].append(dict_gps['LAT'][j])
                final_dict['LON'].append(dict_gps['LON'][j])
                final_dict['gps_date'].append(dict_gps['gps_date'][j])
                #final_dict['gps_time'].append(dict_gps['gps_time'][j])
                final_dict['lat'].append(dict_ctd['lat'][i])
                final_dict['lon'].append(dict_ctd['lon'][i])
                
            #break

#final_dict['PTT'],final_dict['END_DATE'] ,final_dict['TEMP_DBAR'],final_dict['TEMP_VALS'] ,final_dict['lat'],final_dict['lon'] ,final_dict['D_DATE'],final_dict['LAT'] ,final_dict['LON']

with open(path2 +'combined_td_gps.csv','w') as csvfile:
    #fieldnames = ['PTT', 'argos_date', 'TEMP_DBAR', 'TEMP_VALS', 'lat', 'lon', 'D_DATE', 'LAT', 'LON']
    fieldnames = ['PTT', 'argos_date', 'depth', 'temp', 'lat_gps', 'lon_gps', 'gps_date','lat_argos', 'lon_argos']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
   
    for ptt,argos_date,dbar,vals,lat,lon,gps_date,lat1,lon1 in tqdm(zip(final_dict['PTT'],final_dict['argos_date'],
    final_dict['TEMP_DBAR'],final_dict['TEMP_VALS'] ,final_dict['lat'],
    final_dict['lon'] ,final_dict['gps_date'],final_dict['LAT'] ,final_dict['LON'])) :
        writer.writerow({'PTT': ptt, 'argos_date':argos_date, 'depth':dbar, 'temp':vals, 'lat_gps':lat1, 'lon_gps':lon1, 'gps_date':gps_date, 'lat_argos':lat, 'lon_argos':lon})
  

