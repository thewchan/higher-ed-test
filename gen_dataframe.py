"""Helper functions to generate desired dataframe."""
import pandas as pd
import sqlalchemy as sql
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

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


def generate_sql_connection(db_path):
    """Connect to database."""
    sql_connection = sql.create_engine(db_path)
    session_gen = sql.orm.sessionmaker(bind=sql_connection)
    sql_session = session_gen()

    return sql_connection, sql_session


def get_donations_df(db_path):
    """Generate df for all donations received grouped by schools."""
    sql_connection, sql_session = generate_sql_connection(db_path)
    overall_donations = (sql_session.query(
        DonationData.Institution_name.label('School'),
        func.sum(DonationData.Foreign_Gift_Amount).label('Amount')
    )
        .group_by(DonationData.Institution_name)
        .order_by(sql.desc('Amount'))
    )
    df = pd.read_sql(overall_donations.statement, sql_connection)
    sql_session.close()
    sql_connection.dispose()

    return df


def get_donationsTS_df(db_path, school):
    """Generate time series df of donations trends for the desired school."""
    sql_connection, sql_session = generate_sql_connection(db_path)
    donationTS = (sql_session.query(
        DonationData.Institution_name.label('School'),
        DonationData.Foreign_Gift_Received_Date.label('Date'),
        DonationData.Foreign_Gift_Amount.label('Amount'),
        DonationData.Country_of_Giftor.label('Donor Country'),
        DonationData.Giftor_Name.label('Donor'),
    ).filter(DonationData.Institution_name == school)
     .order_by('School')
    )

    df = pd.read_sql(
        donationTS.statement,
        sql_connection,
        parse_dates=['Date']
    ).fillna('Unknown')

    sql_session.close()
    sql_connection.dispose()

    return df


def get_donationsMAP_df(db_path, school):
    """Generate time series df of donations trends for the desired school."""
    sql_connection, sql_session = generate_sql_connection(db_path)
    donationTS = (sql_session.query(
        DonationData.Institution_name.label('School'),
        DonationData.Foreign_Gift_Received_Date.label('Date'),
        DonationData.Foreign_Gift_Amount.label('Amount'),
        DonationData.Country_of_Giftor.label('Donor Country'),
        DonationData.Country_Latitude.label('Latitude'),
        DonationData.Country_Longitude.label('Longitude'),
        DonationData.Score.label('Score')
    ).filter(DonationData.Institution_name == school)
    )

    df = pd.read_sql(
        donationTS.statement,
        sql_connection,
        parse_dates=['Date']
    )

    sql_session.close()
    sql_connection.dispose()

    return df
