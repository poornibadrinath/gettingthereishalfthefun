import pandas as pd
import plotly.graph_objects as go

# Read the CSV file
df = pd.read_csv('nearest_metro_tram_distances1.csv')

# Define the distance ranges
distance_ranges = [
    ("<100m", 0, 100),
    ("100-500m", 100, 500),
    (">500m", 500, float('inf'))
]

# Create a new DataFrame to store aggregated data
aggregated_data = pd.DataFrame(columns=['Range', 'Percentage'])

# Calculate the total number of bus stops
total_bus_stops = len(df)

# Calculate the percentage of bus stops within each range
for range_name, min_range, max_range in distance_ranges:
    within_range = df[(df['Distance (meters)'] >= min_range) & (df['Distance (meters)'] <= max_range)]
    percentage = (len(within_range) / total_bus_stops) * 100
    aggregated_data.loc[len(aggregated_data)] = [range_name, percentage]

# Create a line graph using Plotly
fig = go.Figure()

fig.add_trace(go.Scatter(x=aggregated_data['Range'], y=aggregated_data['Percentage'], mode='lines', 
                         line_shape='spline', name='Percentage', fill='tozeroy',
                         line=dict(color='#2C5530', width=3)))

fig.update_layout(
    title='<b>Bengaluru Connecitivity of different modes of transport: buses:train/tram/ferry</b>',
    xaxis_title='Distance Range',
    yaxis_title='Percentage (%)',
    showlegend=True,
    width=1920,  # Set the width to fit the screen (adjust as needed)
    height=600,  # Set the height of the plot
)

fig.show()
