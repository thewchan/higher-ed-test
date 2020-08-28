"""Test app for higher ed donation visualization."""
import json
import re

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from gen_dataframe import (get_donations_df, get_donationsMAP_df,
                           get_donationsTS_df)
from gen_figures import (get_donation_bar, get_donation_map,
                         get_donationTS_scatter)

# Global scope variables
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
db_path = 'sqlite:///merged_data_w_coord.sqlite'

with open('./school_abbrev.json', 'r') as f:
    school_abbrev = json.load(f)
school_abbrev = pd.DataFrame(
    school_abbrev.items(),
    columns=['School', 'Abbrev'])

# Default data when app first load
overall_donations_df = get_donations_df(db_path)
donationTS_df = get_donationsTS_df(db_path, 'Carnegie Mellon University')
donation_map_df = get_donationsMAP_df(db_path, 'Carnegie Mellon University')
donation_bar = get_donation_bar(overall_donations_df)
donationTS_scatter = get_donationTS_scatter(donationTS_df,
                                            'Carnegie Mellon University')
donation_map = get_donation_map(donation_map_df,
                                'Carnegie Melon University')

# Dashboard layout
app.layout = html.Div(children=[
    html.Div(
        children=html.H1(
            children='School Donations Test App'
        ),
        className='row'
    ),
    html.Div(
        children=[
            html.Div(
                children=dcc.Graph(
                    id='donationTS',
                    figure=donationTS_scatter
                ),
                className='one-half column'
            ),
            html.Div(
                children=dcc.Graph(
                    id='donation-map',
                    figure=donation_map,
                    clickData={
                        'points': [{'y': 'Carnegie Mellon University'}]
                    }
                ),
                className='one-half column'
            )
        ],
        className='row'
    ),
    html.Div(
        children=dcc.Dropdown(
            id='school-dropdown',
            options=[
                {'label': school, 'value': abbrev}
                for school, abbrev
                in school_abbrev.set_index('School')['Abbrev'].items()
            ],
            value='cmu'
        )
    ),
    html.Div(
        children=dcc.Graph(
            id='master-bar-graph',
            figure=donation_bar,
            clickData={'points': [{'y': 'Carnegie Mellon University'}]},
            selectedData=None,
        ),
        className='row',
    ),
    html.Div(
        children=html.Pre(
            id='debug',
            style={
                'border': 'thin lightgrey solid',
                'overflowX': 'scroll'
            }
        )
    )
])


@app.callback(
    Output('donationTS', 'figure'),
    [Input('master-bar-graph', 'clickData')]
)
def update_donationTS_scatter(clickData):
    school_re = re.compile(r'[^\"]')
    school = ''.join(
        school_re.findall(json.dumps(clickData['points'][0]['y']))
    )
    new_donationTS_df = get_donationsTS_df(db_path, school)
    figure = get_donationTS_scatter(new_donationTS_df, school)
    return figure


@app.callback(
    Output('donation-map', 'figure'),
    [Input('master-bar-graph', 'clickData')]
)
def update_donation_map(clickData):
    school_re = re.compile(r'[^\"]')
    school = ''.join(
        school_re.findall(json.dumps(clickData['points'][0]['y']))
    )
    new_donationsMap_df = get_donationsMAP_df(db_path, school)
    figure = get_donation_map(new_donationsMap_df, school)
    return figure


@app.callback(
    Output('master-bar-graph', 'clickData'),
    [Input('school-dropdown', 'value')]
)
def update_clickData_master(value):
    school = (school_abbrev[school_abbrev['Abbrev'] == value]
              ['School'].values[0])
    clickData = {'points': [{'y': school}]}

    return clickData


@app.callback(
    Output('master-bar-graph', 'selectedData'),
    [Input('school-dropdown', 'value')]
)
def update_selectedData_master(value):
    school = (school_abbrev[school_abbrev['Abbrev'] == value]
              ['School'].values[0])
    selectedData = {'points': [{'y': school}]}

    return selectedData


@app.callback(
    Output('debug', 'children'),
    [Input('master-bar-graph', 'selectedData')]
)
def selected_data_debug(selectedData):
    return json.dumps(selectedData)


if __name__ == '__main__':
    app.run_server(debug=True)
