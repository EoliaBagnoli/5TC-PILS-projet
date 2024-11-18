from sympy import symbols, solve, Eq, sqrt

def solve_system(a, b, xa, ya, long):
    """
    Résout le système d'équations :
    1: (y*(a**2)) / (x*(b**2)) = ((x-xa) / (y-ya))
    2: sqrt((x-xa)^2 + (y-ya)^2) = long
    
    Args:
        a, b : paramètres des coefficients
        xa, ya : coordonnées du point A
        long : longueur imposée du segment [XA]
    
    Returns:
        list: Liste des solutions (x, y)
    """
    # Définition des symboles pour x et y
    x, y = symbols('x y')
    
    # Première équation : relation des rapports
    eq1 = Eq((y*(a**2))/(x*(b**2)), (x-xa)/(y-ya))
    
    # Deuxième équation : contrainte de longueur
    eq2 = Eq(sqrt((x-xa)**2 + (y-ya)**2), long)
    
    # Résolution du système
    solution = solve((eq1, eq2), (x, y))
    
    return solution

def print_solutions(solutions, xa, ya):
    """
    Affiche les solutions de manière formatée
    """
    print("Solutions trouvées :")
    if not solutions:
        print("Aucune solution trouvée")
        return
        
    if isinstance(solutions, list):
        for i, sol in enumerate(solutions, 1):
            print(f"\nSolution {i}:")
            print(f"x = {sol[0].evalf()}")
            print(f"y = {sol[1].evalf()}")
            if sol[0] == xa and sol[1] == ya:
                print("Note: Cette solution correspond au point A (cas trivial)")
    else:
        print(f"x = {solutions.get(x)}")
        print(f"y = {solutions.get(y)}")

def verify_solution(x_val, y_val, a, b, xa, ya, long):
    """
    Vérifie si une solution respecte bien les deux équations
    """
    # Vérification de la première équation
    eq1_left = (y_val*(a**2))/(x_val*(b**2))
    eq1_right = (x_val-xa)/(y_val-ya)
    eq1_valid = abs(eq1_left - eq1_right) < 1e-10
    
    # Vérification de la longueur
    actual_length = ((x_val-xa)**2 + (y_val-ya)**2)**0.5
    length_valid = abs(actual_length - long) < 1e-10
    
    return eq1_valid and length_valid

def main():
    # Définition des paramètres (à modifier selon vos besoins)
    a = 2
    b = 2
    xa = 1
    ya = 1
    long = 2  # Longueur imposée du segment
    
    try:
        # Résolution
        solutions = solve_system(a, b, xa, ya, long)
        
        # Affichage des résultats
        print_solutions(solutions, xa, ya)
        
        # Affichage des paramètres utilisés
        print("\nParamètres utilisés:")
        print(f"a = {a}")
        print(f"b = {b}")
        print(f"xa = {xa}")
        print(f"ya = {ya}")
        print(f"longueur = {long}")
        
        # Vérification des solutions
        print("\nVérification des solutions:")
        if isinstance(solutions, list):
            for i, sol in enumerate(solutions, 1):
                x_val, y_val = sol
                if verify_solution(x_val, y_val, a, b, xa, ya, long):
                    print(f"Solution {i}: Valide")
                else:
                    print(f"Solution {i}: Non valide (erreurs numériques possibles)")
        
    except Exception as e:
        print(f"Une erreur s'est produite lors de la résolution : {str(e)}")
        print("Note : Cette erreur peut être due à des divisions par zéro ou d'autres singularités dans l'équation.")

if __name__ == "__main__":
    main()