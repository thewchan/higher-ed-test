"""Test app for higher ed donation visualization."""
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

# top10_by_counts = (
#     donations_df.groupby('Institution Name')
#     .count()
#     .iloc[:, 0]
#     .sort_values(ascending=True)
#     .iloc[-10:])

data = {school: donations
        for school, donations in
        (session.query(
            DonationData.Institution_name,
            func.sum(DonationData.Foreign_Gift_Amount).label('Amount'))
         .group_by(DonationData.Institution_name)
         .order_by(sql.desc('Amount'))
         )[:10]
        }

df = pd.DataFrame(
    data.items(),
    columns=['School', 'Amount']
)

fig = px.bar(
    df,
    x="School",
    y="Amount",
)

app.layout = html.Div(children=[
    html.H1(children='School Donations Test App'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
