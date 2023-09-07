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

# Define the map image as a 3D surface at the bottom of the cube
fig.add_trace(go.Surface(
    z=[[0, 0], [0, 0]],  # Z values to create a flat surface at the bottom
    colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,0,0,0)']],  # Transparent color scale
    showscale=False,  # Hide color scale
    hoverinfo='none',  # Disable hover info
))

# Define color ranges and line width ranges for driving time
color_ranges = [(0, 'green'), (30, 'yellow'), (60, 'red'), (90, 'maroon')]
width_ranges = [(0, 3), (30, 5), (60, 7), (90, 9)]

# ... (Rest of your code for plotting lines and points)

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

# Set cube opacity to 30%
fig.update_traces(opacity=0.3)

# Show the interactive plot
fig.show()
