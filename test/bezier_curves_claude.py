import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

def draw_armpit_shoulder_curve(armpit_point, shoulder_point, control_point_ratio=0.7):
    """
    Draw a curve from armpit to shoulder point using a quadratic Bézier curve.
    
    Parameters:
    armpit_point: tuple (x, y) - coordinates of the armpit point
    shoulder_point: tuple (x, y) - coordinates of the shoulder point
    control_point_ratio: float - controls how steep the initial curve is (0.5 to 0.8 recommended)
    """
    # Convert points to numpy arrays for easier calculation
    P0 = np.array(armpit_point)
    P2 = np.array(shoulder_point)
    
    # Calculate the difference vector between points
    diff = P2 - P0
    
    # Calculate control point
    # Move control_point_ratio of the way from armpit to shoulder horizontally
    # and place it higher than both points to create the curved shape
    vertical_offset = abs(diff[0]) * 0.3  # Adjust this multiplier to change curve height
    P1 = P0 + np.array([diff[0] * control_point_ratio, vertical_offset])
    
    # Create points for the Bézier curve
    t = np.linspace(0, 1, 100)
    curve_points = np.zeros((len(t), 2))
    
    # Calculate quadratic Bézier curve points
    for i, t_i in enumerate(t):
        curve_points[i] = (1-t_i)**2 * P0 + 2*(1-t_i)*t_i * P1 + t_i**2 * P2
    
    # Create the plot
    plt.figure(figsize=(10, 8))
    
    # Plot the curve
    plt.plot(curve_points[:, 0], curve_points[:, 1], 'b-', linewidth=2, label='Pattern Curve')
    
    # Plot the control points and lines
    plt.plot([P0[0], P1[0], P2[0]], [P0[1], P1[1], P2[1]], 'r--', alpha=0.3, label='Control Structure')
    plt.plot(P0[0], P0[1], 'ro', label='Armpit Point')
    plt.plot(P2[0], P2[1], 'go', label='Shoulder Point')
    plt.plot(P1[0], P1[1], 'ko', label='Control Point')
    
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    plt.title('T-Shirt Pattern: Armpit to Shoulder Curve')
    
    return plt.gcf()

# Example usage
armpit = (0, 0)  # Starting point
shoulder = (10, 5)  # Ending point

# Draw the curve
fig = draw_armpit_shoulder_curve(armpit, shoulder, control_point_ratio=2)
plt.show()