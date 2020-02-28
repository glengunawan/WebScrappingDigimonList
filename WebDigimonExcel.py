import xlsxwriter
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
    i.insert(1,j+1)
    list_data[j] = i 
    j+=1

#EXCEL 

#ADD HEADER KE LIST
list_data_excel = list_data 
list_data_excel.insert(0,list_header) 

book = xlsxwriter.Workbook("ExcelDigimon.xlsx") 
sheet = book.add_worksheet("DatabaseDigimon")

row = 0 
for row in range(len(list_data_excel)): 
    for col in range(len(list_data_excel[row])): 
        sheet.write(row,col,list_data_excel[row][col])

book.close()