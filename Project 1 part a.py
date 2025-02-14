import numpy as np
import matplotlib.pyplot as plt
# Constants
epsilon_0 = 8.85e-12 # Permittivity of free space in C^2 / (N·m^2)
sigma = 1e-6 # volume charge density in C/m^3 (1 μC/m^3)
R = 0.05 # Radius of the sphere in meters (5 cm)
# Total charge on the sphere
Q = sigma * (4 / 3) * np.pi * R ** 3 # Charge of the sphere
# Electric field calculation function for a charged sphere in 2D
def electric_field_sphere(x, y, sigma, R, epsilon_0):
    r = np.sqrt(x ** 2 + y ** 2) # Radial distance from the center
    # Electric field inside the sphere (r < R)
    if r < R:
        E = (1 / (4 * np.pi * epsilon_0)) * (Q*r / R ** 3)  # Inside the sphere
    else:
    # Electric field outside the sphere (r > R)
        E = (1 / (4 * np.pi * epsilon_0)) * (Q / r ** 2) # Outside the sphere
    return E

# Create a grid of points in the x-y plane
x = np.linspace(-0.1, 0.1, 200) # X coordinates from -10 cm to 10 cm
y = np.linspace(-0.1, 0.1, 200) # Y coordinates from -10 cm to 10 cm
X, Y = np.meshgrid(x, y)
# Vectorize the electric field function and compute the electric field on the grid.
E_values = np.vectorize(electric_field_sphere)(X, Y, sigma, R, epsilon_0)
# Now, E_values contains the electric field at each (X, Y) point in the grid
# Plotting the electric field as a color map
plt.figure(figsize=(8, 6))
plt.contourf(X, Y, E_values, levels=50, cmap='inferno') # Color map for electric field

# Adding labels and title
plt.colorbar(label='Electric Field Strength (N/C)') # Color bar to show the field strength
plt.xlabel("x (meters)")
plt.ylabel("y (meters)")
plt.title("Electric Field of a Charged Sphere (2D Map)")
plt.grid(True)
# Show the plot
plt.show()