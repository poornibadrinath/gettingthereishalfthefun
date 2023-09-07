
import plotly.graph_objects as go
import dash
from dash import dcc, html
import csv
from PIL import Image
import numpy as np

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

# Read the image you want to use as the texture
im = np.asarray(Image.open("spacetimecuberoutes/bengaluru_map.jpg"))  # reading image as a numpy array
im_x, im_y, im_layers = im.shape                                

# Create a meshgrid of x and y values spanning the image dimensions
x, y = np.meshgrid(np.linspace(0, im_x - 1, im_x), np.linspace(0, im_y - 1, im_y))

# Create a surface mesh from the image
surface = go.Surface(
    x=x,
    y=y,
    z=np.zeros(im.shape[:2]),
    surfacecolor=im,
    showscale=False,
    colorscale='Viridis',
    opacity=0.7,
)

# Create a scatter trace for route lines and origin-destination points
traces = []
for i in range(len(data)):
    x_vals = [origin_lat_long[i][1], destination_lat_long[i][1]]
    y_vals = [origin_lat_long[i][0], destination_lat_long[i][0]]
    z_vals = [driving_times[i]] * 2
    time_color = '#8B0000' if z_vals[0] > 90 else 'green' if z_vals[0] <= 30 else '#FFD700' if z_vals[
                                                                                                      0] <= 60 else 'red'
    line_width = 2 + z_vals[0] / 30

    traces.append({
        'type': 'scatter3d',
        'x': x_vals,
        'y': y_vals,
        'z': z_vals,
        'mode': 'lines',
        'line': {'color': time_color, 'width': line_width},
        'hoverinfo': 'text',
        'text': 'Route: {}<br>Distance: {} km<br>Time: {} mins'.format(route_names[i], distances[i], z_vals[0])
    })

    traces.append({
        'type': 'scatter3d',
        'x': [origin_lat_long[i][1], destination_lat_long[i][1]],
        'y': [origin_lat_long[i][0], destination_lat_long[i][0]],
        'z': z_vals,
        'mode': 'markers',
        'marker': {'size': 5, 'color': ['#00B295', '#23395B']},
        'name': 'Origin-Destination Points'
    })

# Set the layout
app.layout = html.Div([
    dcc.Graph(
        id='space-time-cube',
        figure={
            'data': traces + [surface],
            'layout': {
                'title': 'Space-Time Cube',
                'scene': {
                    'xaxis_title': 'Longitude',
                    'yaxis_title': 'Latitude',
                    'zaxis_title': 'Time (mins)',
                    'zaxis': {'tickvals': list(range(0, 200, 25)), 'ticktext': [str(i) for i in range(0, 200, 25)]},
                    'xaxis': {'range': [0, im_x], 'showticklabels': False},
                    'yaxis': {'range': [0, im_y], 'showticklabels': False},
                    'camera_eye': {'x': -1.5, 'y': -2.5, 'z': 1},
                    'bgcolor': 'rgb(240, 240, 240)',
                }
            }
        },
        style={'width': '100%', 'height': '100vh'}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
