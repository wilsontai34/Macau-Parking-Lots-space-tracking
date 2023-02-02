import plotly.subplots as sp
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
from dash import Dash, dcc, html, Input, Output
from api import get_space_data, get_area_space
from Recommend import dis_sorted
import pandas as pd
import numpy as np

app = Dash(__name__)

app.title = "Macau Parking Space Live Monitoring"

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

pl={}

info = pd.read_csv('info.csv')
for ind in info.index:
    pl[str(ind)]=info['Name'][ind]

app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Div(
                    [
                        html.H4("澳泊--Macau Parking Space Live Monitoring", className="app__header__title"),
                        html.P(
                            "A real-time analysis for Macau Parking Lot's space changing.",
                            className="app__header__title--grey",
                        ),
                    ],
                    className="app__header__desc",
                ),
                html.Div(
                    [
                        html.A(
                            html.Img(
                                src=app.get_asset_url("must_logo_new.png"),
                                className="app__menu__img",
                            ),
                            href="https://www.must.edu.mo",
                        ),
                    ],
                    className="app__header__logo",
                ),
            ],
            className="app__header",
        ),
        html.Div(
            [   
                html.Div(
                    [
                        html.Div(
                            [html.H6('Real Live Tracking', className="graph__title")]
                        ),
                        dcc.Graph(
                            id="the_graph",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            ),
                        ),
                        dcc.Interval(
                            id='interval-component',
                            interval=5 * 1000,  # in milliseconds
                            n_intervals=0,
                        ),
                    ],
                    className="two-thirds column wind__speed__container",
                ),
                html.Div(
                    [   
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Parking Lots",
                                            className="graph__title",
                                        )
                                    ]
                                ), 
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            options=pl,
                                            value='0',
                                            id='dropdown',
                                            searchable=False,
                                            multi=False,
                                            clearable=False,
                                        ),
                                    ],
                                    className="slider",
                                ),
                                dcc.Graph(
                                    id="the_map",
                                    figure=dict(
                                        layout=dict(
                                            plot_bgcolor=app_color["graph_bg"],
                                            paper_bgcolor=app_color["graph_bg"],
                                        )
                                    )
                                ),
                            ],
                            className="graph__container first",
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id='the_table'
                                ),
                            ],
                            className="graph__container second",
                        )
                    ],
                    className="one-third column histogram__direction",     
                ),
            ],
            className="app__content",
        ),
    ],
    className="app__container",
)

@app.callback(Output('the_graph', 'figure'),
              Input('dropdown', 'value'),
              Input('interval-component', 'n_intervals'))

def tracking_graph(dropdown,interval):
    df = get_space_data(dropdown)

    # make subplots
    fig = sp.make_subplots(rows=5, cols=1, shared_xaxes=True)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 10, 't': 10
    }
    fig.add_trace({
        'x': df['Datetime'],
        'y': df['Car'],
        'name': 'Car',
        'mode': 'lines',
        'type': 'scatter',
        'line_color':"crimson"
    }, 1, 1)
    fig.add_trace({
        'x': df['Datetime'],
        'y': df['Motor'],
        'text': df['Datetime'],
        'name': 'Motor',
        'mode': 'lines',
        'type': 'scatter'
    }, 2, 1)
    fig.add_trace({
        'x': df['Datetime'],
        'y': df['Ecar'],
        'text': df['Datetime'],
        'name': 'Elec-Car',
        'mode': 'lines',
        'type': 'scatter'
    }, 3, 1)
    fig.add_trace({
        'x': df['Datetime'],
        'y': df['Emotor'],
        'text': df['Datetime'],
        'name': 'Elec-Motor',
        'mode': 'lines',
        'type': 'scatter'
    }, 4, 1)
    fig.add_trace({
        'x': df['Datetime'],
        'y': df['Disabled'],
        'text': df['Datetime'],
        'name': 'Disability',
        'mode': 'lines',
        'type': 'scatter',
    }, 5, 1)

    fig.update_xaxes(showline=True, linewidth=2, linecolor='grey', gridcolor=app_color['graph_bg'])
    fig.update_yaxes(showline=True, linewidth=2, linecolor='grey', gridcolor=app_color['graph_line'])
    fig.update_layout(  
                        height=700,
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color['graph_bg'],
                        autotypenumbers='convert types',
                        font=dict(
                            color='#fff'
                    )
    )
    return fig

@app.callback(Output('the_map', 'figure'),
              Input('interval-component', 'n_intervals'))

def map_graph(interval):
    lis = get_area_space('Car')
    mapbox_access_token = 'pk.eyJ1Ijoid2lsemVybzM0IiwiYSI6ImNsYnhsYXZreTBleDEzdnA4bjdyYnU0dmMifQ.cWNGi5OUAmNEMzECg4G1Kg'

    name = info['Name'].tolist()
    sub = info['Subdistrict'].tolist()

    tag_list = []
    for i in range(len(lis)):
        tag = name[i] + ' - ' + sub[i] + ' - ' + str(lis[i])
        tag_list.append(tag)

    fig = go.Figure(go.Scattermapbox(
        lat=info['Latitude'],
        lon=info['Longtitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size = 9,
            color = list(lis),  # using the color to representrest parking space
            cmax = 50,
            cmin = 0,
            showscale=True,
            reversescale=True
            #color = "dimgray"
        ),

        text=tag_list,  # tags with different info
    ))

    fig['layout']['margin'] = {
        'l': 5, 'r': 5, 'b': 5, 't': 5
    }

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        height = 500,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                #lat=22.187594,
                lat = 22.1635,
                lon=113.557198
            ),
            pitch=0,
            zoom=11.5
        ),
    )
    return fig

@app.callback(Output('the_table', 'figure'),
              Input('dropdown', 'value'))

def table(dropdown):
    parking_input = pl[dropdown]
    fig =  ff.create_table(dis_sorted(parking_input))
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
