import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
import random

import fmp.demodata as demodata
import fmp.aggrid as aggrid
import fmp.plots as plots
import fmp.plotframework as plotframework
import fmp.metrics as metrics

## sidebar
with st.sidebar:
    period = st.selectbox("📅 Select a timeframe", 
                        ['Last 5 minutes', 'Last 30 minutes', 
                        'Last 1 hour', 'Last 6 hours', 
                        'Last 12 hours', 'Last 24 hours',
                        'Today', 'Yesterday',
                        'Last Week', 'Last Month', 
                        'Year to date', 'Last year',
                        'All available'],
                        index=5)
    st.write("-- OR --")
                        
    startcol, endcol = st.columns(2)
    with startcol:
        start_date = st.date_input("Start date")
        start_time = st.time_input("Start time")
    with endcol:
        end_date = st.date_input("End date")
        end_time = st.time_input("End time")
    tz = st.selectbox("Timezone", ['US/Eastern', 'US/Central', 'US/Pacific'])

owner = {'namefirst': "Katelyn", 'namelast': 'Leonard'}
site = {'address': '4588 Jessica River Apt. 133', 
        'state': 'OR',
        'city': 'Thomasborough',
        'postcode': '69216'
        }

info = owner.copy()
info.update(site)

products = [
            {'product': 'eFlex', 'sn': '20130902017'},
            {'product': 'eFlex', 'sn': '20130902018'},
            {'product': 'eFlex', 'sn': '20130902019'},
            {'product': 'eFlex', 'sn': '20130902020'},            
            ]


def metrics_from_selected_items(selected_items, name_prefix=''):
    metrics_l = []
    for d in selected_items:
        name = name_prefix+d['Name']
        amount='{:.1f}'.format(random.random()*30)
        unit=d['Unit']
        delta='{:.1f} {unit}'.format(random.random()*3, unit=unit)
        metrics_l.append(dict(name=name, amount=amount, unit=unit, delta=delta))
    if metrics_l:
        metrics.show_metric_cols(metrics_l)

prod_df = pd.DataFrame(products)

back_col, name_col, cmd_col = st.columns([2,7, 2])
with back_col:
    st.button("< Back to search results")

with name_col:
    st.info(
    """
    {namefirst} {namelast} \n
    {address} \ {city} {state} {postcode}
    """.format(**info))

with cmd_col:
    st.button("Remotely run commands at this site > ")

with st.expander("⚙️ Show/Hide Summary plots"):
    st.markdown("These plots show data at the level of an entire installation.")
    st.markdown("This can include multiple batteries all connected in parallel")
    st.markdown("Sunspec Model 802")
    df802 = pd.read_csv('sunspec802.csv')
 
    gb802 = aggrid.checkbox_multiple_selection_builder(df802)
    m802_selections = aggrid.make(df802, gb802)
    m802_items = m802_selections['selected_rows']

if m802_items:
    metrics_from_selected_items(m802_items)
plotframework.plot_block(block='Total', items=[d['Name'] for d in m802_items], 
                        serial_numbers=['Total'])

if m802_items:
    st.button("Download this section's data as csv", key='m802_download_button')

st.write("-" * 34)
gb = aggrid.GridOptionsBuilder.from_dataframe(prod_df)
gb.configure_selection('multiple', use_checkbox=True)
selected_products = aggrid.make(prod_df, gb, height=150)

detail_card_fig = None
details_fig = None
batt_data = {}

if not selected_products['selected_rows']:
    st.markdown("Select one or more products above")
    
with st.expander("⚙️ Show/Hide Module level plots"):
    st.markdown("These plots show data at the level of an individual battery module.")
    st.markdown("Fortress products like the eFlex are made up of a single module")
    st.markdown("Sunspec Model 805")

    df805 = pd.read_csv('sunspec805.csv')

    gb805 = aggrid.checkbox_multiple_selection_builder(df805)
    m805_selections = aggrid.make(df805, gb805)
    m805_items = m805_selections['selected_rows']

serial_numbers = [d['sn'] for d in selected_products['selected_rows']]
 
if m805_items:
    for sn in serial_numbers:
        metrics_from_selected_items(m805_items, name_prefix='{}: '.format(sn))
plotframework.plot_block(block='Total', items=[d['Name'] for d in m805_items], 
                        serial_numbers=serial_numbers)


if m802_items:
    st.button("Download this section's data as csv", key='m805_download_button')

st.write("-" * 34)
