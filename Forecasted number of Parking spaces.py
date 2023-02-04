#!/usr/bin/env python
# coding: utf-8

# In[5]:


import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from DDaU import DDaU
import datetime


# In[6]:


db = sqlite3.connect('Parking.sqlite')#数据库


# In[7]:


cursor = db.cursor()#游标
print(cursor)


# In[8]:


def fore():
    difference = 0
    pot = int(input("The parking lot number you want to predict is："))
    time = '2022-12-28 12:00:00'
    dt = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    tem = {}
    tem[0] = float(input("Want to predict the number of parking spaces after () hours  "))#hours
    
    #Calculate the difference using the previous x days
    for i in range(2):
        date1 = (dt + datetime.timedelta(days = -(i+1),minutes = -5)).strftime("%Y-%m-%d %H:%M:%S")
        date2 = (dt + datetime.timedelta(days = -(i+1))).strftime("%Y-%m-%d %H:%M:%S")
        df1=pd.read_sql(f"SELECT * FROM CP{pot} WHERE Datetime > '{date1}' AND Datetime < '{date2}'",con=db)
        data1 = max(df1['Car'].astype(int)[0:-1])
    
        date3 = (dt + datetime.timedelta(days = -(i+1),hours = tem[0],minutes = -5)).strftime("%Y-%m-%d %H:%M:%S")
        date4 = (dt + datetime.timedelta(days = -(i+1),hours = tem[0])).strftime("%Y-%m-%d %H:%M:%S")
        df2=pd.read_sql(f"SELECT * FROM CP{pot} WHERE Datetime > '{date3}' AND Datetime < '{date4}'",con=db)
        data2 = max(df2['Car'].astype(int)[0:-1])

        difference = ((data2-data1)+difference)//(i+1)

    #Current Values and Forecast
    N1 = (dt + datetime.timedelta(minutes = -5)).strftime("%Y-%m-%d %H:%M:%S")
    N2 = dt.strftime("%Y-%m-%d %H:%M:%S")
    df3=pd.read_sql(f"SELECT * FROM CP{pot} WHERE Datetime > '{N1}' AND Datetime < '{N2}'",con=db)
    data5 = max(df3['Car'].astype(int)[0:-1]) 
    forec = data5 + difference
    
    if forec < 0:
        forec = 0
            
    #Verification
    N11 = (dt + datetime.timedelta(hours = tem[0],minutes = -5)).strftime("%Y-%m-%d %H:%M:%S")
    N22 = (dt + datetime.timedelta(hours = tem[0])).strftime("%Y-%m-%d %H:%M:%S")
    df6 = pd.read_sql(f"SELECT * FROM CP{pot} WHERE Datetime > '{N11}' AND Datetime < '{N22}'",con=db)
    data6 = max(df6['Car'].astype(int)[0:-1])
    
    bili = "Unable to calculate"
    if data6 != 0:
        bili = (data6-forec)/data6
    print("\n")
    print("Current parking space \033[31m%d\033[30m"%data5)
    print("After \033[31m%.1f\033[30m hour，the parking lot has \033[31m%d\033[30m space"%(tem[0],forec))
    print("The actual number of parking spaces is %d"%data6)
    if bili == "Unable to calculate":
        print('The closeness of this prediction cannot be calculated')
    if (1-abs(bili)) < 0.6:
        print('Excessive variation in predictions')
    else:
        print('Proximity of this forecast: {:.2%}'.format(1-abs(bili))) 
fore()

