import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def descartes_theorem(r1, r2, r3, postitive=False):
    k1, k2, k3 = 1/r1, 1/r2, 1/r3

    if postitive:
        # Positive case (internally tangent)
        k4 = k1 + k2 + k3 + 2 * np.sqrt(k1*k2 + k2*k3 + k3*k1)
    else:
        k4 = k1 + k2 + k3 - 2 * np.sqrt(k1*k2 + k2*k3 + k3*k1)
        # Negative case (externally tangent)

    return 1/k4

def plot_circle(ax, x, y, r, label=None, color='b'):
    circle = Circle((x, y), r, fill=False, color=color)
    if label:
        # align the text outside of the circle to the
        ax.text(x, y, label, fontsize=12, ha='center', va='center')
    ax.add_artist(circle)


def create_coordinates(r1, r2, r3):
    coords = [
        calculate_first_three_circles(r1, r2, r3),
        calculate_fourth_circle(r1, r2, r3),
        calculate_fifth_circle(r1, r2, r3),
        calculate_sixth_circle(r1, r2, r3),
        calculate_seventh_circle(r1, r2, r3),
        calculate_eighth_circle(r1, r2, r3)
    ]
    # Shift all of the coords so that the 5th circle is at the origin (0, 0)
    x5, y5, _ = coords[2][0]
    for i in range(len(coords)):
        for j in range(len(coords[i])):
            coords[i][j][0] -= x5
            coords[i][j][1] -= y5

    return [item for sublist in coords for item in sublist]

def calculate_first_three_circles(r1, r2, r3):
    x1, y1 = 0, 0
    x2 = r1 + r2
    y2 = 0
    a = r1 + r3
    b = r2 + r3
    c = r2 + r3
    x3 = (a**2 + b**2 - c**2) / (2*b)
    y3 = np.sqrt(a**2 - x3**2)
    return [[x1, y1, r1], [x2, y2, r2], [x3, y3, r3]]

def calculate_fourth_circle(r1, r2, r3):
    r4 = descartes_theorem(r1, r2, r3, postitive=True)
    d, e, f = r1 + r4, r2 + r4, r3 + r4
    b = r2 + r3
    x4 = (d**2 + b**2 - e**2) / (2*b)
    y4 = (d**2 - x4**2)**0.5
    return [[x4, y4, r4]]

def calculate_fifth_circle(r1, r2, r3):
    r5 = descartes_theorem(r1, r2, r3)
    g = r1 + r5
    h = r2 + r5
    i = r3 + r5
    b = r2 + r3
    x5 = (g**2 + b**2 - h**2) / (2*b)
    y5 = (g**2 - x5**2)**0.5
    return [[x5, y5, r5]]

def calculate_sixth_circle(r1, r2, r3):
    r5 = descartes_theorem(r1, r2, r3)
    x5, y5, _ = calculate_fifth_circle(r1, r2, r3)[0]
    r6 = descartes_theorem(r3, r2, r5, postitive=True)
    x6 = x5
    h = r2 + r6
    y6 = -(h**2 - x6**2)**0.5
    return [[x6, y6, r6]]

def calculate_seventh_circle(r1, r2, r3):
    r5 = descartes_theorem(r1, r2, r3)
    x3, y3, _ = calculate_first_three_circles(r1, r2, r3)[2]
    x5, y5, _ = calculate_fifth_circle(r1, r2, r3)[0]
    r7 = descartes_theorem(r3, r2, r5, postitive=True)
    xyz = np.sqrt((x5 - x3)**2 + (y5 - y3)**2)
    x_offset = ((r3 + r7)**2 - (r5 + r7)**2 + xyz**2) / (2 * xyz)
    y_offset = -np.sqrt((r3 + r7)**2 - x_offset**2)
    angle = np.arctan2(y5 - y3, x5 - x3)
    x7 = x3 + x_offset * np.cos(angle) - y_offset * np.sin(angle)
    y7 = y3 + x_offset * np.sin(angle) + y_offset * np.cos(angle)
    return [[x7, y7, r7]]

def calculate_eighth_circle(r1, r2, r3):
    r5 = descartes_theorem(r1, r2, r3)
    x2, y2, _ = calculate_first_three_circles(r1, r2, r3)[1]
    x3, y3, _ = calculate_first_three_circles(r1, r2, r3)[2]
    r8 = descartes_theorem(r2, r3, r5, postitive=True)
    d23 = np.sqrt((x3 - x2)**2 + (y3 - y2)**2)
    x_offset = ((r2 + r8)**2 - (r3 + r8)**2 + d23**2) / (2 * d23)
    y_offset = -np.sqrt((r2 + r8)**2 - x_offset**2)
    angle = np.arctan2(y3 - y2, x3 - x2)
    x8 = x2 + x_offset * np.cos(angle) - y_offset * np.sin(angle)
    y8 = y2 + x_offset * np.sin(angle) + y_offset * np.cos(angle)
    return [[x8, y8, r8]]

def plot(r1, r2, r3):
    coordinates = create_coordinates(r1, r2, r3)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    for x, y, r in coordinates:
        # label by index
        label = str(coordinates.index([x, y, r]) + 1)
        plot_circle(ax, x, y, r, label)

    # Set the plot limits
    max_coord = max([abs(x) + r for x, y, r in coordinates]) * 1.2
    ax.set_xlim(-max_coord, max_coord)
    ax.set_ylim(-max_coord, max_coord)

    plt.title("Three Tangent Circles with Centered Outer Circle")
    # plt.tick_params(axis='both', which='both', bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)
    plt.grid(True)
    plt.show()

r1, r2, r3 = 10, 10, 10
# Plot the circles
# plot(r1, r2, r3)
plot(r1, r2, r3)
