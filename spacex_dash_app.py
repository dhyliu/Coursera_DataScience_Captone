# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Extrac unique launch site names
unique_launch_sites = spacex_df['Launch Site'].unique().tolist()
launch_sites = []
launch_sites.append({'label': 'ALL SITES', 'value': 'ALL'})
for launch_site in unique_launch_sites:
    launch_sites.append({'label': launch_site, 'value': launch_site})


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                            options=launch_sites,
                                            value='ALL',
                                            placeholder="Select a Launch Site here", 
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,max=10000,step=1000,
                                                value=[min_payload,max_payload],
                                                marks={0: '0', 2500:'2500',5000:'5000',
                                                7500:'7500', 10000: '10000'}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))

def show_pie(site):
    if site == 'ALL':
        # select all sites
        fig_pie= px.pie(data_frame = spacex_df, names='Launch Site', values='class' ,title='Total Launches for All SITES')
        return fig_pie
    else:
        # select a specific site
        specific_df=spacex_df.loc[spacex_df['Launch Site'] == site]
        fig_pie = px.pie(data_frame = specific_df, names='class',title='Total Launch for a Specific Site: '+site)
        return fig_pie

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')])

def show_scatter(site, payload_slider):
    if site == 'ALL':
        inrange_df = spacex_df[(spacex_df['Payload Mass (kg)']>=payload_slider[0])
        &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        fig_scatter = px.scatter(data_frame=inrange_df, x="Payload Mass (kg)", y="class",
        title='Total Payload vs. Success for ALL SITES',
        color="Booster Version Category")
        return fig_scatter
    else:
        specific_df=spacex_df.loc[spacex_df['Launch Site'] == site]
        inrange_df = specific_df[(specific_df['Payload Mass (kg)']>=payload_slider[0])
        &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        fig_scatter = px.scatter(data_frame=inrange_df, x="Payload Mass (kg)", y="class", 
        title='Payload vs. Success for a Specific Site: '+site,
        color="Booster Version Category")
        return fig_scatter

# Run the app
if __name__ == '__main__':
    app.run_server()
