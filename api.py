import pathlib
import sqlite3
import pandas as pd
from Crawler import task

DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath("DSATParking.sqlite").resolve()

def get_space_data(id):
    con = sqlite3.connect(str(DB_FILE),check_same_thread=False) #avoid check_sum_threads Error
    statement = f'SELECT * FROM CP{id} order by Datetime desc limit 1300;'
    df = pd.read_sql_query(statement, con)
    return df

def get_area_space(car_type):
    table = task()
    lis = table[car_type].to_list()
    for i in range(len(lis)):
        try:
            lis[i] = int(lis[i])
        except:
            lis[i] = 0
    return lis

if __name__ == "__main__":
    a = get_area_space('Car')
    print(len(a))