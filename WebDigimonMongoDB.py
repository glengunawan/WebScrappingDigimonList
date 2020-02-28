import pymongo
import requests
from bs4 import BeautifulSoup

url = 'http://digidb.io/digimon-list'  
html = requests.get(url) 
soup = BeautifulSoup(html.content, "html.parser") 

#TABEL
table_header = soup.find_all("th")
table_tbody = soup.find("tbody")
table_tr = table_tbody.find_all("tr") 

#AMBIL HEADER
list_header=["No", "Link"]
for i in table_header[1:]: 
    list_header.append(i.text)

#AMBIL DATA TABEL
list_data = []
for i in table_tr: 
    list_tampung = []
    table_td = i.find_all("td") 
    for a in table_td:
        tampung = a.text.replace('\xa0','')
        list_tampung.append(tampung)
    list_data.append(list_tampung)

#AMBIL LINK IMAGE
table_img = table_tbody.find_all("img")  
imagesrc = [] 
for i in table_img: 
    imagesrc.append(i['src'])

#MASUKIN LINK IMAGE KE LIST TABEL
j = 0
for i in list_data:  
    i.insert(1,imagesrc[j]) 
    list_data[j] = i 
    j+=1


#CREATE LIST OF DICTIONARY
list_data_mongoDB = [] 
for i in list_data: 
    tes = zip(list_header, i)
    dicttes = dict(tes)
    list_data_mongoDB.append(dicttes)


#MONGODB

urldb = "mongodb://127.0.0.1:27017"
mongoku = pymongo.MongoClient(urldb) 
dbabc = mongoku['digimon']
coldigimon = dbabc['DigimonList'] 

coldigimon.insert_many(list_data_mongoDB)