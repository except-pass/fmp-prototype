import streamlit as st


def make_metric(name, amount, unit, delta):
    value='{} {}'.format(amount, unit)
    return st.metric(label=name, value=value, delta=delta)


def show_metric_cols(metrics):
    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):
        with col:
            make_metric(**metric)

if __name__ == '__main__':
    metrics = [ dict(name='SoC', amount=98, unit='%', delta='8.9%'),
                dict(name='V', amount=53.1, unit='V', delta='1.4')
            ]
    show_metric_cols(metrics)