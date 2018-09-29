'''
Created on Mar 30, 2018

@author: root
'''

import re 
import re as r
import sys as sys
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
import datetime
from src.util import clean 
from src.exceptions import * 
from src.ik import calc_check_digit, is_valid
from collections import defaultdict
import itertools
from connection import link
from operator import itemgetter
from collections import Counter
from itertools import groupby
import collections
import pandas as pd
import heapq
import itertools
from itertools import groupby
import pprint
from operator import itemgetter
from sys import stdout
from nltk.misc.wordfinder import step

start_time = time.time()

def combine_list(*args):
    return map(list, args)


def group_by_excluding_key(list_of_dicts, key_field):
    """
    Takes a list of `dict` items and groups by ALL KEYS in the dict EXCEPT the key_field.
    :param list_of_dicts: List of dicts to group
    :param key_field: key field in dict which should be excluded from the grouping
    """

    output = []

    for item in list_of_dicts:
        found = False
        item_key = item.pop(key_field)

        for existing_group, found_keys in output:
            if existing_group.viewitems() == item.viewitems():
                found_keys.append(item_key)
                found = True
                break

        if not found:
            output.append((item, [item_key]))

    return output


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' ').strip()


def get_birth_date(number):
    """Split the date parts from the number and return the birth date."""
    number = compact(number)
    if number[0] in '12':
        century = 1800
    elif number[0] in '34':
        century = 1900
    elif number[0] in '56':
        century = 2000
    elif number[0] in '78':
        century = 2100
    else:
        raise InvalidComponent()
    year = century + int(number[1:3])
    month = int(number[3:5])
    day = int(number[5:7])
    try:
        return datetime.date(year, month, day)
    except ValueError:
        raise InvalidComponent()


def get_gender(number):
    """Get the person's birth gender ('M' or 'F')."""
    number = compact(number)
    if number[0] in '1357':
        return 'M'
    elif number[0] in '2468':
        return 'F'
    else:
        raise InvalidComponent()


def calc_check_digit(number):
    """Calculate the check digit."""
    check = sum(((i % 9) + 1) * int(n)
                for i, n in enumerate(number[:-1])) % 11
    if check == 10:
        check = sum((((i + 2) % 9) + 1) * int(n)
                    for i, n in enumerate(number[:-1])) % 11
    return str(check % 10)


def validate(number):
    """Check if the number provided is valid. This checks the length,
    formatting, embedded date and check digit."""
    number = compact(number)
    if not number.isdigit():
        raise InvalidFormat()
    if len(number) != 11:
        raise InvalidLength()
    get_birth_date(number)
    if number[-1] != calc_check_digit(number):
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number provided is valid. This checks the length,
    formatting, embedded date and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False




class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()









config = {
  'user': 'root',
  'password': 'root',
  'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
  'database': 'testdb',
  'raise_on_warnings': True,
}



#conn = mysql.connector.connect(host = "localhost", user="root", passwd="root", db="testdb")
conn = mysql.connector.connect(**config)
cursor = conn.cursor()
if conn.is_connected():
    print("Connected to mysql Database")

cursor.execute("SELECT plain_html FROM TABLE6")

linkfromtable = list(cursor.fetchall())
i = 1
for string in linkfromtable:
    #print(string)
    #nnp = np.asarray(string)
    soup_string = str(string)
    #names = get_human_names(soup_string)
    #print(names)
    numStr = re.findall(r'\d+', soup_string)
    #print(numStr)
    #match = re.findall(r'[\w\.-]+@[\w\.-]+', soup_string)
    #print(match)
    rx = re.compile('^.{11}$')#longer then 8 symbols
    result = [w for w in numStr if rx.match(w)]
    #print(i,result)
    t = str(result)
    u = t.replace('"','')
    p = u.replace("'","")
    
    
    
    b = []
    x = [b.append(item) for item in result if item not in b]
    #print(b)
    
    
    t = str(b)
    u = t.replace('"','')
    p = u.replace("'","")
    newquery="UPDATE TABLE6 set extracted = '"+p+"' where id = "+str(i)
    
    for link in b :
        
        xy = is_valid(link)
        #print(i,link,x)
        if xy == True:
            z = (str(i),str(link))
            #print(z)
            new_list = [x for x in z]
            
            print(new_list)
            
            ty = str(new_list).replace("'", "")
            
            r = str(new_list)
            #print(r)
            g = r.replace('"','')
#print(g)
            h = g.replace("'", "")
            #print(h)
            #newquery= "INSERT INTO TABLE6 * values ('"+h+"''"+str(i)"')
            #newquery =  """INSERT INTO anooog1 VALUES (%s,%s)""",(h)
    #print(i)
    #print(i,b)
    
    
    #newquery="UPDATE TABLE6 set extracted = '"+p+"' where id = "+str(i)
    #newquery="UPDATE TABLE6 set checker = '"+h+"' where id = "+str(i)
    cursor.execute(newquery)
    conn.commit()
    
    i = i + 1
            
 
 
            #qt =  ('index: ' + str(i),'id: ' +link,'validate: ' + str(x))
            #print(qt)
            #df = pd.DataFrame({'key':[i]})
            #print(df)
            #df.groupby('key')
            #newstr = po.replace("(", "")
            #news = newstr.replace(")", "")
            #print(news)
            
            
                        
            
            
            
            
                #for the_value in coloring_dictionary[key]:
                     #print(the_value)  # As simple as that 
            
            
            
            
            
            #print(', '.join(map(str, z)))
            #print(z, sep=' ', end='', flush=True)
                
            
            
            
            
    
        
         
            
        
    
    
  
print("--- %s seconds ---" % (time.time() - start_time))


