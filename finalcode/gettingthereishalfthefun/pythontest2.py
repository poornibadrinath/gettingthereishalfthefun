import plotly.graph_objects as go
import csv

# Read data from the CSV file
data = []
with open("bengalurupeakhr.csv", "r") as csvfile:
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
route_names = []  # New list to store route names


# Extract data from the CSV and split into separate lists for Plotly
for row in data:
    o_lat, o_long = split_lat_long(row['origin_latitude'] + ',' + row['origin_longitude'])
    origin_lat_long.append((o_lat, o_long))
    
    d_lat, d_long = split_lat_long(row['destination_latitude'] + ',' + row['destination_longitude'])
    destination_lat_long.append((d_lat, d_long))
    
    distances.append(float(row['distance']))  # Assuming the CSV contains a 'distance' column
    driving_times.append(float(row['driving_time']))  # Assuming the CSV contains a 'driving_time' column
    route_names.append(row['route_name'])  # Assuming the CSV contains a 'route_name' column


# Set up the map image URL
map_image_url = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/77.5946,12.9716,10,0,0/800x800?access_token=pk.eyJ1IjoicG9vcm5pLWJhZHJpbmF0aCIsImEiOiJjanUwbmYzc3UwdDI3NGRtZ3kzMTltbWZpIn0.SB9PEksVcEwWvZJ9A7J9uA"

# Create the interactive 3D plot using Plotly
fig = go.Figure()

# Define color ranges and line width ranges for driving time
color_ranges = [(0, 'green'), (30, 'yellow'), (60, 'red'), (90, 'maroon')]
width_ranges = [(0, 3), (30, 5), (60, 7), (90, 9)]

# Create dictionaries to store the legend entries for color and width
color_legend = {}
width_legend = {}

# Plot the lines connecting the origin and destination points
for i in range(len(data)):
    x_vals = [distances[i], distances[i]]
    y_vals = [origin_lat_long[i][1], destination_lat_long[i][1]]
    z_vals = [origin_lat_long[i][0], destination_lat_long[i][0]]
    driving_time = driving_times[i]
    route_name = route_names[i]

    # Determine the color and line width based on driving time
    line_color = 'green'  # Default color for driving times below 30 minutes
    line_width = 1  # Default line width for driving times below 30 minutes

    for limit, color in color_ranges:
        if driving_time > limit:
            line_color = color

    for limit, width in width_ranges:
        if driving_time > limit:
            line_width = width

    # Plot the distance as a line with the determined color and line width
    fig.add_trace(go.Scatter3d(x=x_vals, y=y_vals, z=z_vals,
                               mode='lines',
                               line=dict(color=line_color, width=line_width),
                               name='',  # Empty name to avoid showing driving time in the legend
                               showlegend=False,  # Hide driving time entries in the legend
                               hoverinfo='text',  # Show custom hover text
                               text='Route: {}<br>Distance: {} km<br>Driving Time: {} mins'.format(route_name, distances[i], driving_time)))

    # Update color_legend and width_legend dictionaries for grouping in the legend
    color_legend[line_color] = "Driving Time: {} mins".format(driving_time)
    width_legend[line_width] = "Line Width: {}".format(line_width)

# Plot the origin points with red circles
fig.add_trace(go.Scatter3d(x=distances, y=[coord[1] for coord in origin_lat_long], 
                           z=[coord[0] for coord in origin_lat_long], 
                           mode='markers',
                           marker=dict(symbol='circle', size=8, color='red'),
                           name='Origin'))

# Plot the destination points with green circles
fig.add_trace(go.Scatter3d(x=distances, y=[coord[1] for coord in destination_lat_long], 
                           z=[coord[0] for coord in destination_lat_long], 
                           mode='markers',
                           marker=dict(symbol='circle', size=8, color='green'),
                           name='Destination'))

# Add legend groups for color and width
for color, legend_entry in color_legend.items():
    fig.add_trace(go.Scatter3d(x=[None], y=[None], z=[None],
                               mode='markers',
                               marker=dict(color=color),
                               name=legend_entry,
                               legendgroup=legend_entry))

for width, legend_entry in width_legend.items():
    fig.add_trace(go.Scatter3d(x=[None], y=[None], z=[None],
                               mode='lines',
                               line=dict(width=width, color='black'),
                               name=legend_entry,
                               legendgroup=legend_entry))

# Add the map image as a plane at the base of the cube
fig.add_trace(go.Image(
    source=map_image_url,
    x=[-cubeSize / 2, cubeSize / 2, cubeSize / 2, -cubeSize / 2],
    y=[-cubeSize / 2, -cubeSize / 2, cubeSize / 2, cubeSize / 2],
    z=[-cubeSize / 2, -cubeSize / 2, -cubeSize / 2, -cubeSize / 2],
    colorscale='gray',
    opacity=0.8,
))

# Set axis labels and plot title
fig.update_layout(scene=dict(xaxis_title='Distance', yaxis_title='Longitude', zaxis_title='Latitude'), 
                  title='Space-Time Cube: Distance vs. Geographic Coordinates')

# Replace these values with the actual latitude and longitude ranges for Bangalore
latitude_range = (12.8, 13.2)
longitude_range = (77.5, 77.9)

# Calculate the ratio of longitude range to latitude range
longitude_ratio = (longitude_range[1] - longitude_range[0]) / (latitude_range[1] - latitude_range[0])

# Set the camera position and aspect ratio to make the plot appear bigger and spread out
fig.update_layout(scene_camera=dict(eye=dict(x=1.5, y=-2.2, z=2.0)),  # Adjust z value for larger cube
                  scene_aspectmode='manual', scene_aspectratio=dict(x=1, y=longitude_ratio, z=0.6))

# Show the interactive plot
fig.show()
