import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from . import cards

def plot_key_stats(fig, soc, voltage, amps):
    fig.add_trace(go.Scatter(y=soc),
            row=1, col=1)
    fig.add_trace(go.Scatter(y=voltage),
            row=2, col=1)
    fig.add_trace(go.Scatter(y=amps),
            row=3, col=1)
    return fig

def stats_and_cards(soc, voltage, amps, fig=None):
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