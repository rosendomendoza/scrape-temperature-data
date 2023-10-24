import streamlit as st
import plotly.express as px
#import pandas as pd
from scrapedata import scrapedata
import sqlite3

st.set_page_config(layout="centered")
st.info("Scrapping the data...")


scrapedata(15, 1)

#df = pd.read_csv("data.txt")
#colX , colY = df.columns
#x_values = df.get(colX)
#y_values = df.get(colY)

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cursor.execute("SELECT date FROM temp_stamp")
x_values = cursor.fetchall()
x_values = [str(item).rstrip("',)").lstrip("('") for item in x_values]

cursor.execute("SELECT temperature FROM temp_stamp")
y_values = cursor.fetchall()
y_values = [str(item).rstrip("',)").lstrip("('") for item in y_values]

cursor.close()
connection.close()

figure = px.line(x=x_values, y=y_values,
                 labels={"x": "Dates", "y": "Temperature (ºC)"})
st.plotly_chart(figure)

