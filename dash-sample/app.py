import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import json
from textwrap import dedent as d
from datetime import datetime
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'cb5392c35661370d95f300086accea51/raw/'
    '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
    'indicators.csv')

df1 = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv')

df2 = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}
available_indicators = df['Indicator Name'].unique()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

num = 3
markdown_text=f'''
    ### Dash and markdown
    you can list number of stuff here  
    {num}
    ```
    python app.py
    ```


'''
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


app.layout = html.Div(children=[
    html.Div(children=[
        html.H1(
        children='TMHCC Infra Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
        )
    ]),
    html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            id='year-slider',
            min=df2['year'].min(),
            max=df2['year'].max(),
            value=df2['year'].min(),
            marks={str(year): str(year) for year in df2['year'].unique()},
            step=None
        )
    ]),
    html.Div([
        html.H3(style={'textAlign': 'center'}, children=['Interaction visualization 1']),
        dcc.Graph(
            id='basic-interactions',
            figure={
                'data': [
                    {
                        'x': [1, 2, 3, 4],
                        'y': [4, 1, 3, 5],
                        'text': ['a', 'b', 'c', 'd'],
                        'customdata': ['c.a', 'c.b', 'c.c', 'c.d'],
                        'name': 'Trace 1',
                        'mode': 'markers',
                        'marker': {'size': 12}
                    },
                    {
                        'x': [1, 2, 3, 4],
                        'y': [9, 4, 1, 4],
                        'text': ['w', 'x', 'y', 'z'],
                        'customdata': ['c.w', 'c.x', 'c.y', 'c.z'],
                        'name': 'Trace 2',
                        'mode': 'markers',
                        'marker': {'size': 12}
                    }
                ],
                'layout': {
                    'clickmode': 'event+select'
                }
            }
        ),

        html.Div(className='row', children=[
            html.Div([
                dcc.Markdown(d("""
                    **Hover Data**

                    Mouse over values in the graph.
                """)),
                html.Pre(id='hover-data', style=styles['pre'])
            ], className='three columns'),

            html.Div([
                dcc.Markdown(d("""
                    **Click Data**

                    Click on points in the graph.
                """)),
                html.Pre(id='click-data', style=styles['pre']),
            ], className='three columns'),

            html.Div([
                dcc.Markdown(d("""
                    **Selection Data**

                    Choose the lasso or rectangle tool in the graph's menu
                    bar and then select points in the graph.

                    Note that if `layout.clickmode = 'event+select'`, selection data also 
                    accumulates (or un-accumulates) selected data if you hold down the shift
                    button while clicking.
                """)),
                html.Pre(id='selected-data', style=styles['pre']),
            ], className='three columns'),

            html.Div([
                dcc.Markdown(d("""
                    **Zoom and Relayout Data**

                    Click and drag on the graph to zoom or click on the zoom
                    buttons in the graph's menu bar.
                    Clicking on legend items will also fire
                    this event.
                """)),
                html.Pre(id='relayout-data', style=styles['pre']),
            ], className='three columns')
        ])
    ]),
    html.Div([
        html.H3(style={'textAlign': 'center'}, children=['Interaction visualization 2']),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-xaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Fertility rate, total (births per woman)'
                ),
                dcc.RadioItems(
                    id='crossfilter-xaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ],
            style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='crossfilter-yaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Life expectancy at birth, total (years)'
                ),
                dcc.RadioItems(
                    id='crossfilter-yaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),

        html.Div([
            dcc.Graph(
                id='crossfilter-indicator-scatter',
                hoverData={'points': [{'customdata': 'Japan'}]}
            )
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
        html.Div([
            dcc.Graph(id='x-time-series'),
            dcc.Graph(id='y-time-series'),
        ], style={'display': 'inline-block', 'width': '49%'}),

        html.Div(dcc.Slider(
            id='crossfilter-year--slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=df['Year'].max(),
            marks={str(year): str(year) for year in df['Year'].unique()}
        ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
    ]),
    html.Div(children=[
        dcc.Tabs(id='tabs', value='tab-1', children=[
            dcc.Tab(label='Global', value='Global'),
            dcc.Tab(label='Houston', value='Houston'),
            dcc.Tab(label='UK', value='UK')
        ]),
        html.Div(id='tabs-content')
    ]),
    html.Div(children=[
        dcc.Markdown(children=markdown_text)
    ]),
    html.Div(style={'backgroundColor': colors['background'], 'columnCount':2}, children=[
        html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
        }),


        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1,2,3], 'y':[4,1,2], 'type':'bar', 'name':'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    }
                }
            }
        ),

        html.Div(children='Dash: A web application framework for Python2.', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        dcc.Graph(
            id='example-graph2',
            figure={
                'data': [
                    {'x': [1,2,3,4], 'y':[4,1,2,19], 'type':'bar', 'name':'Japan'},
                    {'x': [1, 2, 3,4], 'y': [10, 2, 0,6], 'type': 'bar', 'name': 'USA'},
                ],
                'layout': {
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    }
                }
            }
        )
    ]),
    html.Div(children=[
        dcc.ConfirmDialogProvider(children=html.Button('Click ME'),
        id='danger-danger',
        message='Danger danger. Are you sure you want to continue?'
        ),
        html.Div(children=[
            html.H4(children='multi output'),
            dcc.Input(
                id='num',
                type='number',
                value=5
            ),
            html.Table([
                html.Tr([html.Td(['x', html.Sup(2)]), html.Td(id='square')]),
                html.Tr([html.Td(['x', html.Sup(3)]), html.Td(id='cube')]),
                html.Tr([html.Td(['2', html.Sup('x')]), html.Td(id='twos')]),
                html.Tr([html.Td(['3', html.Sup('x')]), html.Td(id='threes')]),
                html.Tr([html.Td(['x', html.Sup('x')]), html.Td(id='x^x')]),
            ])
        ]),
        html.Div(children=[
            html.P('Enter a number to see its prime factors'),
            dcc.Input(id='in-prime', type='number', debounce=True, min=1, step=1),
            html.P(id='err-prime', style={'color':'red'}),
            html.P(id='out-prime')
        ])
    ]),
    html.Div(children=[
        html.H4(children='US Agriculture Exports (2011)'),
        generate_table(df1)
    ]),
    html.Div(style={'textAlign': 'center'}, children=[
        html.H3("Core components")
    ]),
    html.Div(style={'columnCount': 2}, children=[
        html.Label('Dropdown: Region option'),
        dcc.Dropdown(
            options=[
                {'label':'North America - Houston', 'value': 'HOU'},
                {'label':'Europe - United Kingdam', 'value': 'UK'}
            ],
            value='HOU'
        ),

        html.Label('Multi-select dropdown: Resources to be shown'),
        dcc.Dropdown(
            options=[
                {'label':'CPU', 'value': 'CPU'},
                {'label':'Memory', 'value': 'Memory'},
                {'label':'Network', 'value': 'Network'},
                {'label':'Storage', 'value': 'Storage'},
            ],
            value=['CPU', 'Memory'],
            multi=True
        ),
        html.Label("Radio items: Resources to be shown"),
        dcc.RadioItems(
            options=[
                {'label':'CPU', 'value': 'CPU'},
                {'label':'Memory', 'value': 'Memory'},
                {'label':'Network', 'value': 'Network'},
                {'label':'Storage', 'value': 'Storage'},
            ],
            value="CPU"
        ),
        html.Label("Checkbox: Resources to be shown"),
        dcc.Checklist(
            options=[
                {'label':'CPU', 'value': 'CPU'},
                {'label':'Memory', 'value': 'Memory'},
                {'label':'Network', 'value': 'Network'},
                {'label':'Storage', 'value': 'Storage'},
            ],
            value=["CPU"]
        ),
        html.Label('Text Input'),
        dcc.Input(value='HOU', type='text'),

        html.Label('Slider'),
        dcc.Slider(
            min=0,
            max=10,
            marks={i:'Label{}'.format(i) if i == 1 else str(i) for i in range(1, 10)},
            value=5
        )

    ]),
    html.Div(children=[
        html.Label('Data picker'),
        dcc.DatePickerSingle(
            id='date-picker',
            date=datetime(2019, 9, 24)
        ),
        html.Label('Data range picker'),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=datetime(2019, 9, 24),
            end_date_placeholder_text='pick a date!'

        ),

        html.Label('input button'),
        html.Div(dcc.Input(id='input-box', type='text')),
        html.Button('Submit', id='input-button'),
        html.Div(id='output-container-button', children='Enter a value and press submit')
    ])
    
])


