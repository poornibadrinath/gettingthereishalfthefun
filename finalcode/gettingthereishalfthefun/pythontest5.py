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

# Create the interactive 3D plot using Plotly
fig = go.Figure()

# Define color ranges and line width ranges for driving time
color_ranges = [(0, 'green'), (30, 'yellow'), (60, 'red'), (90, 'maroon')]
width_ranges = [(0, 3), (30, 5), (60, 7), (90, 9)]

# Plot the lines connecting the origin and destination points
for i in range(len(data)):
    x_vals = [origin_lat_long[i][1], destination_lat_long[i][1]]
    y_vals = [origin_lat_long[i][0], destination_lat_long[i][0]]
    z_vals = [driving_times[i], driving_times[i]]  # Change z values to driving times
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

# Set axis labels and plot title
fig.update_layout(scene=dict(xaxis_title='Longitude', yaxis_title='Latitude', zaxis_title='Time (mins)'), 
                  title='Space-Time Cube: Geographic Coordinates vs. Time')

# Define a meshgrid of coordinates for the surface plot
x_coords = [coord[1] for coord in origin_lat_long]
y_coords = [coord[0] for coord in origin_lat_long]
z_coords = [0] * len(origin_lat_long)  # Z coordinates are set to 0 for the bottom layer

# Create the surface plot for the bottom layer using meshgrid coordinates
fig.add_trace(go.Surface(x=x_coords, y=y_coords, z=z_coords, colorscale='Viridis'))

# Show the interactive plot
fig.show()
