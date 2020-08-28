"""Helper functions to generate figures."""
import plotly.express as px


def get_donation_bar(data):
    """Return the master horizontal bar graph."""
    fig = px.bar(
        data,
        x="Amount",
        y="School",
        orientation='h',
    )
    fig.update_yaxes(title_text='')
    fig.update_xaxes(tickprefix='$')
    fig.update_layout(clickmode='event+select')

    return fig


def get_donationTS_scatter(data, school):
    """Return scatter plot of the donation time series."""
    fig = px.scatter(
        data,
        x='Date',
        y='Amount',
        custom_data=['Donor Country', 'Donor'],
        color_discrete_sequence=px.colors.qualitative.Alphabet,
        color='Donor Country',
        title=school
    )
    fig.update_xaxes(title_text='')
    fig.update_yaxes(
        title_text='',
        tickprefix="$"
    )
    fig.update_traces(
        hovertemplate=("Date: %{x|%Y-%m-%d}<br>"
                       "Amount: %{y:$,}<br>"
                       "Donor Country: %{customdata[0]}<br>"
                       "Donor: %{customdata[1]}")
    )

    return fig


def get_donation_map(data, school):
    """Return donation map."""
    fig = px.scatter_mapbox(
        data,
        lat="Latitude",
        lon="Longitude",
        color="Score",
        size="Amount",
        custom_data=['Donor Country', 'Date', 'Amount', 'Score'],
        color_continuous_scale=px.colors.sequential.Bluered[::-1],
        opacity=0.5,
        size_max=15,
        zoom=0,
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_traces(
        hovertemplate=("Donor Country: %{customdata[0]}<br>"
                       "Date: %{customdata[1]|%Y-%m-%d}<br>"
                       "Amount: %{customdata[2]:$,}<br>"
                       "Democracy Score: %{customdata[3]}")
    )

    return fig
