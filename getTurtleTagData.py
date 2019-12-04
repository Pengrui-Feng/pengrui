# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 12:59:27 2019

@author: Jon ONeil
modified by Pengrui in Sep 30 without hardcodes testing one database "tu102"
found it needed sudo apt-get install mdb-tools
"""
import tqdm
import requests
import zipfile
import io
import subprocess
import os
#from turtle_email import send_turtle_email

 
def exportCSVFiles(db):
    #database = '/home/joneil/PycharmProjects/turtle_tag/' + db + ".mdb"
    database = db + ".mdb"
    #database = "tu84.mdb"

    # Get the list of table names with "mdb-tables"
    table_names = subprocess.Popen(["mdb-tables", "-1", database],
                                   stdout=subprocess.PIPE).communicate()[0]
    tables = table_names.decode().split('\n')

    # Dump each table as a CSV file using "mdb-export",
    # converting " " in table names to "_" for the CSV filenames.
    for table in tables:

        if table != '':
            #filename = '/home/joneil/PycharmProjects/turtle_tag/' + db + "_" + table.replace(" ", "_") + ".csv"
            filename =  '/home/zdong/PENGRUI/get_original_data/'+db + "_" + table.replace(" ", "_") + ".csv"
            file = open(filename, 'wb')
            print("Dumping " + db + " " + table)
            contents = subprocess.Popen(["mdb-export", database, table],
                                        stdout=subprocess.PIPE).communicate()[0]
            file.write(contents)
            file.close()
            #os.system("scp " + filename + " joneil@sole.nefsc.noaa.gov:/external_ora_data/turtle_data/")

#create the URLs to feed to the getAccessFiles function to download the zip files
def createURL (filename):
        url = 'http://www.smru.st-and.ac.uk/protected/' + filename + '/db/' + filename + '.zip'
        return url

def getAccessFiles(url, username, password):
    r = requests.get(url, auth=(username, password),stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    #z.extractall(path='/home/joneil/PycharmProjects/turtle_tag/')
    z.extractall(path='')

user_pw_file = [
    #['barco', 'virginia', 'tu69'],
    #['barco', 'virginia', 'tu75'],
    #['ron','farm','tu80'],
    #['barco','virginia','tu84'],
    #['ron','farm','tu86'],
    #['ron','farm','tu87'],
    #['barco','virginia','tu88'],
    #['ron','farm','tu92'],
    ['haas', 'heather','tu73'],
    ['haas', 'heather', 'tu74'],
    ['haas','heather','tu94'],
    ['haas','heather','tu94c'],
    ['haas','heather','tu98'],
    ['haas','heather','tu99'],
    ['haas','heather','tu102']
]
'''
user_pw_file = ['haas','heather','tu73']

# Download and export MS Access files to CSV format by table.
'''
for accessinfo in user_pw_file:
    getAccessFiles(createURL(accessinfo[2]),accessinfo[0],accessinfo[1])
    exportCSVFiles(accessinfo[2])
'''
getAccessFiles(createURL(user_pw_file[2]),user_pw_file[0],user_pw_file[1])
exportCSVFiles(user_pw_file[2])
'''
