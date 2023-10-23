import streamlit as st
import plotly.express as px
import pandas as pd
from scrapedata import scrapedata

st.set_page_config(layout="centered")
st.info("Scrapping the data...")


scrapedata(15,1)

df = pd.read_csv("data.txt")
colX , colY = df.columns
x_values = df.get(colX)
y_values = df.get(colY)

figure = px.line(x=x_values, y=y_values, labels={"x": colX.title(), "y": colY.title()})
st.plotly_chart(figure)