@app.callback(
    Output('output-container-button', 'children'),
    [Input('input-button', 'n_clicks')],
    [State('input-box', 'value')])
def update_output(n_clicks, value):
    if n_clicks is None:
        raise PreventUpdate
    return f'The input value was {value} and the button has been clicked {n_clicks}'

@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')])
def render_tab_content(tab):
    if tab == 'Global':
        return html.Div(children=[
            html.H3(tab),
            render_content(tab)
        ])
    elif tab == 'Houston':
        return html.Div(children=[
            html.H3(tab),
            render_content(tab)
        ])
    else:
        return html.Div(children=[
            html.H3(f'{tab} not available')
        ])

def render_content(country):
    return dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                    350, 430, 474, 526, 488, 537, 500, 439],
                    name='Rest of world',
                    marker=go.bar.Marker(
                        color='rgb(55, 83, 109)'
                    )
                ),
                go.Bar(
                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                    299, 340, 403, 549, 499],
                    name='China',
                    marker=go.bar.Marker(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=go.Layout(
                title=f'{country} Export of Plastic Scrap',
                showlegend=True,
                legend=go.layout.Legend(
                    x=0,
                    y=1.0
                ),
                margin=go.layout.Margin(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='my-graph'
    ) 

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def upate_figure(selected_year):
    filtered_df = df2[df2.year==selected_year]
    traces = []
    for continent in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent']==continent]
        traces.append(go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width':0.5, 'color':'white'}
            },
            name=continent
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type':'log', 'title':'GDP Per Capita'},
            yaxis={'title':'Life expectancy', 'range':[20,90]},
            margin={'l':40, 'b':40, 't':10,'r':10},
            legend={'x':0, 'y':1},
            hovermode='closest'
        )
    }

