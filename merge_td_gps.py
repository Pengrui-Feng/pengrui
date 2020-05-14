'''
Created on 11 Oct  2019
@author: pengrui
merge two csv files from turtles including 1) 'CTD' and 2) 'GPS'
output results including split and nosplit
'''
import pandas as pd
from datetime import datetime,timedelta
import csv
from tqdm import tqdm
######hardcode########
db= 'tu109' #tu55,63,67,68,69,73,74,75,80,84,86,87,88,91,92,94,98,99,102,109
path1 = '/content/drive/My Drive/PENGRUI/get_original_data/' 
path2 = '/content/drive/My Drive//PENGRUI/merge_split/'
path3 = '/content/drive/My Drive/PENGRUI/merge_nosplit/'
hour=3 #match ctd and gps in 3 hours

#convert time format
df = pd.read_csv(path1 + db+'_ctd.csv') 
df['END_DATE'] = pd.to_datetime(df['END_DATE'])
df.rename(columns = {"LAT": "lat",'LON':'lon'},inplace=True) #tu73,tu74
df=df.dropna(subset=['lat'])
df.to_csv(path1 + db+'_ctd.csv')

df = pd.read_csv(path1 + db+'_gps.csv')
df['D_DATE'] = pd.to_datetime(df['D_DATE'])
df=df.dropna(subset=['PTT'])
df.to_csv(path1 + db+'_gps.csv')

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
for i in range(len(dict_ctd['PTT'])):
  dict_ctd['PTT'][i]=int(float(dict_ctd['PTT'][i]))
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
for i in range(len(dict_gps['PTT'])):
  dict_gps['PTT'][i]=int(float(dict_gps['PTT'][i]))

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
print("\nmin time computing,about 2 minites: ")
time_dict = {}
for ctd_ptt,argos_date in tqdm(zip(dict_ctd['PTT'],dict_ctd['argos_date'])):
    diff_time = []
    for gps_ptt,gps_date in zip(dict_gps['PTT'],dict_gps['gps_date']):
        if(ctd_ptt == gps_ptt and  abs((datetime.strptime(argos_date, "%Y-%m-%d %H:%M:%S") - datetime.strptime(gps_date, "%Y-%m-%d %H:%M:%S")).total_seconds()) < hour*3600):
            timediff = abs((datetime.strptime(argos_date, "%Y-%m-%d %H:%M:%S") -  datetime.strptime(gps_date, "%Y-%m-%d %H:%M:%S")).total_seconds())
            diff_time.append(timediff)
    if ctd_ptt not in time_dict.keys():
        time_dict[ctd_ptt] = {}
    time_dict[ctd_ptt][argos_date]=diff_time


print("\nmerging csv,about 2 minites: ")
num=0
tmp_ptt = dict_ctd['PTT'][0]
for i,(ctd_ptt,argos_date) in tqdm(enumerate(zip(dict_ctd['PTT'],dict_ctd['argos_date']))):
    if ctd_ptt != tmp_ptt:
        num = 0
        tmp_ptt = ctd_ptt
#split cols to get one row for each depth
    for j,(gps_ptt,gps_date) in enumerate(zip(dict_gps['PTT'],dict_gps['gps_date'])):
        if(ctd_ptt == gps_ptt and  abs((datetime.strptime(argos_date, "%Y-%m-%d %H:%M:%S") - datetime.strptime(gps_date, "%Y-%m-%d %H:%M:%S")).total_seconds()) < hour*3600):
            timediff = abs((datetime.strptime(argos_date, "%Y-%m-%d %H:%M:%S") - datetime.strptime(gps_date, "%Y-%m-%d %H:%M:%S")).total_seconds())
            min_timediff = min(time_dict[ctd_ptt][argos_date])
            if timediff != min_timediff:
                continue         
            list_dbar = dict_ctd['TEMP_DBAR'][i].split(',')
            list_vals = dict_ctd['TEMP_VALS'][i].split(',')
            num += 1
            for dbar, vals in zip(list_dbar,list_vals):
                final_dict['num'].append(num)
                final_dict['PTT'].append(ctd_ptt)
                final_dict['argos_date'].append(dict_ctd['argos_date'][i])
                final_dict['TEMP_DBAR'].append(dbar)
                final_dict['TEMP_VALS'].append(vals)
                final_dict['LAT'].append(dict_gps['LAT'][j])
                final_dict['LON'].append(dict_gps['LON'][j])
                final_dict['gps_date'].append(dict_gps['gps_date'][j])
                final_dict['lat'].append(dict_ctd['lat'][i])
                final_dict['lon'].append(dict_ctd['lon'][i])
            break

print("\nwriting file: ")
with open(path2+db+'_merge_split.csv','w') as csvfile:
    fieldnames = ['dive_num','PTT', 'argos_date', 'depth', 'temp','lat_argos', 'lon_argos','gps_date','lat_gps', 'lon_gps']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
   
    for num,ptt,argos_date,dbar,vals,lat1,lon1,gps_date,lat,lon in zip(final_dict['num'],final_dict['PTT'],final_dict['argos_date'],
    final_dict['TEMP_DBAR'],final_dict['TEMP_VALS'] ,final_dict['LAT'] ,final_dict['LON'] ,final_dict['gps_date'],final_dict['lat'],
    final_dict['lon']) :
        writer.writerow({'dive_num':num,'PTT': ptt, 'argos_date':argos_date, 'depth':dbar, 'temp':vals, 'lat_argos':lat, 'lon_argos':lon, 'gps_date':gps_date,'lat_gps':lat1, 'lon_gps':lon1 })

###convert to nosplit
df=pd.read_csv(path2+db+'_merge_split.csv')
df['depth'] = df['depth'].astype('str')
df['temp']= df['temp'].astype('str')
df=df.groupby(['dive_num','PTT','argos_date','lat_argos','lon_argos','gps_date','lat_gps','lon_gps'])['depth','temp'].agg(lambda x:x.str.cat(sep=','))
df.to_csv(path3+db+'_merge_td_gps.csv')
df=pd.read_csv('/content/drive/My Drive/PENGRUI/merge_nosplit/'+db+'_merge_td_gps.csv')
df=df[['PTT','dive_num','gps_date','lat_gps','lon_gps','depth','temp','argos_date','lat_argos','lon_argos']]
df.to_csv('/content/drive/My Drive/PENGRUI/merge_nosplit/'+db+'_merge_td_gps.csv')
