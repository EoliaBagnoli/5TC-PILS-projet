import numpy as np
import cv2

def quadratic_interpolation_curve(start_point, end_point, through_point, image_size=(500, 500)):
    """
    Create a quadratic interpolation curve passing through three specified points.
    
    Parameters:
    start_point: tuple (x, y) - starting point (armpit)
    end_point: tuple (x, y) - ending point (shoulder)
    through_point: tuple (x, y) - point the curve must pass through
    image_size: tuple (width, height) - size of the output image
    
    Returns:
    numpy array (image with curve)
    """
    # Convert points to numpy arrays
    P0 = np.array(start_point, dtype=np.float64)
    P2 = np.array(end_point, dtype=np.float64)
    P1 = np.array(through_point, dtype=np.float64)
    
    # Create a white image
    img = np.ones((image_size[1], image_size[0], 3), dtype=np.uint8) * 255
    
    # Compute quadratic interpolation coefficients
    def compute_parabola_coefficients(x0, y0, x1, y1, x2, y2):
        """
        Compute coefficients for a parabola passing through three points
        """
        denom = (x0 - x1) * (x0 - x2) * (x1 - x2)
        if abs(denom) < 1e-10:
            # Fallback if denominator is too close to zero
            return lambda x: np.mean([y0, y1, y2])
        
        A = (x2 * (y1 - y0) + x1 * (y0 - y2) + x0 * (y2 - y1)) / denom
        B = (x2*x2 * (y0 - y1) + x1*x1 * (y2 - y0) + x0*x0 * (y1 - y2)) / denom
        C = (x1 * x2 * (x1 - x2) * y0 + x2 * x0 * (x2 - x0) * y1 + x0 * x1 * (x0 - x1) * y2) / denom
        
        return lambda x: A*x*x + B*x + C
    
    # Generate x values
    x_values = np.linspace(P0[0], P2[0], 100)
    
    # Compute the parabolic function
    y_func = compute_parabola_coefficients(P0[0], P0[1], P1[0], P1[1], P2[0], P2[1])
    
    # Generate curve points
    curve_points = np.zeros((len(x_values), 2), dtype=np.int32)
    for i, x in enumerate(x_values):
        curve_points[i] = [int(x), int(y_func(x))]
    
    # Draw the curve
    cv2.polylines(img, [curve_points], isClosed=False, color=(0, 0, 255), thickness=2)
    
    # Draw points
    cv2.circle(img, tuple(P0.astype(np.int32)), 8, (0, 0, 255), -1)  # Start point - red
    cv2.circle(img, tuple(P2.astype(np.int32)), 8, (0, 255, 0), -1)  # End point - green
    cv2.circle(img, tuple(P1.astype(np.int32)), 8, (0, 0, 0), -1)   # Through point - black
    
    # Add text labels
    cv2.putText(img, f"Start: {P0}", tuple(P0.astype(np.int32) + [10, 10]), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.putText(img, f"End: {P2}", tuple(P2.astype(np.int32) + [10, 10]), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(img, f"Through: {P1}", tuple(P1.astype(np.int32) + [10, 10]), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    # Find the point on the curve closest to the through point
    distances = np.linalg.norm(curve_points - P1, axis=1)
    closest_point_index = np.argmin(distances)
    closest_point = curve_points[closest_point_index]
    
    print(f"Specified through point:  {P1}")
    print(f"Closest point on curve:   {closest_point}")
    print(f"Distance:                 {np.linalg.norm(P1 - closest_point)}")
    
    return img

# Multiple test cases to show flexibility
def run_tests():
    # Test case 1: Gentle curve
    img1 = quadratic_interpolation_curve(
        start_point=(50, 50),     # Armpit
        end_point=(400, 300),     # Shoulder
        through_point=(200, 150)  # Curve point
    )
    
    # Test case 2: Steeper curve
    img2 = quadratic_interpolation_curve(
        start_point=(50, 50),     # Armpit
        end_point=(400, 300),     # Shoulder
        through_point=(200, 50)   # Higher curve point
    )
    
    # Test case 3: Asymmetric curve
    img3 = quadratic_interpolation_curve(
        start_point=(50, 50),     # Armpit
        end_point=(400, 300),     # Shoulder
        through_point=(300, 100)  # Offset curve point
    )
    
    # Display images
    cv2.imshow('Test 1: Gentle Curve', img1)
    cv2.imshow('Test 2: Steeper Curve', img2)
    cv2.imshow('Test 3: Asymmetric Curve', img3)
    
    # Save images
    """cv2.imwrite('gentle_curve.png', img1)
    cv2.imwrite('steeper_curve.png', img2)
    cv2.imwrite('asymmetric_curve.png', img3)"""
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Run the tests
run_tests()