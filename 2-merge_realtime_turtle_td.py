import csv

path= '/home/zdong/PENGRUI/original_data/'

dict_ctd = {}
dict_ctd["PTT"] = []
dict_ctd["END_DATE"] = []
dict_ctd["TEMP_DBAR"] = []
dict_ctd["TEMP_VALS"] = []
dict_ctd["lat"] = []
dict_ctd["lon"] = []

with open( path+ 'tu102_ctd.csv',"r") as csvfile:
    reader1 = csv.DictReader(csvfile)
    for row in reader1:
        dict_ctd["PTT"].append(row['PTT'])
        dict_ctd["END_DATE"].append(row["END_DATE"])
        dict_ctd["TEMP_DBAR"].append(row["TEMP_DBAR"])
        dict_ctd["TEMP_VALS"].append(row["TEMP_VALS"])
        dict_ctd["lat"].append(row["lat"])
        dict_ctd["lon"].append(row["lon"])
        ##print(row['PTT'], row['END_DATE'], row['TEMP_DBAR'], row['TEMP_VALS'],row["lat"],row["lon"])         

dict_gps = {}
dict_gps["PTT"] = []
dict_gps["D_DATE"] = []
dict_gps["LAT"] = []
dict_gps["LON"] = []

with open( path + 'tu102_gps.csv',"r") as csvfile:
    reader2 = csv.DictReader(csvfile)
    for row in reader2:
        dict_gps["PTT"].append(row["PTT"])
        dict_gps["D_DATE"].append(row["D_DATE"])
        dict_gps["LAT"].append(row["LAT"])
        dict_gps["LON"].append(row["LON"])
        #print(row['PTT'], row['D_DATE'], row['LAT'], row['LON'])         

final_dict = {}
final_dict["PTT"] = []
final_dict["END_DATE"] = []
final_dict["TEMP_DBAR"] = []
final_dict["TEMP_VALS"] = []
final_dict["lat"] = []
final_dict["lon"] = []
final_dict["D_DATE"] = []
final_dict["LAT"] = []
final_dict["LON"] = []

#print(dict_ctd)
#print(dict_gps)
for i,ctd_ptt in enumerate(dict_ctd["PTT"]):
    for j,gps_ptt in enumerate(dict_gps["PTT"]):
        #print("ptt",cts_ptt, gps_ptt)
        if(ctd_ptt == gps_ptt):
            list_dbar = dict_ctd["TEMP_DBAR"][i].split(",")
            list_vals = dict_ctd["TEMP_VALS"][i].split(",")
            #print("split result",list_dbar,list_vals)
            for dbar, vals in zip(list_dbar,list_vals):
                final_dict["PTT"].append(ctd_ptt)
                final_dict["END_DATE"].append(dict_ctd["END_DATE"][i])
                final_dict["TEMP_DBAR"].append(dbar)
                final_dict["TEMP_VALS"].append(vals)
                final_dict["lat"].append(dict_ctd['lat'][i])
                final_dict["lon"].append(dict_ctd['lon'][i])
                final_dict["D_DATE"].append(dict_gps["D_DATE"][j])
                final_dict["LAT"].append(dict_gps["LAT"][j])
                final_dict["LON"].append(dict_gps["LON"][j])
            break

#final_dict["PTT"],final_dict["END_DATE"] ,final_dict["TEMP_DBAR"],final_dict["TEMP_VALS"] ,final_dict["lat"],final_dict["lon"] ,final_dict["D_DATE"],final_dict["LAT"] ,final_dict["LON"]
with open("result.csv","w") as csvfile:
    fieldnames = ['PTT', 'END_DATE', "TEMP_DBAR", "TEMP_VALS", "lat", "lon", "D_DATE", "LAT", "LON"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for ptt,end,dbar,vals,lat,lon,date,lat1,lon1 in zip(final_dict["PTT"],final_dict["END_DATE"] ,
    final_dict["TEMP_DBAR"],final_dict["TEMP_VALS"] ,final_dict["lat"],
    final_dict["lon"] ,final_dict["D_DATE"],final_dict["LAT"] ,final_dict["LON"]):
        writer.writerow({'PTT': ptt, 'END_DATE':end, "TEMP_DBAR":dbar, "TEMP_VALS":vals, "lat":lat, "lon":lon, "D_DATE":date, "LAT":lat1, "LON":lon1})
