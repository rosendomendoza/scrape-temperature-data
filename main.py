import streamlit as st
import plotly.express as px
from scrapedata import scrapedata
import sqlite3

st.set_page_config(layout="centered")
st.info("Scrapping the data...")

scrapedata(5, 1)

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cursor.execute("SELECT date FROM temp_stamp")
x_values = cursor.fetchall()
x_values = [x[0] for x in x_values]

cursor.execute("SELECT temperature FROM temp_stamp")
y_values = cursor.fetchall()
y_values = [y[0] for y in y_values]

cursor.close()
connection.close()

figure = px.line(x=x_values, y=y_values,
                 labels={"x": "Dates", "y": "Temperature (ºC)"})
st.plotly_chart(figure)

