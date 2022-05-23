import streamlit as st


class Sidebar:
    def __init__(self):
        self.search_text = None

    def make(self):
        st.markdown('Search by **name**, **address**, or **serial number**')
        self.search_text = st.text_input("🔎")
        tz = st.selectbox("Timezone", ['US/Eastern', 'US/Central', 'US/Pacific'])
        startcol, endcol = st.columns(2)
        with startcol:
            start_date = st.date_input("Start date")
            start_time = st.time_input("Start time")
        with endcol:
            end_date = st.date_input("End date")
            end_time = st.time_input("End time")