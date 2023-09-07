import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import numpy as np

# Load the map image
map_image = Image.open('bengaluru_map.png')

# Sample data for latitude, longitude, and elevation
latitudes = [37.7749, 34.0522, 40.7128, 41.8781]
longitudes = [-122.4194, -118.2437, -74.0060, -87.6298]
elevations = [0, 100, 200, 50]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set limits for the plot
ax.set_xlim(-180, 180)
ax.set_ylim(-90, 90)
ax.set_zlim(0, 200)

# Display the map image as a background
ax.imshow(np.array(map_image), extent=[-180, 180, -90, 90], alpha=0.5, aspect='auto', zorder=-1)

# Create scatter plot for cube points
ax.scatter(longitudes, latitudes, elevations, c='r', marker='o')

# Set labels for each point
for i, txt in enumerate(['San Francisco', 'Los Angeles', 'New York', 'Chicago']):
    ax.text(longitudes[i], latitudes[i], elevations[i], txt)

# Draw a cube using polygons
cube_vertices = np.array([
    [-120, 30, 0],
    [-120, 40, 0],
    [-110, 40, 0],
    [-110, 30, 0],
    [-120, 30, 100],
    [-120, 40, 100],
    [-110, 40, 100],
    [-110, 30, 100]
])

cube_faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]]

for face in cube_faces:
    ax.add_collection3d(plt.Polygon(cube_vertices[face]))

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Elevation')

plt.show()
