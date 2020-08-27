"""Test app for higher ed donation visualization."""
from collections import namedtuple

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import sqlalchemy as sql
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

Base = declarative_base()


class DonationData(Base):
    """Class for the donation data table."""

    __tablename__ = 'donation_data'

    Index = sql.Column(sql.Integer, primary_key=True)
    Country_of_Giftor = sql.Column(sql.String)
    Institution_name = sql.Column(sql.String)
    ID = sql.Column(sql.Integer)
    OPEID = sql.Column(sql.Integer)
    City = sql.Column(sql.String)
    State = sql.Column(sql.String)
    Foreign_Gift_Received_Date = sql.Column(sql.String)
    Foreign_Gift_Amount = sql.Column(sql.Integer)
    Gift_Type = sql.Column(sql.String)
    Giftor_Name = sql.Column(sql.String)
    Country_to_merge_on = sql.Column(sql.String)
    Rank = sql.Column(sql.Float)
    Score = sql.Column(sql.Float)
    Electoral_process_and_pluralism = sql.Column(sql.Float)
    Functioning_of_government = sql.Column(sql.Float)
    Political_participation = sql.Column(sql.Float)
    Political_culture = sql.Column(sql.Float)
    Civil_liberties = sql.Column(sql.Float)
    Regime_type = sql.Column(sql.String)
    Region = sql.Column(sql.String)
    Country_Latitude = sql.Column(sql.Float)
    Country_Longitude = sql.Column(sql.Float)
    School_Latitude = sql.Column(sql.Float)
    SChool_Longitude = sql.Column(sql.Float)


engine = sql.create_engine('sqlite:///merged_data_w_coord.sqlite')
session_gen = sql.orm.sessionmaker(bind=engine)
session = session_gen()


overall_donations = {school: donations
                     for school, donations in
                     (session.query(
                         DonationData.Institution_name,
                         func.sum(
                             DonationData.Foreign_Gift_Amount).label('Amount')
                     )
                         .group_by(DonationData.Institution_name)
                         .order_by(sql.desc('Amount'))
                     )}

school_donations_by_date = [
    namedtuple(
        'donations_by_date',
        ['school', 'date', 'donation', 'country', 'giftor']
    )(school, date, donation, country, giftor)
    for school, date, donation, country, giftor
    in session.query(
        DonationData.Institution_name,
        DonationData.Foreign_Gift_Received_Date,
        DonationData.Foreign_Gift_Amount,
        DonationData.Country_of_Giftor,
        DonationData.Giftor_Name,
    ).filter(
        DonationData.Institution_name == 'Stanford University'
    )
]

school_donation_map = [
    namedtuple(
        'donation_map',
        ['school', 'date', 'donation', 'country', 'lat', 'lon', 'score']
    )(school, date, donation, country, lat, lon, score)
    for school, date, donation, country, lat, lon, score
    in session.query(
        DonationData.Institution_name,
        DonationData.Foreign_Gift_Received_Date,
        DonationData.Foreign_Gift_Amount,
        DonationData.Country_of_Giftor,
        DonationData.Country_Latitude,
        DonationData.Country_Longitude,
        DonationData.Score,
    ).filter(
        DonationData.Institution_name == 'Stanford University'
    )
]


df = pd.DataFrame(
    overall_donations.items(),
    columns=['School', 'Amount of Foreign Donations Received']
)

df2 = pd.DataFrame(school_donations_by_date).fillna('Unknown')
df2['date'] = pd.to_datetime(df2['date'])
df2 = df2.sort_values('date')

df3 = pd.DataFrame(school_donation_map).fillna('Unknown')
# df3['date'] = pd.to_datetime(df3['date'])

fig = px.bar(
    df,
    x="Amount of Foreign Donations Received",
    y="School",
    orientation='h',
)
fig.update_yaxes(title_text='')
fig.update_xaxes(tickprefix='$')

fig2 = px.scatter(
    df2,
    x='date',
    y='donation',
    hover_data=['country', 'giftor']
)
fig2.update_xaxes(title_text='')
fig2.update_yaxes(
    title_text='',
    tickprefix="$"
)

# px.set_mapbox_access_token(open(".mapbox_token").read())
fig3 = px.scatter_mapbox(
    df3,
    lat="lat",
    lon="lon",
    color="score",
    size="donation",
    color_continuous_scale=px.colors.sequential.Bluered[::-1],
    # reversescale=True,
    size_max=15,
    zoom=0,
    hover_data=['country', 'date'],
    )
fig3.update_layout(mapbox_style="open-street-map")

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
                    figure=fig2
                ),
                className='one-half column'
            ),
            html.Div(
                children=dcc.Graph(
                    id='example-graph3',
                    figure=fig3
                ),
                className='one-half column'
            )
        ],
        className='row'
    ),
    html.Div(
        children=dcc.Graph(
            id='example-graph',
            figure=fig,
        ),
        className='row'
    )
]
)


if __name__ == '__main__':
    app.run_server(debug=True)
