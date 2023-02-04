#!/usr/bin/env python
# coding: utf-8

# In[24]:


import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from DDaU import DDaU
import time


# In[15]:


db = sqlite3.connect('Parking.sqlite')#数据库


# In[16]:


cursor = db.cursor()#游标
print(cursor)


# In[17]:


df=pd.read_sql("SELECT * FROM CP58 WHERE Datetime > '2022-12-26 00:00:00' AND Datetime < '2022-12-29 00:00:00'",con=db)
df2 = DDaU(df)
print(df.head())


# In[18]:


#去重数据作图及形状辅助判断
fig, ax = plt.subplots(11, 6)
for i in range(61):
    df=pd.read_sql(f"SELECT * FROM CP{i} WHERE Datetime > '2022-12-26 00:00:00' AND Datetime < '2022-12-29 00:00:00'",con=db)
    if (i != 1) and (i != 10) and (i != 19) and (i != 27):
        
        #去重
        df2 = DDaU(df)
        
        ax[i%11,i//11].plot(df2['Car'].astype(int))
        print
        
        df3 = df2.loc[df2['Datetime']>='2022-12-26 00:00:00']
        time1 = df3.loc[df3['Datetime']<='2022-12-26 00:30:00']
        time1i=time1['Car'].astype(int)

        df4 = df2.loc[df2['Datetime']>='2022-12-26 12:00:00']
        time2 = df4.loc[df4['Datetime']<='2022-12-26 12:30:00']
        time2i=time2['Car'].astype(int)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.suptitle('26—28 56个停车场剩余车位数量折线图',fontsize=20)
plt.show


# In[19]:


fig, ax = plt.subplots(11, 6)
for i in range(61):
    df=pd.read_sql(f"SELECT * FROM CP{i} WHERE Datetime > '2022-12-26 00:00:00' AND Datetime < '2022-12-27 00:00:00'",con=db)
    if (i != 1) and (i != 10) and (i != 19) and (i != 27):       
        df2 = DDaU(df) 
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))     
        ax[i%11,i//11].plot(df2['Car'].astype(int))
        for i in range(11):
            for j in range(6):
                ax[i,j].xaxis.set_ticks([])
                ax[i,j].yaxis.set_ticks([])

plt.show


# In[20]:


fig, ax = plt.subplots(11, 6)
for i in range(61):
    df=pd.read_sql(f"SELECT * FROM CP{i} WHERE Datetime > '2022-12-27 00:00:00' AND Datetime < '2022-12-28 00:00:00'",con=db)
    if (i != 1) and (i != 10) and (i != 19) and (i != 27):       
        df2 = DDaU(df) 
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))     
        ax[i%11,i//11].plot(df2['Car'].astype(int))
        for i in range(11):
            for j in range(6):
                ax[i,j].xaxis.set_ticks([])
                ax[i,j].yaxis.set_ticks([])

plt.show


# In[21]:


fig, ax = plt.subplots(11, 6)
for i in range(61):
    df=pd.read_sql(f"SELECT * FROM CP{i} WHERE Datetime > '2022-12-28 00:00:00' AND Datetime < '2022-12-29 00:00:00'",con=db)
    if (i != 1) and (i != 10) and (i != 19) and (i != 27):       
        df2 = DDaU(df) 
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))     
        ax[i%11,i//11].plot(df2['Car'].astype(int))
        for i in range(11):
            for j in range(6):
                ax[i,j].xaxis.set_ticks([])
                ax[i,j].yaxis.set_ticks([])

plt.show


# In[22]:


print("住宅区有：")
for i in range(60):
    if (i == 2 ) or (i == 3 ) or (i == 4 ) or (i == 5 ) or (i == 11 ) or (i == 12 ) or (i == 15 ) or (i == 18 ) or (i == 20 ) or (i == 22 ) or (i == 24 ) or (i == 28 ) or (i == 29 ) or (i == 30 ) or (i == 35 ) or (i == 52 ) or (i == 53 ):
        df=pd.read_sql(f"SELECT * FROM CP{i}",con=db)
        print("%s"%df['Location'][0])
print("-----------------")
print("工作区有：")
for i in range(60):
    if (i == 7 ) or (i == 8 ) or (i == 9 ) or (i == 13 ) or (i == 16 ) or (i == 17 ) or (i == 21 ) or (i == 23 ) or (i == 25 ) or (i == 26 ) or (i == 31 ) or (i == 32 ) or (i == 33 ) or (i == 34 ) or (i == 39 ) or (i == 40 ) or (i == 49 ) or (i == 54 ) or (i == 55 ) or (i == 56 ) or (i == 57 ) or (i == 59 ):
        df=pd.read_sql(f"SELECT * FROM CP{i}",con=db)
        print("%s"%df['Location'][0])
print("-----------------")
print("特殊区有：")
for i in range(60):
    if (i == 36 ) or (i == 42 ) or (i == 45 ) or (i == 46 ) or (i == 47 ) or (i == 48 ) or (i == 50 ) or (i == 58 ):
        df=pd.read_sql(f"SELECT * FROM CP{i}",con=db)
        print("%s"%df['Location'][0])


# In[27]:


x = y =[]
for i in range(60):
    df=pd.read_sql(f"SELECT *,MAX(cast(Car as int)) FROM CP{i} WHERE Datetime > '2022-12-26 00:00:00' AND Datetime < '2022-12-29 00:00:00'",con=db)
    if (i != 1) and (i != 10) and (i != 19) and (i != 27) and (i != 0) and (i != 6) and (i != 14) and (i != 37) and (i != 38) and (i != 41) and (i != 43) and (i != 44) and (i != 51) and (i != 42) and (i != 46) and (i != 47) and (i != 48):
        string = df.Datetime[0]
        dt = time.strptime(string, "%Y-%m-%d %H:%M:%S")
        x = x+[(dt).tm_hour]
        y = y+[i]
#my_x_ticks = np.arange(0, 23, 1)
#plt.xticks(my_x_ticks)
plt.scatter(x, y, color = 'r')


x = y =[]
for i in range(60):
    df=pd.read_sql(f"SELECT *,MIN(cast(Car as int)) FROM CP{i} WHERE Datetime > '2022-12-26 00:00:00' AND Datetime < '2022-12-29 00:00:00'",con=db)
    if (i != 1) and (i != 10) and (i != 19) and (i != 27):
        string = df.Datetime[0]
        dt = time.strptime(string, "%Y-%m-%d %H:%M:%S")
        x = x+[(dt).tm_hour]
        y = y+[i]
plt.scatter(x, y, color = 'b')

plt.xlabel('hours')
plt.ylabel('Parking lot number')

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.suptitle('Scatter plot of the Max&Min remaining parking spaces',fontsize=13)
plt.show()


# In[26]:


x = y =[]
for i in range(60):
    df=pd.read_sql(f"SELECT *,MAX(cast(Car as int)) FROM CP{i} WHERE Datetime > '2022-12-26 00:00:00' AND Datetime < '2022-12-29 00:00:00'",con=db)
    if (i != 1) and (i != 10) and (i != 19) and (i != 27) and (i != 0) and (i != 6) and (i != 14) and (i != 37) and (i != 38) and (i != 41) and (i != 43) and (i != 44) and (i != 51) and (i != 42) and (i != 46) and (i != 47) and (i != 48):
        string = df.Datetime[0]
        dt = time.strptime(string, "%Y-%m-%d %H:%M:%S")
        
        st = df.Car[0]
        x = x+[(dt).tm_hour]
        y = y+[i]

plt.scatter(x, y, color = 'r')
plt.suptitle('The max remaining parking spaces scatter plot',fontsize=13)

plt.xlabel('hours')
plt.ylabel('Parking lot number')


for a, b in zip(x, y):  
    plt.text(a, b, (a, b),size = 'x-small',c = 'green')
plt.show()

