
import json
import plotly.graph_objects as go
import pandas as pd
import math

# Load GeoJSON data from the file
with open('dataanalysis/commuteamsbus.geojson') as f:
    data = json.load(f)

# Separate the features into two categories (A and B)
categoryA = []
categoryB = []

for feature in data['features']:
    if feature['properties']['Category'] == 'A':
        categoryA.append(feature)
    elif feature['properties']['Category'] == 'B':
        categoryB.append(feature)

# Define the coordinates of the center point
center_coords = (52.39, 4.89)  # Amsterdam center coordinates

# Create the scatter plot figure
fig = go.Figure()

# Calculate the distance for each point in category A to all points in category B
scatter_lat = []
scatter_lon = []
scatter_size = []
scatter_color = []
scatter_text = []
scatter_names = []

for pointA in categoryA:
    coordsA = pointA['geometry']['coordinates']
    min_distance = float('inf')  # Initialize with a very large value

    for pointB in categoryB:
        coordsB = pointB['geometry']['coordinates']
        distance = math.sqrt((coordsA[1] - coordsB[1])**2 + (coordsA[0] - coordsB[0])**2)
        min_distance = min(min_distance, distance)

    scatter_lat.append(coordsA[1])  # Latitude of point A
    scatter_lon.append(coordsA[0])  # Longitude of point A
    scatter_size.append(15 + min_distance * 0.005)  # Adjust the scaling for size
    scatter_color.append(min_distance)  # Set color based on distance
    scatter_text.append(f"Nearest distance: {min_distance:.2f} m")
    scatter_names.append(pointA['properties']['Name'])

# Add points of category B to the figure
for pointB in categoryB:
    coordsB = pointB['geometry']['coordinates']
    scatter_lat.append(coordsB[1])
    scatter_lon.append(coordsB[0])
    scatter_size.append(6)  # Constant size for category B points
    scatter_color.append(float('inf'))  # Set a placeholder for category B points
    scatter_text.append(f"Public Transport: {pointB['properties']['Name']}")
    scatter_names.append(f"Public Transport: {pointB['properties']['Name']}")

# Define the custom color scale
color_scale = 'Greens_r'

# Filter out placeholder values ('inf') from scatter_color list
filtered_scatter_color = [color for color in scatter_color if color != float('inf')]

# Create the scatter plot trace for category A
scatter_trace_A = go.Scattermapbox(
    lat=scatter_lat[:len(categoryA)],
    lon=scatter_lon[:len(categoryA)],
    mode='markers',
    marker=dict(
        size=scatter_size[:len(categoryA)],
        color=filtered_scatter_color[:len(categoryA)],
        colorscale=color_scale,
        opacity=1,
        showscale=True,
        cmin=min(filtered_scatter_color),
        cmax=max(filtered_scatter_color),
        colorbar=dict(title='Distance (m)'),
    ),
    text=scatter_text[:len(categoryA)],
    hoverinfo='text',
    customdata=scatter_names[:len(categoryA)],
    name='Points of Interest'
)

# Create the scatter plot trace for category B
scatter_trace_B = go.Scattermapbox(
    lat=scatter_lat[len(categoryA):],
    lon=scatter_lon[len(categoryA):],
    mode='markers',
    marker=dict(
        size=6,
        color='black',  # Set color for category B points
        opacity=1,
    ),
    text=scatter_text[len(categoryA):],
    hoverinfo='text',
    customdata=scatter_names[len(categoryA):],
    name='Public Transport'
)

# Set the map layout
fig.update_layout(
    mapbox=dict(
        accesstoken='pk.eyJ1IjoicG9vcm5pLWJhZHJpbmF0aCIsImEiOiJjanUwbmYzc3UwdDI3NGRtZ3kzMTltbWZpIn0.SB9PEksVcEwWvZJ9A7J9uA',
        center=dict(lat=center_coords[0], lon=center_coords[1]),
        zoom=11,
        style='mapbox://styles/poorni-badrinath/clkkdd0eq00fd01qy03s15boh'
    ),
    margin=dict(l=1, r=1, t=1, b=1),
    showlegend=True,
    coloraxis_showscale=True,
    legend=dict(x=0.02, y=0.97)
)

# Add both traces to the figure
fig.add_trace(scatter_trace_A)
fig.add_trace(scatter_trace_B)

# Show the map
fig.show()
