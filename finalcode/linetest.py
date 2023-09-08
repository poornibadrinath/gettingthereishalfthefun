import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import pandas as pd

# Read data from the CSV files
bus_data = pd.read_csv('finalcalculations/amsbusstops.csv')
metro_data = pd.read_csv('finalcalculations/busstopsams1.csv')

# Create a Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Amsterdam Public Transport Proximity Range'),

    # Line Graph
    html.Div([
        dcc.Graph(figure={
            'data': [
                go.Scatter(x=bus_data['Distance Range'], y=bus_data['Percentage'], mode='lines', fill='tozeroy', name='Bus Stops', line=dict(color='#305252'), line_shape='spline'),
                go.Scatter(x=metro_data['Distance Range'], y=metro_data['Percentage'], mode='lines', fill='tozeroy', name='Train Stops', line=dict(color='#488286'), line_shape='spline'),
            ],
            'layout': go.Layout(title='Amsterdam Public Transport Proximity Range', xaxis_title='Distance Range', yaxis_title='Percentage (%)')
        }),
    ], className='graph-container'),
])

if __name__ == '__main__':
    app.run_server(debug=True)
