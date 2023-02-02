import pandas as pd
import datetime as dt

def dis_sorted(parking):
    df = pd.read_csv('distance_info.txt')
    sorted_df = df[df['origin'] == parking].sort_values('Distance(km)')
    top3_df = sorted_df.iloc[:3,1:4]
    top3_df['Distance(km)'] = top3_df['Distance(km)'].div(1000)
    top3_df['Time(mins)'] = pd.to_datetime(top3_df['Time(mins)'], unit='s')
    top3_df['Time(mins)'] = top3_df['Time(mins)'].dt.strftime('%M:%S')
    
    return top3_df


if __name__=="__main__":
    df = pd.read_csv('distance_info.txt')
    parking_input = input('Please input the parking space right now: ')
    dis_sorted(parking_input)


