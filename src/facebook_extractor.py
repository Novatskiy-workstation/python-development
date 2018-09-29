'''
Created on Jun 18, 2018

@author: mikhailnovatskiy
'''

import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import selenium.webdriver.support.ui as ui
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from html.parser import HTMLParser
import mysql.connector
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

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

#conn = mysql.connector.connect(host = "localhost", user="root", passwd="root", db="testdb",charset='utf8')
conn = mysql.connector.connect(**config)
cursor = conn.cursor()
if conn.is_connected():
    print("Connected to mysql Database")

usr = "mixanovatski13@gmail.com"
pwd = "devil6007472"

_browser_profile = webdriver.FirefoxProfile()
_browser_profile.set_preference("dom.webnotifications.enabled", False)
binary = FirefoxBinary('/Users/mikhailnovatskiy/eclipse-workspace/HtmlUrl/src/geckodriver')

driver = webdriver.Firefox(firefox_profile=_browser_profile)

driver.maximize_window()
driver.get("https://www.facebook.com/groups/364076470395469/members/")

assert "Facebook" in driver.title
elem = driver.find_element_by_id("email")
elem.send_keys(usr)
elem = driver.find_element_by_id("pass")
elem.send_keys(pwd)
elem.send_keys(Keys.RETURN)
driver.find_element_by_id('loginbutton').click()


pause = 3
wait = WebDriverWait(driver, 100)
lastHeight = driver.execute_script("return document.body.scrollHeight")
print(lastHeight)
i = 3
#driver.get_screenshot_as_file("test03_1_"+str(i)+".jpg")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause)
    newHeight = driver.execute_script("return document.body.scrollHeight")
    ##print(newHeight)
    if newHeight == lastHeight:
        break
    lastHeight = newHeight
    i += 1
    #driver.get_screenshot_as_file("test03_1_"+str(i)+".jpg")
page_source = driver.page_source

driver.close()
#_60ri fsl fwb fcb
#_60rg _8o _8r lfloat _ohe
soup = BeautifulSoup(page_source,"lxml").decode('unicode_escape').encode('ISO-8859-1','ignore').decode('utf8','ignore')
#print(soup.encode("utf-8"))


soup_str = str(soup)




g = soup_str.replace('\n','')
z = g.replace('"','')
#print(g)
h = z.replace("'", "")

#urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', str)
#ST = str(urls)
#print(urls)
j = 1
newquery="UPDATE TABLE123 set plain_html = '"+h+"' where id = "+str(j)
cursor.execute(newquery)
    
conn.commit()

#links_with_text = [a['href'] for a in soup.find_all('a',  href=True) if a.text]
#j = 1
#for tweet in soup:
    #print(tweet)
    
   # r = str(tweet)
   # g = tweet.replace('\n','')

   # z = g.replace('"','')
#print(g)
   # h = z.replace("'", "")
    
   # t = strip_tags(h)
    
    #print((strip_tags(z)).encode('utf8')) 
    
   # newquery="UPDATE TABLE123 set plain_html = '"+t+"' where id = "+str(j)
    #cursor.execute(newquery)
    
   # conn.commit()
   # j = j + 1
#j = 1
#for tweet in soup.select("a"):
   # r = str(tweet)
   # g = r.replace('\n','')

    #z = g.replace('"','')
#print(g)
   # h = z.replace("'", "")
    
  #  t = strip_tags(h)
    
    #print((strip_tags(z)).encode('utf8')) 
    
   # newquery="UPDATE TABLE123 set plain_html = '"+t+"' where id = "+str(j)
   # cursor.execute(newquery)
    
   # conn.commit()
  #  j = j + 1
    


    
       


     




#soup = BeautifulSoup(page_source,"lxml")
#for tweet in soup.select("div.tweet"):
   # print((tweet.text).encode('utf8'))
                                                                                              



#elem = driver.find_element_by_css_selector(".input.textInput")
#elem.send_keys("Posted using Python's Selenium WebDriver bindings!")
#elem = driver.find_element_by_css_selector("input[value=\"Publicar\"]")
#elem.click()


