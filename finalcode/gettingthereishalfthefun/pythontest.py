import matplotlib.pyplot as plt
import numpy as np

# Generate random data for demonstration purposes
np.random.seed(42)
num_points = 50
x_coords = np.random.uniform(0, 100, num_points)  # X-coordinates in the space
y_coords = np.random.uniform(0, 100, num_points)  # Y-coordinates in the space
driving_times = np.random.uniform(10, 60, num_points)  # Time taken in minutes for driving
public_transport_times = np.random.uniform(15, 90, num_points)  # Time taken in minutes for public transport

# Create the space-time cube visualization
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Plot the dots for driving time
ax.scatter(x_coords, y_coords, driving_times, c='b', marker='o', label='Driving Time')

# Plot the dots for public transport time
ax.scatter(x_coords, y_coords, public_transport_times, c='r', marker='^', label='Public Transport Time')

# Set axis labels
ax.set_xlabel('X-coordinate')
ax.set_ylabel('Y-coordinate')
ax.set_zlabel('Time (minutes)')

# Set plot title and legend
plt.title('Space-Time Cube: Driving Time vs. Public Transport Time')
ax.legend()

# Show the plot
plt.show()
