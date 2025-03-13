import dash
import plotly.graph_objs as go

from plotly.subplots import make_subplots
from dash.dependencies import Output, Input
from dash import dcc
from dash import html

from api_manager.exmo_api.api import ExmoAPI
from api_manager.hepler.TimeFormatter import TimeConverter


api = ExmoAPI()
app = dash.Dash(__name__)

dates = []
prices = []

response = api.get_candles_history(
    symbol='BTC_USD',
    resolution=15,
    from_sec=TimeConverter.get_now_in_sec() - 172800,
    to_sec=TimeConverter.get_now_in_sec()
)

candles_data = response['candles']
candles_data.reverse()

for n in candles_data:
    time1 = int(str(n['t'])[:-3])
    dates.append(TimeConverter.sec_to_date(time1))
    prices.append(float(n['c']))

fig = go.Scatter(x=dates, y=prices)
fig_main = make_subplots(rows=5, cols=4, specs=[[{"rowspan": 2, "colspan": 3}, {}, {}, {}],
                                                [{}, {}, {}, {}],
                                                [{}, {}, {}, {}],
                                                [{}, {}, {}, {}],
                                                [{}, {}, {}, {}]])

fig_main.append_trace(fig, row=1, col=1)
fig_main.update_xaxes(fixedrange=False, row=1, col=1)
fig_main.update_layout(height=1000, width=1000, title_text="Stacked Subplots")

app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='live-graph-1',
            animate=True,
            style=dict(width='1500px', height='700px'),
            config=dict(scrollZoom=True, displayModeBar='hover', responsive=True, autosizable=True)
        ),
        dcc.Interval(
                    id='graph-update-1',
                    interval=5000,
                    n_intervals=0
                )
    ]),
    # html.Div([
    #         dcc.Graph(
    #             id='live-graph-2',
    #             animate=True,
    #             style=dict(width='1500px', height='300px'),
    #             config=dict(scrollZoom=True, displayModeBar='hover')
    #         ),
    #         dcc.Interval(
    #                     id='graph-update-2',
    #                     interval=3600,
    #                     n_intervals=0
    #                 )
    #     ])
])


@app.callback(
    Output('live-graph-1', 'figure'),
    [Input('graph-update-1', 'n_intervals')]
)
def update_graph_scatter(n):
    response = api.get_candles_history(
        symbol='BTC_USD',
        resolution=15,
        from_sec=TimeConverter.get_now_in_sec() - 172800,
        to_sec=TimeConverter.get_now_in_sec()
    )

    candles_data = response['candles']
    candles_data.reverse()

    dates.clear()
    prices.clear()

    for n in candles_data:
        time1 = int(str(n['t'])[:-3])
        dates.append(TimeConverter.sec_to_date(time1))
        prices.append(float(n['c']))

    fig_main.update_traces(patch=dict(x=dates, y=prices), row=1, col=1)

    return fig_main


if __name__ == '__main__':
    app.run_server(debug=True, port=3005)
