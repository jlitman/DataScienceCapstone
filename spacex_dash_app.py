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

def create_launch_site_list():
    launch_sites = spacex_df['Launch Site'].unique()
    site_list = [{'label': 'All Sites', 'value': 'ALL'}] #list of dictionaries
    for site in launch_sites:
        site_list.append({'label':site,'value':site})
    return site_list

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=create_launch_site_list(),#[
                                        #{'label': 'All Sites', 'value': 'ALL'},
                                        #{'label': 'site1', 'value': 'site1'},
                                    #],
                                    value='ALL',
                                    placeholder="Select a Launch Site",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df.groupby(['Launch Site'])['class'].sum().reset_index(),
                     values='class', names='Launch Site', 
                     title='All Successful Launches by Site')
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        
        success_count = filtered_df['class'].sum()
        total = filtered_df['class'].count()
        tmp_df = pd.DataFrame({'count': {'success': success_count,
                               'failure':total-success_count}})

        fig = px.pie(tmp_df,values='count',names=tmp_df.index,
                     title='Successful Launches at {}'.format(entered_site))

    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
