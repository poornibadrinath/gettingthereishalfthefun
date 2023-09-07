import json
from geopy.distance import geodesic
import csv

# Load GeoJSON data from the file for metro stops
with open('dataanalysis/commuteamstrain.geojson') as f:
    data = json.load(f)

# Separate the features into two categories (A and B) for metro stops
categoryA = []
categoryB = []

for feature in data['features']:
    if feature['properties']['Category'] == 'A':
        categoryA.append(feature)
    elif feature['properties']['Category'] == 'B':
        categoryB.append(feature)

# Calculate the distance ranges
distance_ranges = {
    '<500m': (0, 500),
    '500-1000m': (500, 1000),
    '>1000m': (1000, float('inf'))
}

# Count the number of metro stops within each distance range
within_distance_range_count = {key: 0 for key in distance_ranges}

for pointA in categoryA:
    coordsA = pointA['geometry']['coordinates']

    for pointB in categoryB:
        coordsB = pointB['geometry']['coordinates']
        distance = geodesic((coordsA[1], coordsA[0]), (coordsB[1], coordsB[0])).meters

        for range_name, (min_range, max_range) in distance_ranges.items():
            if min_range <= distance <= max_range:
                within_distance_range_count[range_name] += 1

# Calculate the total number of metro stops in category A
total_metro_stops = len(categoryA)

# Calculate the percentage for each distance range
percentage_within_ranges = {
    range_name: (count / total_metro_stops) * 100
    for range_name, count in within_distance_range_count.items()
}

# Calculate the sum of percentages within defined ranges
sum_of_percentages = sum(percentage_within_ranges.values())

# Adjust the 'more than 1000m' range percentage to make the total 100%
percentage_within_ranges['>1000m'] = 100 - sum_of_percentages

# Write the percentage values to a CSV file
with open('busstopsams1.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Distance Range', 'Percentage'])
    
    for range_name, percentage in percentage_within_ranges.items():
        csv_writer.writerow([range_name, percentage])
