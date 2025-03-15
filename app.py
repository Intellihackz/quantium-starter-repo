# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# Load the processed data
df = pd.read_csv('processeddata.csv')

# Convert the 'Sales' column from string to numeric by removing '$' and converting to float
df['Sales'] = df['Sales'].str.replace('$', '').astype(float)

# Convert 'Date' to datetime for proper sorting
df['Date'] = pd.to_datetime(df['Date'])

# Sort by date
df = df.sort_values('Date')

# Create the line chart
fig = px.line(
    df, 
    x='Date', 
    y='Sales', 
    color='Region',
    title='Pink Morsel Sales Over Time',
    markers=True,
    labels={
        'Date': 'Date',
        'Sales': 'Sales Amount ($)',
        'Region': 'Region'
    }
)

app.layout = html.Div(children=[
    html.H1(children='Soul Foods Sales Analysis Dashboard'),
    
    dcc.Graph(
        id='sales-time-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)
