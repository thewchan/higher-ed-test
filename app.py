"""Test app for higher ed donation visualization."""
import json
import re

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from gen_dataframe import (get_donations_df, get_donationsMAP_df,
                           get_donationsTS_df)
from gen_figures import (get_donation_bar, get_donation_map,
                         get_donationTS_scatter)

# Global scope variables
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
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
app.layout = html.Div(
    children=[
        html.Div(
            dbc.Navbar(
                [
                    html.A(
                        dbc.Row(
                            dbc.Col(
                                dbc.NavbarBrand(
                                    'Foreign Donations to US Universities',
                                    className='display-3'
                                )
                            ),
                            align='center',
                            no_gutters=True,
                        ),
                        href='#',
                    ),
                    dbc.NavbarToggler(id='navbar-toggler'),
                    dbc.Collapse(
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='school-dropdown',
                                        options=[{'label': school,
                                                  'value': abbrev}
                                                 for school, abbrev
                                                 in school_abbrev
                                                 .set_index('School')
                                                 .sort_index()['Abbrev']
                                                 .items()],
                                        value='cmu',
                                        style={'width': '30em'}
                                    ),
                                    width={'offset': 11}
                                ),
                                dbc.Col(
                                    dbc.NavLink(
                                        "About",
                                        href="#",
                                        className='ml-2'
                                    ),
                                    width={'offset': 12}
                                ),
                            ],
                            no_gutters=True,
                            className='ml-auto, flex-nowrap mt-3 mt-md-0',
                            align='center',
                        ),
                        id='navbar-collapse',
                        navbar=True,
                    ),
                ],
                className='navbar navbar-expand-lg navbar-light bg-light',
            ),
        ),
        html.Div(
            dbc.Jumbotron(
                dcc.Markdown(
                    """
                    This is a visualization tool for the disclosed foreign
                    donations received by US universities. Between 2012 and
                    2019. Choose or type a school name from the drop-down menu
                    see see donation received trends and sources. "Score" on
                    the map refers to the [Democracy Index]
                    (https://www.eiu.com/topic/democracy-index) as published
                    by [The Economist](https://www.economist.com/) in 2019. You
                    may also select a school from the total received foreign
                    donations by school bar chart at the bottom
                    (drag to zoom.). You may also isolate donations from a
                    particular country by double-clicking on the country at
                    the legend of the donation trend graph. The source of the
                    donation data is from the
                    [US Department of Education](https://catalog.data.gov/dataset/foreign-gifts-and-contracts-report-2011).
                    """,
                    # className='lead'
                ),
                className='jumbotron'
            ),
        ),
        html.Div(
            children=[
                html.Div(
                    dcc.Graph(
                        id='donation-map',
                        figure=donation_map,
                        clickData={
                            'points': [{'y': 'Carnegie Mellon University'}]
                        }
                    ),
                    className='one-half column'
                ),
                html.Div(
                    dcc.Graph(
                        id='donationTS',
                        figure=donationTS_scatter
                    ),
                    className='one-half column'
                ),
            ],
            className='row'
        ),
        html.Div(
            dcc.Graph(
                id='master-bar-graph',
                figure=donation_bar,
                clickData={'points': [{'y': 'Carnegie Mellon University'}]},
                selectedData={'points': [{'y': 'Carnegie Mellon University'}]},
            ),
            # className='row',
        ),
        html.Div(
            html.Pre(
                id='debug',
                style={
                    'border': 'thin lightgrey solid',
                    'overflowX': 'scroll'
                }
            )
        )
    ]
)


@ app.callback(
    [
        Output('donation-map', 'figure'),
        Output('donationTS', 'figure'),
    ],
    [Input('master-bar-graph', 'clickData')]
)
def update_upper_figures(clickData):
    school_re = re.compile(r'[^\"]')
    school = ''.join(
        school_re.findall(json.dumps(clickData['points'][0]['y']))
    )
    new_donationsMap_df = get_donationsMAP_df(db_path, school)
    new_donationTS_df = get_donationsTS_df(db_path, school)
    figureTS = get_donationTS_scatter(new_donationTS_df, school)
    figure_map = get_donation_map(new_donationsMap_df, school)
    return figure_map, figureTS


@ app.callback(
    [
        Output('master-bar-graph', 'figure'),
        Output('master-bar-graph', 'clickData'),
    ],
    [Input('school-dropdown', 'value')]
)
def drop_down_callbacks(value):
    school = (school_abbrev[school_abbrev['Abbrev'] == value]
              ['School'].values[0])
    clickData = {'points': [{'y': school}]}
    df = get_donations_df(db_path)
    school_idx = df[df['School'] == school].index[0]
    fig = get_donation_bar(df, school_idx)

    return fig, clickData


@ app.callback(
    Output('school-dropdown', 'value'),
    [Input('master-bar-graph', 'selectedData')]
)
def update_dropdown(selectedData):
    school_re = re.compile(r'[^\"]')
    school = ''.join(
        school_re.findall(json.dumps(selectedData['points'][0]['y']))
    )
    value = (school_abbrev[school_abbrev['School'] == school]['Abbrev']
             .values[0])

    return value


# @app.callback(
#     Output('debug', 'children'),
#     [Input('master-bar-graph', 'selectedData')]
# )
# def selected_data_debug(selectedData):
#     return json.dumps(selectedData)


if __name__ == '__main__':
    app.run_server(debug=True)
