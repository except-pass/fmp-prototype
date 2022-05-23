import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder


def make(df, gbuilder, **configs):
    gridOptions = gbuilder.build()
    aggrid_opts = dict(data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=False,
        theme='blue', #Add theme color to the table
        enable_enterprise_modules=False,
        height=250,
        width='100%',
        reload_data=False)

    aggrid_opts.update(configs)
    return AgGrid(
        df,
        gridOptions=gridOptions,
        **aggrid_opts
    )    

def checkbox_multiple_selection_builder(df:pd.DataFrame):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection('multiple', use_checkbox=True)
    return gb
