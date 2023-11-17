import time
from threading import Thread
from streamlit.runtime.scriptrunner import add_script_run_ctx
import streamlit as st
import plotly.express as px
from scrapedata import scrapedata, URL
import sqlite3

# Show a progress bar while scraping data
def show_progres(ratio):
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.0155 * ratio)
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.empty()

# Configuring and show the header info web
st.set_page_config(layout="centered")
st.title("DATA SCRAPING EXERCISE")
st.subheader(f"Temperature scrapping data from {URL}")

# Input data for scrape processing
text_input_measurement = st.empty()
m = int(text_input_measurement.text_input("How many measurements do you "
                                          "want to make?", value=0))

text_input_delay = st.empty()
d = float(text_input_delay.text_input("delay (in seconds) between measurements",
                                      value=0.0))

process_button = st.empty()
my_button = process_button.button(label="Process", type="primary")

if d != 0 and m != 0.0 and my_button:
    text_input_delay.empty()
    text_input_measurement.empty()
    process_button.empty()

    st.caption(f"{m} Measurements every {d} seconds")

    # Show progress-bar in a Thread
    progress_thread = Thread(target=show_progres, args=(m * d,), daemon=True)
    add_script_run_ctx(progress_thread)

    # Scrape data in a Thread
    scrape_thread = Thread(target=scrapedata, args=(m, d), daemon=True)
    add_script_run_ctx(scrape_thread)

    # Start threaders
    progress_thread.start()
    scrape_thread.start()

    # Join threader
    progress_thread.join()
    scrape_thread.join()

    # Connecting to database
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    # Collected the scraped data
    cursor.execute("SELECT date FROM temp_stamp")
    x_values = cursor.fetchall()
    x_values = [x[0] for x in x_values]
    cursor.execute("SELECT temperature FROM temp_stamp")
    y_values = cursor.fetchall()
    y_values = [y[0] for y in y_values]

    cursor.close()
    connection.close()

    st.subheader("Temperature Line Graph")

    # Show the scraped data
    figure = px.line(x=x_values, y=y_values,
                     labels={"x": "Dates", "y": "Temperature (ºC)"})
    st.plotly_chart(figure)


