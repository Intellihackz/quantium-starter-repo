import pandas
from dash import Dash, html, dcc

from plotly.express import line

# the path to the formatted data file
DATA_PATH = "./processeddata.csv"

# load in data
data = pandas.read_csv(DATA_PATH)
data = data.sort_values(by="Date")

# initialize dash
dash_app = Dash(__name__)

# create the visualization
line_chart = line(data, x="Date", y="Sales", title="Pink Morsel Sales")
visualization = dcc.Graph(
    id="visualization",
    figure=line_chart
)

# create the header
header = html.H1(
    "Pink Morsel Visualizer",
    id="header"
)

# define the app layout
dash_app.layout = html.Div(
    [
        header,
        visualization
    ]
)

# this is only true if the module is executed as the program entrypoint
if __name__ == '__main__':
    dash_app.run_server()