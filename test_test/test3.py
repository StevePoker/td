import dash
import plotly
import datetime

from dash.dependencies import Output, Input
from dash import dcc
from dash import html
from api_manager.exmo_api.api import ExmoAPI
from api_manager.hepler.TimeFormatter import TimeConverter

api = ExmoAPI()
data_x = []
data_y = []

app = dash.Dash(__name__)

# app.layout = html.Div(
#     [
#         dcc.Graph(
#             id='live-graph',
#             animate=True,
#             style=dict(width='1500px', height='900px'),
#             config=dict(scrollZoom=True, displayModeBar='hover')
#         ),
#         dcc.Interval(
#             id='graph-update',
#             interval=3600,
#             n_intervals=0
#         ),
#     ]
# )

app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='live-graph-1',
            animate=True,
            style=dict(width='1500px', height='700px'),
            config=dict(scrollZoom=True, displayModeBar='hover')
        ),
        dcc.Interval(
                    id='graph-update-1',
                    interval=50000,
                    n_intervals=0
                )
    ]),
    html.Div([
            dcc.Graph(
                id='live-graph-2',
                animate=True,
                style=dict(width='1500px', height='300px'),
                config=dict(scrollZoom=True, displayModeBar='hover')
            ),
            dcc.Interval(
                        id='graph-update-2',
                        interval=50000,
                        n_intervals=0
                    )
        ])
])


result_1 = api.get_candles_history(
    symbol='BTC_USD',
    resolution=5,
    from_sec=TimeConverter.get_now_in_sec() - 172800,
    to_sec=TimeConverter.get_now_in_sec()
)

data1 = result_1['candles']
data1.reverse()

for n in data1:
    time1 = int(str(n['t'])[:-3])
    data_x.append(TimeConverter.sec_to_date(time1))
    data_y.append(float(n['c']))


def update_data():
    data_x.clear()
    data_y.clear()

    from_sec = TimeConverter.get_now_in_sec() - 172800
    to_sec = TimeConverter.get_now_in_sec()

    result = api.get_candles_history(
        symbol='BTC_USD',
        resolution=5,
        from_sec=from_sec,
        to_sec=to_sec
    )

    data2 = result['candles']
    data2.reverse()

    for i in data2:
        time = int(str(i['t'])[:-3])
        data_x.append(TimeConverter.sec_to_date(time))
        data_y.append(float(i['c']))


@app.callback(
    Output('live-graph-1', 'figure'),
    [Input('graph-update-1', 'n_intervals')]
)
def update_graph_scatter(n):
    update_data()
    print(data_y)
    print(data_x)

    data = plotly.graph_objs.Scatter(
        x=data_x,
        y=data_y,
        name='Scatter',
        mode='lines'
    )

    # return {'data': [data],
    #         'layout': go.Layout(
    #             yaxis=dict(
    #                 range=[min(data_y), max(data_y)]
    #             ),
    #             xaxis=dict(
    #                 range=[min(data_x), max(data_y)]
    #             )
    #         )
    #             }
    return {'data': [data]}


@app.callback(
    Output('live-graph-2', 'figure'),
    [Input('graph-update-2', 'n_intervals')]
)
def update_graph_scatter(n):
    update_data()

    data = plotly.graph_objs.Scatter(
        x=data_x,
        y=data_y,
        name='Scatter',
        mode='lines'
    )
    return {'data': [data]}


if __name__ == '__main__':
    app.run_server(debug=True, port=3004)
