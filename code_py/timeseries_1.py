# code for time series 1

import numpy as np
import matplotlib.pyplot as plt
import timesynth as ts
import pandas as pd
import plotly.express as px
import plotly.io as pio


np.random.seed()
# generate time axis with sequential numbers
times = np.arange(200)
times # 0:199
values = np.random.randn(200)*100
values



def plot_time_series(time, values, label, legends=None):
    if legends is not None:
        assert len(legends) == len(values)
    if isinstance(values, list):
        series_dict = {"Time": time}
        for v, l in zip(values, legends):
            series_dict[l] = v
        plot_df = pd.DataFrame(series_dict)
        plot_df = pd.melt(plot_df, id_vars="Time", var_name="ts", value_name="Value")
    else:
        series_dict = {"Time": time, "Value": values, "ts": ""}
        plot_df = pd.DataFrame(series_dict)

    if isinstance(values, list):
        fig = px.line(plot_df, x="Time", y="Value", line_dash="ts")
    else:
        fig = px.line(plot_df, x="Time", y="Value")
    fig.update_layout(
        autosize=False,
        width=900,
        height=500,
        title={
            'text': label,
            #         'y':0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        titlefont={
            "size": 25
        },
        yaxis=dict(
            title_text="Value",
            titlefont=dict(size=12),
        ),
        xaxis=dict(
            title_text="Time",
            titlefont=dict(size=12),
        )
    )
    return fig

fig = plot_time_series(times, values, 'White noise')
fig.show()

