import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import csv

# Read data from the CSV file
data = []
with open("spacetimecuberoutes/amsnonpeakhour.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)

# Function to split latitude and longitude values from a string in "lat, long" format
def split_lat_long(lat_long_str):
    lat, long = map(float, lat_long_str.split(','))
    return lat, long

# Create lists to store data for Plotly
origin_lat_long = []
destination_lat_long = []
distances = []
driving_times = []
public_transport_times = []
transport_modes = []
route_names = []  # New list to store route names

# Extract data from the CSV and split into separate lists for Plotly
for row in data:
    o_lat, o_long = split_lat_long(row['origin_latitude'] + ',' + row['origin_longitude'])
    origin_lat_long.append((o_lat, o_long))
    
    d_lat, d_long = split_lat_long(row['destination_latitude'] + ',' + row['destination_longitude'])
    destination_lat_long.append((d_lat, d_long))
    
    distances.append(float(row['distance']))  # Assuming the CSV contains a 'distance' column
    driving_times.append(float(row['driving_time']))  # Assuming the CSV contains a 'driving_time' column
    public_transport_times.append(float(row['public_transport']))  # Assuming the CSV contains a 'public_transport' column
    transport_modes.append(int(row['transport_modes']))  # Assuming the CSV contains a 'transport_modes' column
    route_names.append(row['route_name'])  # Assuming the CSV contains a 'route_name' column

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='space-time-cube', style={'width': '100%', 'height': '100vh'}),  # Adjust width and height
    html.Div([
        dcc.Checklist(id='toggle-cube', options=[{'label': 'Driving Time', 'value': 'driving'},
                                                 {'label': 'Public Transport Time', 'value': 'transport'}],
                      value=['driving', 'transport'])
    ], style={'text-align': 'center', 'margin-top': '10px'})
])

@app.callback(Output('space-time-cube', 'figure'),
              Input('toggle-cube', 'value'))
def update_cube(selected_values):
    traces = []

    for i in range(len(data)):
        x_vals = [origin_lat_long[i][1], destination_lat_long[i][1]]
        y_vals = [origin_lat_long[i][0], destination_lat_long[i][0]]
        z_vals = [driving_times[i] if 'driving' in selected_values else public_transport_times[i]] * 2
        time_color = '#8B0000' if z_vals[0] > 90 else 'green' if z_vals[0] <= 30 else '#FFD700' if z_vals[0] <= 60 else 'red'
        line_width = 2 + z_vals[0] / 30  # Adjust the width based on time

        # Add lines for routes
        traces.append(go.Scatter3d(x=x_vals, y=y_vals, z=z_vals,
                                   mode='lines',
                                   line=dict(color=time_color, width=line_width),
                                   name='',
                                   hoverinfo='text',
                                   text='Route: {}<br>Distance: {} km<br>Time: {} mins'.format(route_names[i], distances[i], z_vals[0])))

        # Add origin and destination points as scatter traces with matching z-coordinates
        traces.append(go.Scatter3d(x=[origin_lat_long[i][1], destination_lat_long[i][1]],
                                   y=[origin_lat_long[i][0], destination_lat_long[i][0]],
                                   z=z_vals,
                                   mode='markers',
                                   marker=dict(size=5,
                                               color=['#00B295', '#23395B']),  # Custom colors for origin and destination
                                   name='Origin-Destination Points'))

    figure = {
    'data': traces,
    'layout': go.Layout(scene=dict(xaxis_title='Longitude', yaxis_title='Latitude', zaxis_title='Time (mins)',
                                    zaxis=dict(tickvals=list(range(0, 200, 25)), ticktext=[str(i) for i in range(0, 200, 25)])),
                         title='Space-Time Cube',
                         showlegend=False,  # Show legend
                         legend=dict(
                             title='Time (mins)',  # Set legend title
                             itemsizing='constant',  # Set item sizing for color values
                             x=1,  # Adjust x position of the legend
                             y=1,  # Adjust y position of the legend
                             bgcolor='rgba(255, 255, 255, 0.5)',  # Set legend background color
                             bordercolor='rgba(0, 0, 0, 0.5)',  # Set legend border color
                             borderwidth=1,  # Set legend border width
                             font=dict(size=10, color='black'),  # Set legend font properties
                         ))
}
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)