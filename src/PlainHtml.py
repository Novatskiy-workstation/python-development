import re
import nltk
import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from nameparser.parser import HumanName
import html
import numpy as np
import mysql.connector
from array import array
from pydoc import plain
import requests
import bs4
from bs4 import BeautifulSoup
import time
start_time = time.time()

config = {
  'user': 'root',
  'password': 'root',
  'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
  'database': 'testdb',
  'raise_on_warnings': True,
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()
if conn.is_connected():
    print("Connected to mysql Database")

cursor.execute("SELECT * FROM TABLE4")

linkfromtable = list(cursor.fetchall())

i = 1
#print(linkfromtable)
for url in linkfromtable:
    print(url[1])
    
    responce = requests.get(url[1])
    #print(responce)
    
    #soup = BeautifulSoup(responce.text,'lxml')
    soup = BeautifulSoup(responce.content,"html.parser")
    
    plainHtml = soup.find("html")
    
    #print(plainHtml)
    
    r = str(plainHtml)
    g = r.replace('"','')
    h = g.replace("'", "")
    #print(h)
    
    newquery="UPDATE TABLE4 set plain_html = '"+h+"' where id = "+str(i)
    cursor.execute(newquery)
    conn.commit()
    i = i+1
    
print("--- %s seconds ---" % (time.time() - start_time))






    
    