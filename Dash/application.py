import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Input, Output

import plotly.plotly as py

import numpy as np
import pandas as pd

from config import username, api_key

py.sign_in(username, api_key)

#initialize the dash app
app = Dash(__name__)

application = app.server

#load the beer style data
df = pd.read_csv("../data/style_plus_beer.csv")
df_style_abv = df[['Super Style', 'abv']]


#clean data

# values for our dropdown
dropdown_val = df_style_abv['Super Style'].unique()

# define the color palette
colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5', '#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd', '#ccebc5', '#ffed6f', '#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#999999', '#621e15', '#e59076', '#128dcd', '#083c52', '#64c5f2', '#61afaf', '#0f7369', '#9c9da1', '#365e96', '#983334', '#77973d', '#5d437c', '#36869f', '#d1702f', '#8197c5', '#c47f80', '#acc484', '#9887b0', '#2d588a', '#58954c', '#e9a044', '#c12f32', '#723e77', '#7d807f', '#9c9ede', '#7375b5', '#4a5584', '#cedb9c', '#b5cf6b', '#8ca252', '#637939', '#e7cb94', '#e7ba52', '#bd9e39', '#8c6d31', '#e7969c', '#d6616b', '#ad494a', '#843c39', '#de9ed6', '#ce6dbd', '#a55194', '#7b4173', '#000000', '#0000FF']

################################################################
# build out the HTML
app.layout = html.Div(className="container", style={"padding":"10px"}, children=[
    html.Div(className="jumbotron text-center", children=[
        html.H1("Beer Style Analysis"),
        html.P("Select two beers to visualize the data"),
        html.P("Use the slider to choose the significance of the test")
    ]),
    dcc.Dropdown(className="col-md-4", style={"margin-bottom": "10px"}, id="dropdown_x",
        options=[
            {'label':val, 'value':val} for val in dropdown_val
        ],
        value=dropdown_val[0]
    ),
    dcc.Dropdown(className="col-md-4", style={"margin-bottom": "10px"}, id="dropdown_y",
        options=[
            {'label':val, 'value':val} for val in dropdown_val
        ],
        value=dropdown_val[1]
    ),
    html.Br(),

    # dcc.Slider(id='slider_n',
    #     min=1,
    #     max=9,
    #     marks={i:'{}'.format(i) for i in range (1,10)},
    #     value=3
    # ),
    html.Br(),

    html.Div(style={"padding":"20px"}, children=[
        dcc.Graph(id="cluster")
    ])
])

########################################################
# import external css
app.css.append_css({"external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"})

#import external javascript
app.scripts.append_script({"external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"})

#########################################################
# Callback functions to update plots

@app.callback(Output('cluster', 'figure'), [Input("dropdown_x", "value"), Input("dropdown_y", "value")])
def update_graph(x_val, y_val):
    df = pd.read_csv("../data/style_plus_beer.csv")
    df_style_abv = df[['Super Style', 'abv']]
    data = []
    # plot the actual labels
    c=0
    for i in [x_val, y_val]:
        print(i)
        #split up the clusters to visualize and extract sepal length and width
        df = df_style_abv[df_style_abv['Super Style'] == i]
        data.append({
            'x': df['abv'],
            'type': 'histogram',
            'name':i,
            'xbins': dict(
                        start=1,
                        end=20,
                        size=1),
            'marker': dict(
                color = colors[c],
                opacity=0.75
            )
        })
        c +=2
    layout = {
    'hovermode':'closest',
    'barmode':'overlay',
    'margin': {
        'r':10,
        't':25,
        'b':40,
        'l':60
    },
    'title': 'Comparing ABV of Beer Styles',
    'xaxis': {
        #'domain': [0,1],
        'title': 'ABV'
    },
    'yaxis': {
        #'domain': [0,1],
        'title': 'Count'
    }
}   


    fig = {"data": data, "layout":layout}
    return fig

if __name__ == '__main__':
    application.run()