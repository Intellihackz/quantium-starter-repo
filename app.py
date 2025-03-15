import pandas
from dash import Dash, html, dcc, Input, Output

from plotly.express import line

# the path to the formatted data file
DATA_PATH = "./processeddata.csv"

# load in data
data = pandas.read_csv(DATA_PATH)
data = data.sort_values(by="Date")

# initialize dash with external stylesheets
dash_app = Dash(__name__)

# Define styles
COLORS = {
    'background': '#f8f9fa',
    'text': '#2c3e50',
    'accent': '#e74c3c'
}

STYLES = {
    'container': {
        'max-width': '1200px',
        'margin': '0 auto',
        'padding': '2rem',
        'background-color': COLORS['background'],
        'font-family': 'Arial, sans-serif'
    },
    'header': {
        'color': COLORS['text'],
        'text-align': 'center',
        'margin-bottom': '2rem',
        'font-size': '2.5rem'
    },
    'radio': {
        'margin': '1rem 0',
        'padding': '1rem',
        'border-radius': '8px',
        'background-color': 'white',
        'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'
    }
}

# create the header
header = html.H1(
    "Pink Morsel Sales Dashboard",
    id="header",
    style=STYLES['header']
)

# create the region selector
region_selector = dcc.RadioItems(
    id='region-filter',
    options=[
        {'label': ' All Regions', 'value': 'all'},
        {'label': ' North', 'value': 'north'},
        {'label': ' South', 'value': 'south'},
        {'label': ' East', 'value': 'east'},
        {'label': ' West', 'value': 'west'}
    ],
    value='all',
    style=STYLES['radio']
)

# create the visualization container
visualization = dcc.Graph(
    id="visualization"
)

# define the app layout
dash_app.layout = html.Div(
    [
        header,
        region_selector,
        visualization
    ],
    style=STYLES['container']
)

# callback to update the graph based on region selection
@dash_app.callback(
    Output('visualization', 'figure'),
    Input('region-filter', 'value')
)
def update_graph(selected_region):
    if selected_region == 'all':
        filtered_data = data
        title = "Pink Morsel Sales - All Regions"
    else:
        filtered_data = data[data['Region'] == selected_region]
        title = f"Pink Morsel Sales - {selected_region.capitalize()} Region"
    
    return line(
        filtered_data, 
        x="Date", 
        y="Sales",
        title=title,
        template="plotly_white"
    )

# this is only true if the module is executed as the program entrypoint
if __name__ == '__main__':
    dash_app.run_server(debug=True)