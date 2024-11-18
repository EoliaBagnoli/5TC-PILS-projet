from sympy import symbols, solve, Eq, sqrt

def solve_system_symbolic():
    """
    Résout symboliquement le système d'équations :
    1: (y*(a**2)) / (x*(b**2)) = ((x-xa) / (y-ya))
    2: sqrt((x-xa)^2 + (y-ya)^2) = long
    
    Returns:
        list: Liste des solutions (x, y) en fonction de a, b, xa, ya et long
    """
    # Définition de tous les symboles
    x, y, a, b, xa, ya, long = symbols('x y a b xa ya long')
    
    # Première équation : relation des rapports
    eq1 = Eq((y*(a**2))/(x*(b**2)), (x-xa)/(y-ya))
    
    # Deuxième équation : contrainte de longueur
    eq2 = Eq(sqrt((x-xa)**2 + (y-ya)**2), long)
    
    # Résolution du système
    try:
        solutions = solve((eq1, eq2), (x, y))
        return solutions
    except Exception as e:
        print(f"Erreur lors de la résolution : {str(e)}")
        return None

def print_symbolic_solutions(solutions):
    """
    Affiche les solutions symboliques de manière formatée
    """
    print("Solutions symboliques trouvées :")
    if not solutions:
        print("Aucune solution trouvée")
        return
        
    if isinstance(solutions, list):
        for i, sol in enumerate(solutions, 1):
            print(f"\nSolution {i}:")
            print(f"x = {sol[0]}")
            print(f"y = {sol[1]}")
    else:
        x, y = symbols('x y')
        print(f"x = {solutions.get(x)}")
        print(f"y = {solutions.get(y)}")

def main():
    # Résolution symbolique
    solutions = solve_system_symbolic()
    
    # Affichage des résultats
    print_symbolic_solutions(solutions)

if __name__ == "__main__":
    main()