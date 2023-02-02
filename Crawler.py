#!/usr/bin/env python
# coding: utf-8

# In[3]:

import time
from datetime import datetime
from threading import Timer
import urllib.request
import re
from urllib.error import HTTPError
#SQL
import sqlite3
#from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def task():
    url = 'http://www.dsat.gov.mo/dsat/carpark_realtime_core.aspx'
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    #bulid the column names
    names = ['Location', 'Datetime', 'Car', 'Motor', 'Ecar', 'Emotor', 'Disabled']
    #build the storage of parking
    car = []
    motor = []
    ecar = []
    emot = []
    disa = []

    #engine = create_engine('sqlite:///DSATParking.sqlite')
    conn = sqlite3.connect('DSATParking.sqlite')

    # 定时任务 https://cloud.tencent.com/developer/article/1800067

    req = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(req).read().decode('utf-8')

    # get the update time from html
    time = re.findall(r'<div align="center" style="font-size:12px;color:#666;">(\d+-\d+-\d+ \d+:\d+:\d+|\D*)', html)
    # get the update time from html
    for i, j in enumerate(time):
        if j[0] != "2":
            time[i] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # get the names of parking lot from html
    locations = re.findall(r'<div align="center">(\D*)</', html)

    # get the number of parking
    car = re.findall(r'carpark_car.png"  height="40" align="absmiddle" /> (\d*)', html)
    motor = re.findall(r'carpark_motor.png"  height="40" align="absmiddle" /> (\d*)', html)
    ecar = re.findall(r'carpark_ecar.png"  height="40" align="absmiddle" /> (\d*)', html)
    emot = re.findall(r'carpark_emotor.png"  height="40" align="absmiddle" /> (\d*)', html)
    disa = re.findall(r'carpark_disabled.png"  height="40" align="absmiddle" /> (\d*)', html)

    # bulid a dataframe
    park = pd.DataFrame(np.array([locations, time, car, motor, ecar, emot, disa]).T, columns=names)
    #print(park)
    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # method one: named the table by natural numbers: 1 ,2 ..., 60
    for i in range(len(locations)):
        park[i:i+1].to_sql('CP'+str(i), con = conn , index = False, if_exists = 'append')

    return park
