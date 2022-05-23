import streamlit as st
import plotly.graph_objects as go

def add_indicators(soc, volts, amps, fig, col=0, SN=''):
    fig.add_trace( go.Indicator(
        mode = "number",
        value = soc,
        number = {'prefix':'soc: '},
        title = SN,
        domain = {'row': 0, 'column': col})
    )
    fig.add_trace(  go.Indicator(
        mode = "number",
        value = volts,
        number = {'suffix':' V'},    
        #title = 'voltage',
        domain = {'row': 1, 'column': col})
    )

    fig.add_trace( go.Indicator(
        mode = "number",
        value = amps,
        number = {'suffix':' A'},
        domain = {'row': 2, 'column': col})
    )

    return fig

if __name__ == '__main__':
    cardfig = go.Figure()

    cardfig = add_indicators(1,2,3, cardfig, col=0)
    cardfig = add_indicators(4,5,6, cardfig, col=1, SN='DEF456')
    cardfig.update_layout(
        grid = {'rows': 3, 'columns':2, 'pattern': "independent"})

    st.plotly_chart(cardfig)