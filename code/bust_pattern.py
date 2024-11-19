"""
Hérite de pattern_piece.py et implémente le patron particulier d'un buste
"""
from pattern_piece import PatternPiece
from custom_line import CustomLine
from custom_ellipse import CustomEllipseCurve

from math import sqrt
from sympy import symbols, solve, Eq, sqrt


class BustPattern(PatternPiece) :
    def __init__(self):
        super().__init__(name="BustPattern")
        letter_points = "ABCDEFGHI"
        self.initiate_points(letter_points=letter_points)

    def create_body_pattern(self, distances) : 
        self.set_body_pattern_points(distances)
        self.set_body_pattern_links(distances)
        self.center_points_on_screen(100)

    def set_body_pattern_points(self, distances) : 
        self.set_point("A", [0, distances.get("hauteur_buste")])
        self.set_point("B", [distances.get("inter_aisselles"), distances.get("hauteur_buste")])
        self.set_point("C", [self.get_point_x_value("B"), distances.get("hauteur_buste")-distances.get("hauteur_cou")])
        self.set_point("D", [self.get_point_x_value("B"), 0])
        self.set_point("E", [self.compute_e_point(distances=distances), self.get_point_y_value("D")])
        self.set_point("F", [0,0])
        self.set_point("G", [distances.get("inter_aisselles")-distances.get("inter_epaules"), self.get_point_y_value("C")]) 
        self.set_point("H", self.compute_h_point(distances=distances)) # replace with real values
        self.set_point("I", [0,  distances.get("hauteur_buste") - distances.get("hauteur_aisselles")])
        self.set_point("J", [0, distances.get("hauteur_buste")-distances.get("hauteur_aisselles")-64]) #replace with real values

    def set_body_pattern_links(self, distances) : 
        print(self.points)
        a = abs(self.get_point_x_value("E") - self.get_point_x_value("D"))
        b = abs(self.get_point_y_value("C") - self.get_point_y_value("D"))
        axes_ce = (a, b)
        c = 100
        d = 64
        axes_hi = (c, d)
        self.links = {
            "AB" : CustomLine("A", "B"), 
            "BC" : CustomLine("B", "C"), 
            "CE" : CustomEllipseCurve(axes_ce, "D", "C", "E"), 
            "EG" : CustomLine("E", "G"),
            "GH" : CustomLine("G", "H"), 
            "HI" : CustomEllipseCurve(axes_hi, "J", "I", "H"), 
            "IA" : CustomLine("I", "A")
        }
    
    def solve_system(self, a, b, xa, ya, long):
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

    def compute_h_point(self, distances) : 
        # Définition des paramètres (à modifier selon vos besoins)
        a = 60
        b = 64
        xa, ya = self.points.get("G")
        print(xa, ya)
        long = 25 # Longueur imposée du segment
        
        # Résolution
        solutions = self.solve_system(a, b, xa, ya, long)
        return [solutions[0][0].evalf(), solutions[0][1].evalf()]
    
    def compute_e_point(self, distances) : 
        """
        Trouvée en faisant le théorème de pythagore dans le triangle EGF car E-G est connue et G-F est connue
        """
        return int(sqrt(distances.get("cou_epaule")**2 - (distances.get("hauteur_cou")-distances.get("hauteur_buste"))**2))