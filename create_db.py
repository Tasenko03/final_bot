import sqlite3
import pandas
connection = sqlite3.connect('dict_final.db', check_same_thread=False)
df = pandas.read_csv("C:/Users/Ольга/Desktop/terms_last_ver.csv", sep=';')
df.to_sql('terms_n', connection, if_exists='append', index=False)
