'''
Created on Mar 31, 2018

@author: root
'''


'''
Program introduction
The programm should display the outcome of a string Variable
In final result user should get the relust of all id codes for him to see
Provide user with options to do staff 
The will be 
'''
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
import mysql.connector as my
from time import sleep
#from src.util import clean
#from src.exceptions import *
#from src.ik import calc_check_digit
import datetime
start_time = time.time()
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

def is_valid(number):
    """Check if the number provided is valid. This checks the length,
    formatting, embedded date and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def get_human_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    names = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: #ignore surnames only
            for part in person:
                name += part + ' '
            if name[:-1] not in names:
                names.append(name[:-1])
            name = ''
        person = []
    print(names)   
    first_names = []
    for name in names:
        first_name = HumanName(name).first
        first_names.append(first_name)
    return first_names


print("\t  Test module 1  ")
print("    Please login to mysql server")
print("\n")
print("To connect to mysql server please fill all filed's")
h = input("Hostname: ")
u = input("User: ")
p = input("Password: ")
d = input("Database: ")
#print(h,u,p,d)
try:
   #conn = my.connect(host = h, user= u, passwd=p, db=d)
   conn = mysql.connector.connect(user="root", passwd="devil6007472", db="testdb")
   cursor = conn.cursor()
   if conn.is_connected():
      print("Connected to mysql Database")
      
   choice = ''
   while choice != 'q':    
         #display_title_bar()
    
    # Let users know what they can do.
    print("\n[1] get names from web site.")
    print("[2] Get id codes from web site.")
    print("[3] Get mail address")
    print("[4] Get names")
    print("[5] Insert id codes into mysql")
    print("[q] Quit.")
    
    choice = input("What would you like to do? ")
    cursor = conn.cursor()
    cursor.execute("SELECT plain_html FROM table5") 
    linkfromtable = list(cursor.fetchall())
    for string in linkfromtable:
           soup_string = str(string)
           numStr = re.findall(r'\d+', soup_string)
           rx = re.compile('^.{11}$')#longer then 8 symbols
           result = [w for w in numStr if rx.match(w)]
    
    # Respond to the user's choice.
    if choice == '1':
       for string in linkfromtable:
           soup_string = str(string)
           names = get_human_names(soup_string)   
       #print("\nYou are  "+names+".\n")
       
    elif choice == '2':
        
        #id = is_valid('35701105226')
        #print(id)
        for string in linkfromtable:
           soup_string = str(string)
           numStr = re.findall(r'\d+', soup_string)
           rx = re.compile('^.{11}$')#longer then 8 symbols
           
           result = [w for w in numStr if rx.match(w)]
           print(result)
          # r = int(str(result))
           #result1 = [is_valid(r) for x in list if list]
           #print(result1)
           for x in result:
               print(is_valid(x))
           #id = is_valid(str(all))
           #print(id)
           #print(x)
           
           
            
           
           #id = is_valid(int(str(result)))
           #print(id)
           

           
        
           
    
        
        #print("\nI can't wait to meet this person!\n")
    elif choice == '3':
        for string in linkfromtable:
           soup_string = str(string)
           match = re.findall(r'[\w\.-]+@[\w\.-]+', soup_string)
           print(match)
    elif choice == '4':  
          i = 1
          for string in linkfromtable:
              newquery="UPDATE TABLE4 set extracted = '"+str(result)+"' where id = "+str(i)
              cursor.execute(newquery)
              conn.commit()
              i = i + 1
              print()  
    elif choice == 'q':
        
        print("\nThanks for playing. Bye.")
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        print("\nI didn't understand that choice.\n")
        

    
except my.Error as e:
    print(e)
    
    
    









