#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""Data de duplication and update"""
def DDaU(df):
    #数据去重
    df1 = df.drop_duplicates(subset=['Datetime'], keep='first', inplace= False)
    #索引更新
    df2 = df1.reset_index(drop=True)
    return df2


# In[ ]:




