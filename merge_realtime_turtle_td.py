'''
Created on 11 Oct  2019
@author: pengrui

merge two csv files from turtles including 1) 'CTD' and 2) 'GPS'
'''

import csv

#creat dictionaries and read two csv files

path= '/home/zdong/PENGRUI/original_data/'

dict_ctd = {}
dict_ctd['PTT'] = []
dict_ctd['END_DATE'] = []
dict_ctd['argos_date'] = []
dict_ctd['argos_time'] = []
dict_ctd['TEMP_DBAR'] = []
dict_ctd['TEMP_VALS'] = []
dict_ctd['lat'] = []
dict_ctd['lon'] = []

with open( path+ 'tu102_ctd.csv','r') as csvfile:
    reader1 = csv.DictReader(csvfile)
    for row in reader1:
        dict_ctd['PTT'].append(row['PTT'])
        dict_ctd['END_DATE'].append(row['END_DATE'])
        dict_ctd['TEMP_DBAR'].append(row['TEMP_DBAR'])
        dict_ctd['TEMP_VALS'].append(row['TEMP_VALS'])
        dict_ctd['lat'].append(row['lat'])
        dict_ctd['lon'].append(row['lon'])
        argos_date,argos_time=row['END_DATE'].split(' ')
        dict_ctd['argos_date'].append(argos_date)
        dict_ctd['argos_time'].append(argos_time)

dict_gps = {}
dict_gps['PTT'] = []
dict_gps['D_DATE'] = []
dict_gps['gps_date'] = []
dict_gps['gps_time'] = []
dict_gps['LAT'] = []
dict_gps['LON'] = []

with open( path + 'tu102_gps.csv','r') as csvfile:
    reader2 = csv.DictReader(csvfile)
    for row in reader2:
        dict_gps['PTT'].append(row['PTT'])
        dict_gps['D_DATE'].append(row['D_DATE'])
        dict_gps['LAT'].append(row['LAT'])
        dict_gps['LON'].append(row['LON'])              
        gps_date,gps_time = row['D_DATE'].split(' ')
        dict_gps['gps_date'].append(gps_date)
        dict_gps['gps_time'].append(gps_time)

#create a new dictionary
final_dict = {}
final_dict['PTT'] = []
final_dict['argos_date'] = []
final_dict['argos_time'] = []
final_dict['TEMP_DBAR'] = []
final_dict['TEMP_VALS'] = []
final_dict['lat'] = []
final_dict['lon'] = []
final_dict['gps_date'] = []
final_dict['gps_time'] = []
final_dict['LAT'] = []
final_dict['LON'] = []
'''
for i,ctd_date in dict_ctd['argos_date']:
    for j,gps_date in dict_gps['gps_date']:
        if(ctd_date == gps_date):
            final_dict['argos_date'].append(dict_ctd['argos_date'][i])
            final_dict['argos_time'].append(dict_ctd['argos_time'][i])
            final_dict['gps_date'].append(dict_gps['gps_date'][j])
            final_dict['gps_time'].append(dict_gps['gps_time'][j])
'''
#split cols to get one row for each depth
for i,ctd_ptt in enumerate(dict_ctd['PTT']):
    for j,gps_ptt in enumerate(dict_gps['PTT']):
        for ctd_date in dict_ctd['argos_date']:
            for gps_date in dict_gps['gps_date']:
                if(ctd_ptt == gps_ptt and ctd_date == gps_date ):
                    list_dbar = dict_ctd['TEMP_DBAR'][i].split(',')
                    list_vals = dict_ctd['TEMP_VALS'][i].split(',')
                    #print('split result',list_dbar,list_vals)
                    for dbar, vals in zip(list_dbar,list_vals):
                        final_dict['PTT'].append(ctd_ptt)
                        final_dict['argos_date'].append(dict_ctd['argos_date'][i])
                        final_dict['argos_time'].append(dict_ctd['argos_time'][i])
                        final_dict['gps_date'].append(dict_gps['gps_date'][j])
                        final_dict['gps_time'].append(dict_gps['gps_time'][j])
                        final_dict['TEMP_DBAR'].append(dbar)
                        final_dict['TEMP_VALS'].append(vals)
                        final_dict['LAT'].append(dict_gps['LAT'][j])
                        final_dict['LON'].append(dict_gps['LON'][j])
                        final_dict['lat'].append(dict_ctd['lat'][i])
                        final_dict['lon'].append(dict_ctd['lon'][i])
                    

#final_dict['PTT'],final_dict['END_DATE'] ,final_dict['TEMP_DBAR'],final_dict['TEMP_VALS'] ,final_dict['lat'],final_dict['lon'] ,final_dict['D_DATE'],final_dict['LAT'] ,final_dict['LON']
with open('combined_td_gps_.csv','w') as csvfile:
    #fieldnames = ['PTT', 'END_DATE', 'TEMP_DBAR', 'TEMP_VALS', 'lat', 'lon', 'D_DATE', 'LAT', 'LON']
    fieldnames = ['PTT', 'argos_date','argos_time', 'depth', 'temp', 'lat_gps', 'lon_gps', 'gps_date','gps_time', 'lat_argos', 'lon_argos']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
   
    for ptt,argos_date,argos_time,dbar,vals,lat,lon,gps_date,gps_time,lat1,lon1 in zip(final_dict['PTT'],final_dict['argos_date'],final_dict['argos_time'] ,
    final_dict['TEMP_DBAR'],final_dict['TEMP_VALS'] ,final_dict['lat'],
    final_dict['lon'] ,final_dict['gps_date'],final_dict['gps_time'],final_dict['LAT'] ,final_dict['LON']) :
        writer.writerow({'PTT': ptt, 'argos_date':argos_date, 'argos_time':argos_time,'depth':dbar, 'temp':vals, 'lat_gps':lat1, 'lon_gps':lon1, 'gps_date':gps_date,'gps_time':gps_time, 'lat_argos':lat, 'lon_argos':lon})
  