@app.callback(
    [Output('square', 'children'),
    Output('cube', 'children'),
    Output('twos', 'children'),
    Output('threes', 'children'),
    Output('x^x', 'children'),],
    [Input('num', 'value')])
def callback_factor(x):
    if x is None:
        raise PreventUpdate
    return x**2, x**3, 2**x, 3**x, x**x

@app.callback(
    [Output('out-prime', 'children'), Output('err-prime', 'children')],
    [Input('in-prime', 'value')])
def show_factors(num):
    if num is None:
        raise PreventUpdate

    factors = prime_factors(num)
    if len(factors) == 1:
        return dash.no_update, f'{factors} is prime!'

    return f"{num} is {'*'.join(str(n) for n in factors)}", ''

def prime_factors(num):
    n, i, out = num, 2, []
    while i * i <= n:
        if n % i == 0:
            n = int(n/i)
            out.append(i)

        else:
            i += 1 if i == 2 else 2
    out.append(n)
    return out

@app.callback(
    Output('hover-data', 'children'),
    [Input('basic-interactions', 'hoverData')])
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(
    Output('click-data', 'children'),
    [Input('basic-interactions', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
    Output('selected-data', 'children'),
    [Input('basic-interactions', 'selectedData')])
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)


@app.callback(
    Output('relayout-data', 'children'),
    [Input('basic-interactions', 'relayoutData')])
def display_selected_data(relayoutData):
    return json.dumps(relayoutData, indent=2)

@app.callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    [Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-yaxis-column', 'value'),
     Input('crossfilter-xaxis-type', 'value'),
     Input('crossfilter-yaxis-type', 'value'),
     Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Year'] == year_value]

    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }


@app.callback(
    Output('x-time-series', 'figure'),
    [Input('crossfilter-indicator-scatter', 'hoverData'),
     Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@app.callback(
    Output('y-time-series', 'figure'),
    [Input('crossfilter-indicator-scatter', 'hoverData'),
     Input('crossfilter-yaxis-column', 'value'),
     Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)

