import mysql.connector 
import requests
from bs4 import BeautifulSoup

url = 'http://digidb.io/digimon-list'  
html = requests.get(url) 
soup = BeautifulSoup(html.content, "html.parser") 

#TABEL
table_tbody = soup.find("tbody")
table_tr = table_tbody.find_all("tr") 

#AMBIL DATA TABEL
list_data = []
for i in table_tr: 
    list_tampung = []
    table_td = i.find_all("td")
    for a in table_td[1:]:
        tampung = a.text.replace(u'\xa0 ',u'')
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
    i.insert(0,imagesrc[j]) 
    i.insert(0,j+1)
    list_data[j] = i 
    j+=1

#CREATE LIST OF TUPLES 
list_tuple = [tuple(l) for l in list_data]

dbDigimon = mysql.connector.connect( 
    host = 'localhost', 
    port = '3306', 
    user = 'root', 
    passwd = '***',
    database = 'digimon'
)

x = dbDigimon.cursor()

query = 'CREATE TABLE IF NOT EXISTS DigimonList (Num int, Link varchar(100), Digimon varchar(50), Stage varchar(20), Tipe varchar(20), Attribute varchar(20), Memori int, EquipSlots int, HP int, SP int, Atk int, Def int, Intelligence int, Spd int);'
x.execute(query)

queryku = 'insert into DigimonList values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' 
x.executemany(queryku,list_tuple)
dbDigimon.commit() 
print(x.rowcount, "data sukses tersimpan")