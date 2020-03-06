import plotly.plotly as py
import plotly.graph_objs as go
import mysql.connector
import pandas as pd

conn = mysql.connector.connect(host="localhost", user="root", passwd="LucieLeia0804", db="mydb")
cursor = conn.cursor()
cursor.execute('select Name, Continent, Population, LifeExpectancy, GNP from Country')

rows = cursor.fetchall()
str(rows)[0:300]

df = pd.DataFrame( [[ij for ij in i] for i in rows] )
df.rename(columns={0: 'Name', 1: 'Continent', 2: 'Population', 3: 'LifeExpectancy', 4:'GNP'}, inplace=True)
df = df.sort_values(['LifeExpectancy'], ascending=[1])
