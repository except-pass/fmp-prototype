import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

import random

def random_enum(maxval=5, n=200, stickiness=0.9):
    returnme = [None]*n
    val = 0
    for i in range(n):
        if random.random()>stickiness:
            val = random.randint(0, maxval)
        returnme[i] = val
    return returnme

data = random_enum()
fig = px.imshow([data]*10)

st.markdown("Show enum data with a heatmap.")
st.markdown("Instead of numbers on the legend, we should show the labels")
st.markdown("e.g. if 1='Communication Error' then show 'Communication Error'")
st.markdown("[This is the behavior I want](https://grafana.com/docs/grafana/latest/visualizations/state-timeline/)")
st.plotly_chart(fig, use_container_width=True)


