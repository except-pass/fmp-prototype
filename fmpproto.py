import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import fmp.demodata as demodata
import fmp.aggrid as aggrid
import sidebar
import fmp.cards as cards

st.title("Fleet Management Portal")

def plot_key_stats(fig, soc, voltage, amps):
    fig.add_trace(go.Scatter(y=soc),
            row=1, col=1)
    fig.add_trace(go.Scatter(y=voltage),
            row=2, col=1)
    fig.add_trace(go.Scatter(y=amps),
            row=3, col=1)
    return fig

def stats_and_cards(soc, voltage, amps, fig=None, show=True):
    fig = fig or make_subplots(rows=3, cols=1,
                        shared_xaxes=True,
                        #vertical_spacing=0.02,
                        )
    fig = plot_key_stats(fig, soc, voltage, amps)
    cardfig = go.Figure()
    cardfig.update_layout(
        grid = {'rows': 3, 'columns':1, 'pattern': "independent"})
    cardfig = cards.add_indicators(soc[-1], voltage[-1], amps[-1], cardfig, col=0)
    return cardfig, fig

def plot_stats_and_cards(cardfig, plotfig):
    # Plot!
    cardcol, plotcol = st.columns([2,5])
    with cardcol:
        st.plotly_chart(cardfig, use_container_width=True)
    with plotcol:
        st.plotly_chart(plotfig, use_container_width=True)

@st.cache
def get_test_data():
    return demodata.make(100)

with st.sidebar:
    sb = sidebar.Sidebar()
    sb.make()

pdf = get_test_data()
pdf = demodata.search_df(pdf, sb.search_text)

gb = GridOptionsBuilder.from_dataframe(pdf)
gb.configure_selection('single')

search_results_col, map_col = st.columns([5,3])

with search_results_col:
    ## TODO split into 2 df, people/sites and serial numbers/product names
    grid_response = aggrid.make(pdf, gb)

active_address = demodata.extract_address(pdf, grid_response)
with map_col:
    st.map(demodata.get_map_df(active_address), zoom=10)

with st.expander("Site summary data", expanded=True):
    soc, voltage, amps, chast, faults = demodata.get_site_data(1)    
    cardfig, plotfig = stats_and_cards(soc, voltage, amps)
    plot_stats_and_cards(cardfig, plotfig)

proddfcol, guardiancmd, productcmd = st.columns([2,5,5])
with proddfcol:
    proddf = pd.DataFrame({"product": ['eFlex']*4, "SN": ['EF001', 'EF002', 'EF003', 'EF004']})
    product_options_builder = GridOptionsBuilder.from_dataframe(proddf)
    product_options_builder.configure_selection('multiple', use_checkbox=True)
    selected_products = aggrid.make(proddf, product_options_builder,
                            height=150)

with guardiancmd:
    st.write("(These will be links in the future)")
    st.write("Guardian Commands:")
    st.write("- Update Guardian Firmware")
    st.write("- Update BMS Firmware")
    st.write("- Some other Guardian Function")

with productcmd:
    if len(selected_products['selected_rows']) == 1:
        row = selected_products['selected_rows'][0]
        st.write("Run command on {prod} {SN}".format(prod=row['product'], 
                                                    SN=row['SN']))
        st.write("- Enable/Disable")
        st.write("- Some other function")
batt_data = {}

detail_card_fig = None
details_fig = None
for row in selected_products['selected_rows']:
    sn = row['SN']
    batt_data[sn] = demodata.get_site_data(sn)
    
    detail_card_fig, details_fig = stats_and_cards(batt_data[sn][0], batt_data[sn][1], batt_data[sn][2],
                        fig=details_fig)

if detail_card_fig and details_fig:
    plot_stats_and_cards(detail_card_fig, details_fig)
