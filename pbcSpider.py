#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 17:28:25 2021

@author: changhaoli
"""

# -*- coding = utf-8 -*-

'''
INPUT: 
- name: name of the city
- year: year
- month: month
OUTPUT:
- a csv file (e.g. 'guangzhou-2021-12.csv')
'''

from datetime import datetime
#from urllib import request, parse
from bs4 import BeautifulSoup
import time
#import pandas as pd
from selenium import webdriver
from fake_useragent import UserAgent
import csv

ua = UserAgent()

name = str(input("Please input city name (e.g. guangzhou): "))
year = str(input("Please indicate which year you wish to scrap: "))
month = str(input("Please indicate which month you wish to scrap: "))

def pbcSpider(link):
    driver = webdriver.Chrome()
    time.sleep(1)
    driver.get(link)
    req = driver.page_source
    # print(req)
    soup = BeautifulSoup(req, 'lxml')
    # print(soup.prettify())
    fram = soup.find("td", class_ = "content_right column")
    # print(fram.prettify())
    
    count = 0
    datelist = []
    linklist = []
    for item in fram.find_all("table", limit=1):
        # print(item)
        for temp in item.find_all("td", limit=1):
            ### FILTER ALL TIME OUT
            for inner in temp.find_all("td", width="100", class_="hei12jj", limit=10):
                # print(inner)
                d = datetime.strptime(inner.text, '%Y-%m-%d')
                ### INPUT DESIRED TIME HERE!
                if ((d > datetime(2021, 12, 1)) & (d < datetime(2021, 12, 31))):
                    print(d)
                    datelist.append(d)
                    count += 1
                else:
                    #return # delete this if exists!
                    pass
            if (count == 0):
                break
            l = temp.select('a[href]', limit=count)
            for k in range(0,len(l)):
                print("http://guangzhou.pbc.gov.cn" + (l[k]['href']))
                w = "http://guangzhou.pbc.gov.cn" + (l[k]['href'])
                linklist.append(w)
    
    txt = '{n}-{y}-{m}.csv'
    f = open(txt.format(n = name, y = year, m = month), 'w')
    writer = csv.writer(f)
    writer.writerow(['发布日期', '罚单链接'])
    
    for i in range(0, count):
        dlist = []
        dlist.append(datelist[i].date().strftime("%Y-%m-%d"))
        dlist.append(linklist[i])
        print(dlist)
        writer.writerow(dlist)
    
    f.close()

### INPUT OFFICIAL WEBSITE INSIDE                
pbcSpider('http://guangzhou.pbc.gov.cn/guangzhou/129142/129159/129166/index.html')








