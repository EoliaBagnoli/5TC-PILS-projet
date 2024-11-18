import numpy as np
from scipy.optimize import fsolve

def find_tangent_point(a, b, point_A):
    """
    Trouve le point de tangence X sur une ellipse à partir d'un point extérieur A.
    
    Paramètres:
    a: demi-grand axe de l'ellipse
    b: demi-petit axe de l'ellipse
    point_A: tuple (x,y) des coordonnées du point A
    
    Retourne:
    Liste des points de tangence possibles (généralement 2)
    """
    xa, ya = point_A
    
    def equations(vars):
        # Le point X(x,y) sur l'ellipse
        x, y = vars
        
        # Équation 1: le point X est sur l'ellipse
        eq1 = (x/a)**2 + (y/b)**2 - 1
        
        # Équation 2: la tangente en X passe par A
        # La pente de la tangente est (-b²x)/(a²y)
        # Cette pente doit être égale à (ya-y)/(xa-x)
        eq2 = b**2 * x * (ya-y) - a**2 * y * (xa-x)
        
        return [eq1, eq2]
    
    # On essaie plusieurs points initiaux pour trouver toutes les solutions
    solutions = []
    initial_guesses = [
        (a/2, b/2),
        (-a/2, b/2),
        (a/2, -b/2),
        (-a/2, -b/2)
    ]
    
    for guess in initial_guesses:
        sol = fsolve(equations, guess)
        if np.abs(equations(sol)[0]) < 1e-10 and np.abs(equations(sol)[1]) < 1e-10:
            # Vérifie si cette solution n'est pas déjà trouvée
            if not any(np.allclose(sol, s) for s in solutions):
                solutions.append(sol)
    
    return solutions

# Exemple d'utilisation
def exemple():
    # Paramètres de l'ellipse
    a, b = 5, 3  # demi-axes de l'ellipse
    point_A = (8, 4)  # point extérieur
    
    # Calcul des points de tangence
    points = find_tangent_point(a, b, point_A)
    
    print(f"Pour une ellipse de demi-axes a={a}, b={b}")
    print(f"et un point A{point_A}")
    print("\nPoints de tangence trouvés:")
    for i, point in enumerate(points, 1):
        print(f"X{i}: ({point[0]:.3f}, {point[1]:.3f})")

if __name__ == "__main__":
    exemple()