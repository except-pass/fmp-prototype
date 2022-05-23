import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import fmp.aggrid as aggrid

class DataStream:
    def __init__(self, name):
        self.name = str(name)

    def plot_as_number(self, data, legend_name):
        return go.Scatter(y=data, 
                    name= legend_name, 
                    showlegend=True
                    )

def random_data(n=200, siteid=None):
    return np.random.randn(n)


def plot_block(block, items, serial_numbers):
    num_plots = len(items)

    subplot_titles = [ '{block}: {item}'.format(block=block, item=item) for item in items]

    if num_plots:
        fig = make_subplots(rows=num_plots, cols=1,
                            shared_xaxes=True,
                            subplot_titles=subplot_titles,
                            #vertical_spacing=0.04,
        )
        fig.update_layout(height=700)

        for row, item in enumerate(items):
            ds = DataStream(name=item)
            for sn in serial_numbers:
                fig.add_trace(ds.plot_as_number(random_data(), sn), 
                                    row=row+1, col=1)

        st.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    import fmp.demodata as demodata
    import numpy as np
    items = ['V', 'A', 'Tmp']
    block = 'module'
    serial_numbers = ['ABC', 'DEF', 'GHI']

    plot_block(block, items, serial_numbers)
