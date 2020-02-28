''' 
SCRAPPING 

http://digidb.io/digimon-list 
- json 
- csv 
- excel 
- mogodb db=digimon col=digimon
''' 
import json 
import csv 
import xlsxwriter 
import pymongo
import requests 
from bs4 import BeautifulSoup 

url = 'http://digidb.io/digimon-list'  
html = requests.get(url) 
soup = BeautifulSoup(html.content, "html.parser") 

table_header = soup.find_all("th")
table_tbody = soup.find("tbody")
table_tr = table_tbody.find_all("tr") 

list_header=["No", "Link"]
for i in table_header[1:]: 
    list_header.append(i.text)

list_data = []
for i in table_tr: 
    list_tampung = []
    table_td = i.find_all("td") 
    for a in table_td[1:]:
        tampung = a.text 
        if "\xa0 " in tampung: 
            tampung = tampung.replace(u'\xa0 ',u'')
        list_tampung.append(tampung)
    list_data.append(list_tampung)

table_img = table_tbody.find_all("img")  

imagesrc = [] 
for i in table_img: 
    imagesrc.append(i['src'])

j = 0

for i in list_data:  
    i.insert(0,imagesrc[j]) 
    i.insert(0,j+1)
    list_data[j] = i 
    j+=1


# print(list_data)

#CSV
list_data_csv = list_data 
list_data_csv.insert(0,list_header) 
# print(list_data_csv)

# with open("csvDigimon.csv", "w") as mycsv: 
#     writer = csv.writer(mycsv, delimiter = ",")
#     writer.writerows(list_data_csv)

#JSON 

list_data_json = [] 
for i in list_data[1:]: 
    tes = zip(list_header, i)
    dicttes = dict(tes)
    list_data_json.append(dicttes)

# with open("jsonDigimon.json", "w") as myjson: 
#     json.dump(list_data_json, myjson, indent=2)

#EXCEL 

# book = xlsxwriter.Workbook("ExcelDigimon.xlsx") 
# sheet = book.add_worksheet("DatabaseDigimon")

# row = 0 
# for row in range(len(list_data_csv)): 
#     for col in range(len(list_data_csv[row])): 
#         sheet.write(row,col,list_data_csv[row][col])

# book.close()

#MONGODB

urldb = "mongodb://127.0.0.1:27017"
mongoku = pymongo.MongoClient(urldb) 
dbabc = mongoku['digimon']
coldigimon = dbabc['DigimonList'] 

coldigimon.insert_many(list_data_json)

# print(list(coldigimon.find()))  