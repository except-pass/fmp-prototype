import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np

import fmp.demodata as demodata
import fmp.aggrid as aggrid
import fmp.plotframework as plotframework
import fmp.metrics as metrics

@st.cache
def get_test_data():
    return demodata.make(100)

def move_to_front(df, col):
    coldata = df.pop(col)
    df.insert(0, col, coldata)

master_df = get_test_data()

st.markdown('Search by **name**, **address**, or **serial number**')
search_text = st.text_input("🔎")

master_df = demodata.search_df(master_df, search_text)

addresses = master_df.drop_duplicates(subset=['address', 'state', 'postcode', 'city'])
addresses.drop('sn', axis=1, inplace=True)
addresses.drop('product', axis=1, inplace=True)
move_to_front(addresses, 'namefirst')
move_to_front(addresses, 'namelast')

gb = aggrid.GridOptionsBuilder.from_dataframe(addresses)
gb.configure_selection('single')

search_results_col, map_col = st.columns([5,3])

with search_results_col:
    address_df_selection = aggrid.make(addresses, gb)
    if address_df_selection['selected_rows']:
        search_row = address_df_selection['selected_rows'][0]
        sn_df = demodata.search_df_for_row(master_df, search_row)[ ['sn', 'product']]
        st.write(sn_df)

active_address = demodata.extract_address(addresses, address_df_selection)

with map_col:
    st.map(demodata.get_map_df(active_address), zoom=10)


st.button("Go to detailed view (not functioning)")

soc, voltage, amps, chast, faults = demodata.get_site_data(active_address)
#cardfig, plotfig = plots.stats_and_cards(soc, voltage, amps)
#plots.plot_stats_and_cards(cardfig, plotfig)
if address_df_selection['selected_rows']:
    metric_l = [ dict(name='SoC', amount='{:.1f}'.format(soc[-1]), unit='%', delta='8.9%'),
                dict(name='V', amount='{:.1f}'.format(voltage[-1]), unit='V', delta='1.4'),
                dict(name='A', amount='{:.1f}'.format(amps[-1]), unit='A', delta='-2.1')
            ]    
    metrics.show_metric_cols(metric_l)
    plotframework.plot_block(block='Total', items=['SoC', 'V', 'A'], 
                            serial_numbers=['Total'])