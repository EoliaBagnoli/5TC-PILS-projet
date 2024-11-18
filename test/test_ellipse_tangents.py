from typing import Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np


def find_tangent_lines(
    center: Tuple[float, float],
    semi_axes: Tuple[float, float],
    rotation: float,
    reference_point: Tuple[float, float],
):
    """Find the Ellipse's two tangents that go through a reference point.

    Args:
        center: The center of the ellipse.
        semi_axes: The semi-major and semi-minor axes of the ellipse.
        rotation: The counter-clockwise rotation of the ellipse in radians.
        reference_point: The coordinates of the reference point.

    Returns:
        (m1, h1): Slope and intercept of the first tangent.
        (m2, h2): Slope and intercept of the second tangent.
    """
    x0, y0 = center
    a, b = semi_axes
    s, c = np.sin(rotation), np.cos(rotation)
    p0, q0 = reference_point

    A = (-a**2*s**2 - b**2*c**2 + (y0-q0)**2)
    B = 2*(c*s*(a**2-b**2) - (x0-p0)*(y0-q0))
    C = (-a**2*c**2 - b**2*s**2 + (x0-p0)**2)

    if B**2 - 4*A*C < 0:
        raise ValueError('Reference point lies inside the ellipse')

    t1, t2 = (
        (-B + np.sqrt(B**2 - 4*A*C))/(2*A),
        (-B - np.sqrt(B**2 - 4*A*C))/(2*A),
    )
    return (
        (1/t1, q0 - p0/t1),
        (1/t2, q0 - p0/t2),
    )


# Example:
CENTER = 1, 2
SEMI_AXES = 3, 1
ROTATION = np.pi/3
REFERENCE_POINT = -2, 3

(m1, h1), (m2, h2) = find_tangent_lines(
    center=CENTER,
    semi_axes=SEMI_AXES,
    rotation=ROTATION,
    reference_point=REFERENCE_POINT,
)

fig, ax = plt.subplots()
ax.add_patch(Ellipse(CENTER, 2*SEMI_AXES[0], 2*SEMI_AXES[1], ROTATION/np.pi*180, color='tab:blue', alpha=0.4))
ax.scatter([REFERENCE_POINT[0]], [REFERENCE_POINT[1]], color='tab:blue', s=50)
ax.axline((0, h1), slope=m1, color='tab:orange', lw=1)
ax.axline((0, h2), slope=m2, color='tab:orange', lw=1)
plt.show()