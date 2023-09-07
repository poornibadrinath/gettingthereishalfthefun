import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go

# Define the coordinates of Majestic Bus Stand and Vidhan Soudha
majestic_coords = (12.9771, 77.5729)
vidhan_soudha_coords = (12.9794, 77.5912)

# Create a Mapbox token (you need to replace 'YOUR_MAPBOX_TOKEN' with your actual token)
mapbox_token = 'pk.eyJ1IjoicG9vcm5pLWJhZHJpbmF0aCIsImEiOiJjanUwbmYzc3UwdDI3NGRtZ3kzMTltbWZpIn0.SB9PEksVcEwWvZJ9A7J9uA'

# Create a layout for the map
layout = go.Layout(
    mapbox=dict(
        accesstoken=mapbox_token,
        center=dict(lat=12.9784, lon=77.5929),
        zoom=14
    ),
)

# Create a figure with a Mapbox base map
fig = go.Figure(data=go.Scattermapbox(), layout=layout)

# Add the route as a line on the map
fig.add_trace(go.Scattermapbox(
    mode="lines",
    lon=[majestic_coords[1], vidhan_soudha_coords[1]],
    lat=[majestic_coords[0], vidhan_soudha_coords[0]],
    marker={'size': 10},
    line={'width': 3},
))

# Show the map
fig.show()
