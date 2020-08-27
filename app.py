"""Test app for higher ed donation visualization."""
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from gen_dataframe import (get_donations_df, get_donationsMAP_df,
                           get_donationsTS_df)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
db_path = 'sqlite:///merged_data_w_coord.sqlite'

df = get_donations_df(db_path)
df2 = get_donationsTS_df(db_path, 'Carnegie Mellon University')
df3 = get_donationsMAP_df(db_path, 'Carnegie Mellon University')

fig = px.bar(
    df,
    x="Amount",
    y="School",
    orientation='h',
)
fig.update_yaxes(title_text='')
fig.update_xaxes(tickprefix='$')

fig2 = px.scatter(
    df2,
    x='Date',
    y='Amount',
    custom_data=['Donor Country', 'Donor'],
    color_discrete_sequence=px.colors.qualitative.Alphabet,
    color='Donor Country'
)
fig2.update_xaxes(title_text='')
fig2.update_yaxes(
    title_text='',
    tickprefix="$"
)
fig2.update_traces(
    hovertemplate=("Date: %{x|%Y-%m-%d}<br>"
                   "Amount: %{y:$,}<br>"
                   "Donor Country: %{customdata[0]}<br>"
                   "Donor: %{customdata[1]}")
)

# px.set_mapbox_access_token(open(".mapbox_token").read())
fig3 = px.scatter_mapbox(
    df3,
    lat="Latitude",
    lon="Longitude",
    color="Score",
    size="Amount",
    custom_data=['Amount', 'Score', 'Date', 'Donor Country'],
    color_continuous_scale=px.colors.sequential.Bluered[::-1],
    opacity=0.5,
    size_max=15,
    zoom=0,
)
fig3.update_layout(mapbox_style="open-street-map")
fig3.update_traces(
    hovertemplate=("Donor Country: %{customdata[3]}<br>"
                   "Date: %{customdata[2]|%Y-%m-%d}<br>"
                   "Amount: %{customdata[0]:$,}<br>"
                   "Democracy Score: %{customdata[1]}")
)

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
