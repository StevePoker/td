from api_manager.binance_api.api import BinanceAPI
from api_manager.hepler.TimeFormatter import TimeConverter
from indicators.umbra_cm import UmbraCM
from indicators.sind_7 import Sind7
from charts.candlestick import CandleStick

import pandas as pd
import plotly.graph_objects as go
import dash

from dash import dcc
from dash import html
from dash.dependencies import Output, Input
from plotly.subplots import make_subplots


data_x = []
data_y = []
interval_main = dict(interval='15m', prev_interval='15m')
candlestick_range = 100


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Dropdown(id='period',
                     options=[
                         {
                            'label': '5m',
                            'value': '5m'
                         },
                         {
                            'label': '15m',
                            'value': '15m'
                         },
                         {
                             'label': '30m',
                             'value': '30m'
                         },
                         {
                             'label': '1h',
                             'value': '1h'
                         },
                         {
                             'label': '2h',
                             'value': '2h'
                         },
                         {
                             'label': '4h',
                             'value': '4h'
                          },
                     ],
                     value='15m',
                     style={"width": "150px", "background-color": "White"},
                     searchable=False,
                     placeholder="Period",
                     clearable=False
                     ),
        dcc.Graph(
            id='live-graph-1',
            animate=True,
            style=dict(width='1500px', height='900px'),
            config=dict(scrollZoom=True, displayModeBar='hover')
        ),
        dcc.Interval(
            id='graph-update-1',
            interval=5000,
            n_intervals=0
        )
    ]
)

api = BinanceAPI()


def get_data(api, interval):
    data = api.get_candles(symbol='BTCUSDT', interval=interval)

    pd_data = pd.DataFrame.from_dict(data)

    pd_data['c'] = pd_data['c'].astype(float)
    pd_data['o'] = pd_data['o'].astype(float)
    pd_data['h'] = pd_data['h'].astype(float)
    pd_data['l'] = pd_data['l'].astype(float)

    pd_data_time = list(map(lambda i: int(str(i)[:-3]) + 1, pd_data['ot']))
    pd_data.update(dict(ot=pd_data_time))

    return pd_data


def get_indicators(data, indicator):
    indicators_dict = {
        'umbra_cm': UmbraCM.process,
        'sind_7': Sind7.process,
    }
    indicator_result = indicators_dict.get(indicator)(data)
    return indicator_result


def get_data_lines(data):
    fig1 = go.Scatter(x=list(map(lambda i: TimeConverter.sec_to_date(i, 7200), data['ot'])),
                      y=data['c'], yhoverformat='.2f', line=dict(color='black', width=3),
                      name='price')

    fig2 = go.Scatter(x=list(map(lambda i: TimeConverter.sec_to_date(i, 7200), data['ot'])),
                      y=data['c'],
                      name='price_layer',
                      line=dict(color='black'), mode='lines+markers+text', yhoverformat='.2f')

    fig3 = go.Scatter(x=list(map(lambda i: TimeConverter.sec_to_date(i, 7200), data['ot'])),
                      y=get_indicators(data, 'umbra_cm'), line=dict(color='blue', width=1),
                      name='umbra_cm', mode='lines+markers+text')

    fig4 = go.Scatter(x=list(map(lambda i: TimeConverter.sec_to_date(i, 7200), data['ot'])),
                      y=get_indicators(data, 'sind_7'), line=dict(color='firebrick', width=1, dash='dash'),
                      name='sind_7', mode='lines+markers+text')

    return dict(fig1=fig1, fig2=fig2, fig3=fig3, fig4=fig4)

# fig1 = go.Candlestick(x=list(map(lambda i: TimeConverter.sec_to_date(i, 7200), data_dict['ot'])),
#                       open=data_dict['o'],
#                       high=data_dict['h'],
#                       low=data_dict['l'],
#                       close=data_dict['c'],
#                       increasing={'fillcolor': 'white', 'line': {'color': 'black'}},
#                       decreasing={'fillcolor': 'black', 'line': {'color': 'black'}},
#                       name='ohlc'
#                       )


fig_main = make_subplots(rows=5, cols=1, print_grid=True, shared_xaxes=True, vertical_spacing=0.05,
                         specs=[[{"rowspan": 2, "colspan": 1}],
                                [{}],
                                [{"rowspan": 3, "colspan": 1, "secondary_y": True}],
                                [{}],
                                [{}]])

api_data = get_data(api=api, interval=interval_main.get('interval'))

lines = get_data_lines(api_data)

fig_main.add_trace(lines.get('fig1'), row=1, col=1)
fig_main.add_trace(lines.get('fig3'), row=3, col=1)
fig_main.add_trace(lines.get('fig4'), row=3, col=1)
fig_main.add_trace(lines.get('fig2'), secondary_y=True, row=3, col=1)

# CandleStick.create(fig=fig_main, row_pos=1, col_pos=1, data=api_data, range_size=candlestick_range)

fig_main.update_layout(height=900, width=1500, title_text="Stacked Subplots", hovermode='x unified',
                       xaxis_showticklabels=True, xaxis3_showticklabels=True)
fig_main.update_xaxes(rangeslider_visible=False)


@app.callback(
    Output('live-graph-1', 'figure'),
    [Input('graph-update-1', 'n_intervals'),
     Input('period', 'value')]
)
def update_graph_scatter(n, period):
    interval_main.update(dict(interval=period))

    api_data_update = get_data(api=api, interval=interval_main.get('interval'))
    updated_lines = get_data_lines(api_data_update)
    # fig1 = go.Candlestick(x=list(map(lambda i: TimeConverter.sec_to_date(i, 7200), data_dict_update['ot'])),
    #                       open=data_dict_update['o'],
    #                       high=data_dict_update['h'],
    #                       low=data_dict_update['l'],
    #                       close=data_dict_update['c'],
    #                       increasing={'fillcolor': 'white', 'line': {'color': 'black'}},
    #                       decreasing={'fillcolor': 'black', 'line': {'color': 'black'}},
    #                       xperiod0=str(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    #                       )

    fig_main.update_traces(updated_lines.get('fig1'), selector={'name': 'price'}, row=1, col=1)
    fig_main.update_traces(updated_lines.get('fig2'), selector={'name': 'price_layer'}, row=3, col=1)
    fig_main.update_traces(updated_lines.get('fig3'), selector={'name': 'umbra_cm'}, row=3, col=1)
    fig_main.update_traces(updated_lines.get('fig4'), selector={'name': 'sind_7'}, row=3, col=1)

    # if interval_main.get('interval') != interval_main.get('prev_interval'):
    #     fig_main.layout.shapes = ()
    #     CandleStick.create(fig=fig_main, row_pos=1, col_pos=1, data=api_data_update, range_size=candlestick_range)

    fig_main.update_yaxes(fixedrange=True, showgrid=False)
    fig_main.update_xaxes(showgrid=True)

    interval_main.update(dict(prev_interval=period))
    return fig_main


if __name__ == '__main__':
    app.run_server(debug=True, port=3006)
