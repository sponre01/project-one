from scipy.stats import ttest_ind as ttest

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Input, Output

import plotly.plotly as py
import plotly.figure_factory as ff

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
        html.P("Use the slider to choose the confidence interval of the test")
    ]),
    dcc.Slider(id='slider_n',
        max=3,
        marks={0:'90%', 1:'95%', 2:'97%', 3:'99%'},
        value=1
    ),
    html.Br(),
    html.Br(),
    ###### testing #####
    html.Div([
    html.Div([
        html.Div([
            html.H3('Select 2 Beers'),

            dcc.Dropdown(className="col-md-6", style={"margin-bottom": "10px", "margin-right":"0px"}, id="dropdown_x",
        options=[
            {'label':val, 'value':val} for val in dropdown_val
        ],
        value=dropdown_val[0]
    ),
            dcc.Dropdown(className="col-md-6", style={"margin-bottom": "10px"}, id="dropdown_y",
        options=[
            {'label':val, 'value':val} for val in dropdown_val
        ],
        value=dropdown_val[1]
    )

        ], className="six columns"),

        html.Div([
            html.H3('Insights'),
            # html.P("p = 0.6246246", id='stat_ob'),
            html.P(children=[
                dcc.Markdown(
                    children='p = 0.1334623 &nbsp more stuff; ',
                    id='stat_ob')
            ]),
            #html.P("There is no difference between the average value of the populations of Blah and Blah2")

        ], className="six columns"),
    ], className="row")
]),

    html.Br(),

    html.Div(style={"padding":"20px"}, children=[
        dcc.Graph(id="cluster")
    ])
])

########################################################
# import external css
app.css.append_css({"external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"})
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


#import external javascript
app.scripts.append_script({"external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"})

#########################################################
# Callback functions to update plots
app.config['suppress_callback_exceptions']=True

@app.callback(Output('cluster', 'figure'), [Input("dropdown_x", "value"), Input("dropdown_y", "value")])
def update_graph(x_val, y_val):
    df = pd.read_csv("../data/style_plus_beer.csv")
    df_style_abv = df[['Super Style', 'abv']]
   
    hist_data = [np.array(df_style_abv[df_style_abv['Super Style'] == x_val]['abv'].dropna()), np.array(df_style_abv[df_style_abv['Super Style'] == y_val]['abv'].dropna())]

    group_labels = [x_val, y_val]

    fig = ff.create_distplot(hist_data, group_labels, bin_size=.2)
    return fig

@app.callback(Output('stat_ob', 'children'), [Input("dropdown_x", "value"), Input("dropdown_y", "value"), Input("slider_n", "value")])
def update_stats(x_val, y_val, n):
    confidence = [.9, .95, .97, .99]
    a = round(1-confidence[n], 2)
    df = pd.read_csv("../data/style_plus_beer.csv")
    df_style_abv = df[['Super Style', 'abv']]

    df_x = df_style_abv[df_style_abv['Super Style'] == x_val]
    df_y = df_style_abv[df_style_abv['Super Style'] == y_val]
    
    results = ttest(np.array(df_x['abv'].dropna()), np.array(df_y['abv'].dropna()), equal_var=False)
    p_value = round(results[1], 4)
    if p_value > a:
        output_p = f"p = {p_value}, which is greater than our alpha value of {a}, therefore we fail to reject the null hypothesis. Then we are {round(confidence[n]*100,0)}% confident that there is no difference between the averge values of the 2 populations."
    else:
        output_p = f"p = {p_value}, which is less than our alpha value of {a}, therefore we reject the null hypothesis. Then we are {round(confidence[n]*100,0)}% confident that there is a statistical difference between the average values of the 2 populations."
    return output_p




if __name__ == '__main__':
    application.run()