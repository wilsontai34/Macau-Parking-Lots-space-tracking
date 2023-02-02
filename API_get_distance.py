import pandas as pd
import json
import numpy as np
from urllib import request
from urllib import parse

def get_location(df):
    location = []
    for i in range(len(df['Longtitude'])):
        lon_lat = str(df['Longtitude'][i]) + ',' + str(df['Latitude'][i])
        location.append(lon_lat)
    return location

def get_distance_info(location, url_base, output):
    for i, ori in enumerate(location):
        for j, des in enumerate(location[i+1:]):
            url=url_base.format(ori,des)
            ori_des = '{0},{1}\n'.format(df['Name'][i], df['Name'][i + j + 1])
            try:
                html=request.urlopen(url,timeout=15).read()
                js=json.loads(html)
                distance = js['route']['paths'][0]['distance']
                time = js['route']['paths'][0]['duration']
                out='{0},{1},{2},{3}\n'.format(df['Name'][i], df['Name'][i + j + 1], distance, time)
                print(out)
                output.write(out.encode('utf8'))
            except Exception as e:
                print(repr(e))
                output.write(ori_des.encode('utf8'))
    output.close()

if __name__ == "__main__":
    df = pd.read_csv('info.csv')
    location = get_location(df)
    url_base='https://restapi.amap.com/v3/direction/driving?&key=95c633476ebff014ced61135508481cb&origin={0}&destination={1}'
    output = open('distance_info.txt', 'wb+')  # the distances of different parking space
    get_distance_info(location, url_base, output)