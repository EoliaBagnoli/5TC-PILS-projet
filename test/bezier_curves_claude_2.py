import numpy as np
import matplotlib.pyplot as plt

def draw_precise_curve(start_point, end_point, through_point):
    """
    Create a quadratic Bézier curve that passes exactly through a specified point.
    
    Parameters:
    start_point: tuple (x, y) - starting point (armpit)
    end_point: tuple (x, y) - ending point (shoulder)
    through_point: tuple (x, y) - point the curve must pass through
    
    Returns:
    numpy array of curve points
    """
    # Convert points to numpy arrays
    P0 = np.array(start_point)
    P2 = np.array(end_point)
    P1 = np.array(through_point)
    
    # Calculate the control point that makes the curve pass through the specified point
    # We'll use the mathematical solution for a quadratic Bézier curve
    t = 0.5  # We'll use midpoint by default, but this can be adjusted
    
    # Calculate the control point using the explicit point constraint
    # Solve the quadratic equation: P = (1-t)²P0 + 2(1-t)tP1 + t²P2
    numerator = P1 - (1-t)**2 * P0 - t**2 * P2
    denominator = 2 * (1-t) * t
    
    actual_control_point = numerator / denominator
    
    # Create points for the Bézier curve
    t_values = np.linspace(0, 1, 100)
    curve_points = np.zeros((len(t_values), 2))
    
    # Calculate quadratic Bézier curve points
    for i, t_i in enumerate(t_values):
        curve_points[i] = (1-t_i)**2 * P0 + 2*(1-t_i)*t_i * actual_control_point + t_i**2 * P2
    
    # Create the plot
    plt.figure(figsize=(10, 8))
    
    # Plot the curve
    plt.plot(curve_points[:, 0], curve_points[:, 1], 'b-', linewidth=2, label='Pattern Curve')
    
    # Plot the points
    plt.plot(P0[0], P0[1], 'ro', label='Start Point')
    plt.plot(P2[0], P2[1], 'go', label='End Point')
    plt.plot(P1[0], P1[1], 'ko', label='Specified Control Point')
    plt.plot(actual_control_point[0], actual_control_point[1], 'mo', label='Computed Control Point')
    
    # Plot lines connecting points
    plt.plot([P0[0], actual_control_point[0], P2[0]], 
             [P0[1], actual_control_point[1], P2[1]], 'r--', alpha=0.3)
    
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    plt.title('Bézier Curve Passing Through Specified Point')
    
    # Verify that the curve passes through the specified point
    midpoint_index = len(curve_points) // 2
    computed_midpoint = curve_points[midpoint_index]
    
    print(f"Specified through point:  {P1}")
    print(f"Curve point at midpoint:  {computed_midpoint}")
    print(f"Difference:               {np.linalg.norm(P1 - computed_midpoint)}")
    
    return curve_points

# Example usage
start_point = (0, 0)    # Armpit point
end_point = (10, 5)     # Shoulder point
through_point = (6, 5)  # Point the curve must pass through

# Draw the curve
curve = draw_precise_curve(start_point, end_point, through_point)
plt.show()