import json
from geopy.distance import geodesic
import csv

# Load the bus stops data from JSON
with open('dataanalysis/commuteblrbusstops.geojson') as f:
    bus_stops_data = json.load(f)

# Load the metro and tram stops data from JSON
with open('dataanalysis/commuteblrmetro.geojson') as f:
    metro_tram_stops_data = json.load(f)

# Extract coordinates for bus stops and metro/tram stops
bus_stops = [(feature['geometry']['coordinates'][1], feature['geometry']['coordinates'][0]) for feature in bus_stops_data['features']]
metro_tram_stops = [(feature['geometry']['coordinates'][1], feature['geometry']['coordinates'][0]) for feature in metro_tram_stops_data['features']]

# Calculate distances between each bus stop and its nearest metro/tram stop
distances = {}

for bus_coords in bus_stops:
    bus_name = f"Bus Stop ({bus_coords[0]}, {bus_coords[1]})"
    nearest_distance = float('inf')
    nearest_metro_tram_stop = None

    for metro_tram_coords in metro_tram_stops:
        distance = geodesic(bus_coords, metro_tram_coords).meters
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_metro_tram_stop = f"Metro/Tram Stop ({metro_tram_coords[0]}, {metro_tram_coords[1]})"

    distances[bus_name] = nearest_distance

# Save distances to a CSV file
with open('nearest_metro_tram_distances1.csv', 'w', newline='') as csvfile:
    fieldnames = ['Bus Stop', 'Nearest Metro/Tram Stop', 'Distance (meters)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for bus_stop, distance in distances.items():
        nearest_metro_tram_stop = f"Metro/Tram Stop ({metro_tram_coords[0]}, {metro_tram_coords[1]})"
        writer.writerow({'Bus Stop': bus_stop, 'Nearest Metro/Tram Stop': nearest_metro_tram_stop, 'Distance (meters)': distance})
