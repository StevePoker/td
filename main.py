from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
from api_manager.binance_api.api import BinanceAPI
from plotly.subplots import make_subplots
from indicators.umbra_cm import UmbraCM
from indicators.sind_7 import Sind7

TIMEFRAME_DICT = {
    'M1': '1m',
    'M5': '5m',
    'M15': '15m',
    'M30': '30m',
    'H1': '1h',
    'H2': '2h',
    'H4': '4h',
    'D1': '1d'
}


def get_data(api, interval, symbol):
    data = api.get_candles(symbol=symbol, interval=interval)

    pd_data = pd.DataFrame.from_dict(data)

    pd_data['c'] = pd_data['c'].astype(float)
    pd_data['o'] = pd_data['o'].astype(float)
    pd_data['h'] = pd_data['h'].astype(float)
    pd_data['l'] = pd_data['l'].astype(float)

    pd_data_time = list(map(lambda i: int(str(i)[:-3]) + 10800, pd_data['ot']))
    pd_data.update(dict(ot=pd_data_time))

    return pd_data


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
api = BinanceAPI()


symbol_dropdown = html.Div([
    html.P('Symbol:'),
    dcc.Dropdown(
        id='symbol-dropdown',
        options=[{'label': 'BTCUSDT', 'value': 'BTCUSDT'},
                 {'label': 'RENUSDT', 'value': 'RENUSDT'}],
        value='BTCUSDT'
    )
])

timeframe_dropdown = html.Div([
    html.P('Timeframe:'),
    dcc.Dropdown(
        id='timeframe-dropdown',
        options=[{'label': timeframe, 'value': timeframe} for timeframe in TIMEFRAME_DICT.keys()],
        value='H2'
    )
])

num_bars_input = html.Div([
    html.P('Number of Candles'),
    dbc.Input(id='num-bar-input', type='number', value='40')
])

# creates the layout of the App
app.layout = html.Div([
    html.H1('Real Time Charts'),

    dbc.Row([
        dbc.Col(symbol_dropdown),
        dbc.Col(timeframe_dropdown),
        dbc.Col(num_bars_input)
    ]),

    html.Hr(),

    dcc.Interval(id='update', interval=500),

    html.Div(id='page-content')

], style={'margin-left': '5%', 'margin-right': '5%', 'margin-top': '20px'})

fig_main = make_subplots(rows=5, cols=1, print_grid=True, shared_xaxes=True, vertical_spacing=0.05,
                             specs=[[{"rowspan": 2, "colspan": 1}],
                                    [{}],
                                    [{"rowspan": 3, "colspan": 1, "secondary_y": True}],
                                    [{}],
                                    [{}]])

counter = {'value': 0}

fig_main.update_layout(height=900, width=1500, title_text="Stacked Subplots", hovermode='x unified',
                       xaxis_showticklabels=True, xaxis3_showticklabels=True)
fig_main.update_xaxes(rangeslider_visible=False)


@app.callback(
    Output('page-content', 'children'),
    Input('update', 'n_intervals'),
    State('symbol-dropdown', 'value'), State('timeframe-dropdown', 'value'), State('num-bar-input', 'value')
)
def update_ohlc_chart(interval, symbol, timeframe, num_bars):

    timeframe_str = timeframe
    timeframe = TIMEFRAME_DICT[timeframe]
    num_bars = int(num_bars)

    bars = get_data(api=api, interval=timeframe, symbol=symbol)

    bars['ot'] = pd.to_datetime(bars['ot'], unit='s')
    df = bars.tail(num_bars)

    fig1 = go.Candlestick(x=df['ot'],
                          open=df['o'],
                          high=df['h'],
                          low=df['l'],
                          close=df['c'], name='candle_price')

    fig2 = go.Scatter(x=df['ot'],
                      y=df['c'], yhoverformat='.2f', line=dict(color='black', width=1.5),
                      name='price', mode='lines+markers+text')

    fig3 = go.Scatter(x=df['ot'],
                      y=UmbraCM.process(df), line=dict(color='blue', width=1),
                      name='umbra_cm', mode='lines+markers+text')

    fig4 = go.Scatter(x=df['ot'],
                      y=Sind7.process(df), line=dict(color='firebrick', width=1, dash='dash'),
                      name='sind_7', mode='lines+markers+text')

    if counter['value'] == 0:
        fig_main.add_trace(fig1, row=1, col=1)
        fig_main.add_trace(fig2, row=3, col=1, secondary_y=True)
        fig_main.add_trace(fig3, row=3, col=1)
        fig_main.add_trace(fig4, row=3, col=1)
        counter['value'] += 1

    fig_main.update_yaxes(fixedrange=True, showgrid=False)
    fig_main.update_xaxes(showgrid=True)

    fig_main.update_traces(fig1, selector={'name': 'candle_price'}, row=1, col=1)
    fig_main.update_traces(fig2, selector={'name': 'price'}, row=3, col=1)
    fig_main.update_traces(fig3, selector={'name': 'umbra_cm'}, row=3, col=1)
    fig_main.update_traces(fig4, selector={'name': 'sind_7'}, row=3, col=1)

    return [
        html.H2(id='chart-details', children=f'{symbol} - {timeframe_str}'),
        dcc.Graph(figure=fig_main, config={'displayModeBar': True})
        ]


if __name__ == '__main__':
    app.run_server()
