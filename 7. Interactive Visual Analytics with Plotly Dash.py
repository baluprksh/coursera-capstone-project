# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

#SJH: Import numpy for linspace
from numpy import linspace

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# SJH: Create some variables to be used in the app layout:
# First, create the list of Launch Sites to be used in Options
LaunchsiteDropdownOptions = [{'label': sitename, 'value': sitename} for sitename in set(spacex_df['Launch Site'].values)]
LaunchsiteDropdownOptions.insert(0, {'label': 'All Sites', 'value': 'ALL'})
# Now create marks for the range slider. It takes a dictionary.
slidermarks = linspace(0,10000, num = 5, dtype=int)
slidermarksdict = {str(i) : str(i) for i in slidermarks}

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                dcc.Dropdown(
                                    id = 'site-dropdown',
                                    options = LaunchsiteDropdownOptions,
                                    value = 'ALL',
                                    placeholder = "Select Launch Site",
                                    searchable = True
                                ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min = 0,
                                    max = 10000,
                                    step = 1000, 
                                    marks = slidermarksdict,
                                    value = [min_payload, max_payload]), 

                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df[['Launch Site', 'class']], values = 'class',
        names =  'Launch Site',
        title = 'Total Success Launches By Site')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df[['Launch Site', 'class']],
        names =  'class',
        title = 'Total Success Launches for site ' + entered_site)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value"))
def get_scatter_chart(entered_site, payload_range_selected):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        pass
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site] 
    fig = px.scatter(
        x = filtered_df['Payload Mass (kg)'], 
        y = filtered_df['class'],
        title = 'Correlation between Payload and Success Rate, for Launch Site ' + entered_site,
        color=filtered_df["Booster Version Category"], 
        labels = dict(x = "Payload Mass (kg)", y = "Launch Success"),
        range_x = [payload_range_selected[0], payload_range_selected[1]]
        )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
