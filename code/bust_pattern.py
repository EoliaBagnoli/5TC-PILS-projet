"""
Hérite de pattern_piece.py et implémente le patron particulier d'un buste
"""
from pattern_piece import PatternPiece
from custom_line import CustomLine
from custom_ellipse import CustomEllipseCurve
from custom_polyline import CustomPolyline

from math import sqrt
from sympy import symbols, solve, Eq, sqrt
import numpy as np


class BustPattern(PatternPiece) :
    def __init__(self, style, sleeves):
        super().__init__(name="BustPattern")
        self.style = style
        self.sleeves = sleeves
        letter_points = "ABCDEFGHIJKL"
        self.initiate_points(letter_points=letter_points)

    def create_body_pattern(self, distances) : 
        print("CREATING BODY PATTERN")
        self.set_body_pattern_points(distances)
        self.set_body_pattern_links(distances)
        self.center_points_on_screen(100)

    def set_body_pattern_points(self, distances) : 
        self.set_point("A", [0, distances.get("hauteur_buste")])
        self.set_point("B", [distances.get("inter_aisselles"), distances.get("hauteur_buste")])
        self.set_point("C", [self.get_point_x_value("B"), distances.get("f-g")])
        self.set_point("D", [self.get_point_x_value("B"), 0])
        self.set_point("E", [distances.get("f-e"), self.get_point_y_value("D")])
        self.set_point("F", [0,0])
        self.set_point("G", [distances.get("inter_aisselles")-distances.get("inter_epaules"), (self.get_point_y_value("C")/ 2)]) 
        self.set_point("I", [0,  distances.get("f-i")])
        self.set_point("H", [distances.get("largeur_epaules"), (self.get_point_y_value("G")+self.get_point_y_value("I"))/2]) # replace with real values
        self.set_point("J", [self.get_point_x_value("H")*1.7, self.get_point_y_value("I")]) #replace with real values
        self.set_point("K", [distances.get("f-k"), (abs(self.get_point_y_value("A")+self.get_point_y_value("I")))/2])
        self.set_point("L", [distances.get("f-l"), (abs(self.get_point_y_value("A")+self.get_point_y_value("I")))/2])

    def set_body_pattern_links(self, distances) : 
        print(self.points)
        a = abs(self.get_point_x_value("E") - self.get_point_x_value("D"))
        b = abs(self.get_point_y_value("C") - self.get_point_y_value("D"))
        axes_ce = (a, b)
        self.links = {
            "AB" : CustomLine("A", "B"), 
            "BC" : CustomLine("B", "C"), 
            "CE" : CustomEllipseCurve(axes_ce, "D", "C", "E"), 
            "EG" : CustomLine("E", "G"),
            "GI" : CustomPolyline(start_point="I", end_point="G", through_point="J"), 
            "IA" : CustomPolyline(start_point="I", end_point="A", through_point="L")
        }
        if self.style == 'loose' : 
            self.links["IA"] = CustomLine("I", "A")

    def compute_h_point(self, distances) : 
        return [50, 230]
    
    def compute_e_point(self, distances) : 
        """
        Trouvée en faisant le théorème de pythagore dans le triangle EGF car E-G est connue et G-F est connue
        """
        return int(sqrt(distances.get("cou_epaule")**2 - (distances.get("f-g"))**2))
        