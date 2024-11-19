import numpy as np
import cv2

def quadratic_bezier_curve(start_point, control_point, end_point, num_points=100):
    """
    Generate points along a quadratic Bézier curve
    
    Args:
    - start_point: Starting point (G)
    - control_point: Control point (H)
    - end_point: Ending point (I)
    - num_points: Number of points to generate along the curve
    
    Returns:
    - Array of points on the Bézier curve
    """
    t_values = np.linspace(0, 1, num_points)
    curve_points = np.zeros((num_points, 2))
    
    for i, t in enumerate(t_values):
        # Quadratic Bézier curve formula
        curve_points[i] = (1-t)**2 * start_point + \
                          2 * (1-t) * t * control_point + \
                          t**2 * end_point
    
    return curve_points.astype(np.int32)

# Specified points
I = np.array([100., 350.])  # start point
H = np.array([150., 330.])  # control point
G = np.array([130., 150.])  # end point

# Create a blank canvas
canvas = np.zeros((1000, 1000, 3), dtype=np.uint8)

# Generate Bézier curve points
curve_points = quadratic_bezier_curve(G, H, I)

# Draw the curve
cv2.polylines(canvas, [curve_points], isClosed=False, color=(0, 255, 0), thickness=2)

# Draw original points
""" cv2.circle(canvas, [G[0], G[1]], 5, (0, 0, 255), -1)  # End point in red
cv2.circle(canvas, tuple(H), 5, (255, 0, 0), -1)  # Control point in blue
cv2.circle(canvas, tuple(I), 5, (0, 255, 255), -1)  # Start point in yellow """

# Show the result
cv2.imshow('Bézier Curve', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()