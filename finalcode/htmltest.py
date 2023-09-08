import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import csv
from PIL import Image
import numpy as np
import pyproj

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

# Convert the image projection to WGS84
crs = pyproj.CRS.from_string('EPSG:32643')  # Assumes the image is projected in UTM zone 43N
crs_to = pyproj.CRS.from_string('EPSG:4326')  # WGS84
transformer = pyproj.Transformer.from_crs(crs, crs_to)

# Read the image you want to use as the texture
im = np.asarray(Image.open("spacetimecuberoutes/bengaluru_map.jpg"))  # reading image as a numpy array
im_x, im_y, im_layers = im.shape
x_coords = np.linspace(0, im_x, num=im_x)
y_coords = np.linspace(0, im_y, num=im_y)
lon_coords, lat_coords = transformer.transform(y_coords, x_coords)

# Create a surface mesh from the image
surface = go.Surface(
    x=lat_coords,
    y=lon_coords,
    z=np.zeros((im_x, im_y)),  # pass a 2D array of zeros
    surfacecolor=im,
    showscale=False,
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
        'type': 'scattermapbox',
        'lat': [origin_lat_long[i][0], destination_lat_long[i][0]],
        'lon': [origin_lat_long[i][1], destination_lat_long[i][1]],
        'mode': 'lines',
        'line': {'color': time_color, 'width': line_width},
        'hoverinfo': 'text',
        'text': 'Route: {}<br>Distance: {} km<br>Time: {} mins'.format(route_names[i], distances[i], z_vals[0])
    })

    traces.append({
        'type': 'scattermapbox',
        'lat': [origin_lat_long[i][0], destination_lat_long[i][0]],
        'lon': [origin_lat_long[i][1], destination_lat_long[i][1]],
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
                'mapbox': {
                    'accesstoken': 'pk.eyJ1IjoicG9vcm5pLWJhZHJpbmF0aCIsImEiOiJjanUwbmYzc3UwdDI3NGRtZ3kzMTltbWZpIn0.SB9PEksVcEwWvZJ9A7J9uA',
                    'style': 'mapbox://styles/mapbox/light-v10',
                    'center': {'lat': np.mean(lat_coords), 'lon': np.mean(lon_coords)},
                    'zoom': 10,
                },
                'title': 'Space-Time Cube',
            },
        },
        style={'width': '100%', 'height': '100vh'}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
