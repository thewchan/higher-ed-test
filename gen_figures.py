"""Helper functions to generate figures."""
import plotly.express as px


def get_donation_bar(data, highlighted_bar=0):
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
    fig.update_traces({
        'selected': {'marker': {'opacity': 1.0}},
        'unselected': {'marker': {'opacity': 0.3}},
        'selectedpoints': [highlighted_bar]
    }
    )
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                buttons=list([
                    dict(
                        args=[{"visible": [True, True]},
                              {'xaxis': {'type': 'log'}}],
                        label="Log scale",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [True, False]},
                              {'xaxis': {'type': 'linear'}}],
                        label="Linear Scale",
                        method="update"
                    )
                ]),
                x=1.0,
                xanchor="right",
                yanchor="top",
                bgcolor='rgba(229, 236, 246, 0.5)',
                active=1,
            ),
        ]
    )

    return fig


def get_donationTS_scatter(data, school, school_abbrev):
    """Return scatter plot of the donation time series."""
    if ('-' in school_abbrev) and (school_abbrev != 'rose-hulman'):
        school_abbrev = '.'.join(school_abbrev.split('-'))

    fig = px.scatter(
        data,
        x='Date',
        y='Amount',
        custom_data=['Donor Country', 'Donor'],
        color_discrete_sequence=px.colors.qualitative.Alphabet,
        color='Donor Country',
        # title=school,
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
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                buttons=list([
                    dict(
                        args=[{"visible": [True, True]},
                              {'yaxis': {'type': 'log'}}],
                        label="Log scale",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [True, False]},
                              {'yaxis': {'type': 'linear'}}],
                        label="Linear Scale",
                        method="update"
                    )
                ]),
                x=0.15,
                xanchor="left",
                yanchor="middle",
                y=1.1,
                active=1
            ),
        ]
    )
    fig.add_layout_image(
        dict(
            source=f"http://logo.clearbit.com/{school_abbrev}.edu",
            xref="paper", yref="paper",
            x=0,
            y=1.1,
            sizex=0.18,
            sizey=0.18,
            xanchor="left",
            yanchor="middle"
        )
    )

    return fig


def get_donation_map(data, school):
    """Return donation map."""
    if school.endswith('(The)'):
        school = school.split(' (')[0]

    if school.endswith('The'):
        school = 'The ' + school.split(',')[0]

    fig = px.scatter_mapbox(
        data,
        lat="Latitude",
        lon="Longitude",
        color="Score",
        size=abs(data["Amount"]),
        custom_data=['Donor Country', 'Date', 'Amount', 'Score'],
        color_continuous_scale=px.colors.sequential.Bluered[::-1],
        opacity=0.5,
        size_max=15,
        zoom=0,
        title=f'Temporal and geographical donation trends of <br>{school}'
    )
    fig.update_layout(
        {'coloraxis': {'cmin': 0.0, 'cmax': 10.0},
         'mapbox_style': 'open-street-map'})
    fig.update_traces(
        hovertemplate=("Donor Country: %{customdata[0]}<br>"
                       "Date: %{customdata[1]|%Y-%m-%d}<br>"
                       "Amount: %{customdata[2]:$,}<br>"
                       "Democracy Score: %{customdata[3]}")
    )

    return fig
