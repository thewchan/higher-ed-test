"""Test app for higher ed donation visualization."""
import dash
import dash_core_components as dcc
import dash_html_components as html

from gen_dataframe import (get_donations_df,
                           get_donationsMAP_df,
                           get_donationsTS_df)
from gen_figures import (get_donation_bar,
                         get_donation_map,
                         get_donationTS_scatter)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
db_path = 'sqlite:///merged_data_w_coord.sqlite'

overall_donations_df = get_donations_df(db_path)
donationTS_df = get_donationsTS_df(db_path, 'Carnegie Mellon University')
donation_map_df = get_donationsMAP_df(db_path, 'Carnegie Mellon University')

donation_bar = get_donation_bar(overall_donations_df)
donationTS_scatter = get_donationTS_scatter(donationTS_df)
donation_map = get_donation_map(donation_map_df)

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
                    id='example-graph2',
                    figure=donationTS_scatter
                ),
                className='one-half column'
            ),
            html.Div(
                children=dcc.Graph(
                    id='example-graph3',
                    figure=donation_map
                ),
                className='one-half column'
            )
        ],
        className='row'
    ),
    html.Div(
        children=dcc.Graph(
            id='example-graph',
            figure=donation_bar,
        ),
        className='row'
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
