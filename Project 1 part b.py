import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants
epsilon_0 = 8.85e-12  # Permittivity of free space in C^2 / (N·m^2)
sigma = 1e-6  # Volume charge density in C/m^3 (1 μC/m^3)
R = 0.05  # Initial Radius of the sphere in meters (5 cm)
Q = sigma * (4 / 3) * np.pi * R ** 3  # Initial Charge of the sphere


# Define the electric field function
def electric_field_sphere(x, y, R, Q):
    r = np.sqrt(x ** 2 + y ** 2)
    E_inside = (1 / (4 * np.pi * epsilon_0)) * (Q * r / R ** 3)
    E_outside = (1 / (4 * np.pi * epsilon_0)) * (Q / r ** 2)
    return np.where(r < R, E_inside, E_outside)  # Field inside and outside sphere


# Create a grid
x = np.linspace(-0.1, 0.1, 200)
y = np.linspace(-0.1, 0.1, 200)
X, Y = np.meshgrid(x, y)

# Initial tracked point (inside the sphere)
tracked_point = np.array([0.02, 0.02])  # Starting point inside the sphere

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-0.1, 0.1)
ax.set_ylim(-0.1, 0.1)

# Initialize a circle and moving point
circle = plt.Circle((0, 0), R, fill=False, edgecolor='b')
point, = ax.plot([tracked_point[0]], [tracked_point[1]], 'ko', markersize=8)  # black point
ax.add_patch(circle)

# Initial colormap
E_values = electric_field_sphere(X, Y, R, Q)
cmap = ax.contourf(X, Y, E_values, levels=500, cmap='inferno')
plt.colorbar(cmap, ax=ax, label='Electric Field Strength (N/C)')

# Legend for energy value
energy_text = ax.text(0.01, 0.08, '', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
contour_plots = []


# Function to update the animation
def update(frame):
    global R, Q, contour_plots

    # Update radius
    R = 0.05 + 0.02 * np.sin(frame * 0.1)
    Q = sigma * (4 / 3) * np.pi * R ** 3  # Update charge

    # Update circle radius
    circle.set_radius(R)

    # Remove old contour plots
    for c in contour_plots:
        c.remove()

    # Update colormap
    E_values = electric_field_sphere(X, Y, R, Q)
    contour = ax.contourf(X, Y, E_values, levels=500, cmap='inferno')
    contour_plots[:] = contour.collections  # Update stored contours

    # Calculate electric field at tracked point
    r_point = np.sqrt(tracked_point[0] ** 2 + tracked_point[1] ** 2)
    E_point = electric_field_sphere(tracked_point[0], tracked_point[1], R, Q)

    # Update legend text
    energy_text.set_text(f'E @ ({tracked_point[0]:.2f}, {tracked_point[1]:.2f}) = {E_point:.2e} N/C')

    return circle, point, energy_text


# Function to update the tracked point on click
def on_click(event):
    global tracked_point
    if event.inaxes is not None:
        r = np.sqrt(event.xdata ** 2 + event.ydata ** 2)
        if r < 0.1:  # Ensure point is within the grid limits
            tracked_point = np.array([event.xdata, event.ydata])
            point.set_data([tracked_point[0]], [tracked_point[1]])


fig.canvas.mpl_connect('button_press_event', on_click)

# Create animation
ani = animation.FuncAnimation(fig, update, frames=100, interval=50, blit=False)
plt.show()