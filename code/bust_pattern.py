"""
Hérite de pattern_piece.py et implémente le patron particulier d'un buste
"""
from pattern_piece import PatternPiece
from custom_line import CustomLine
from custom_ellipse import CustomEllipseCurve


class BustPattern(PatternPiece) :
    def __init__(self):
        super().__init__(name="BustPattern")
        
        letter_points = "ABCDEFGHI"
        self.initiate_points(letter_points=letter_points)

    def create_body_pattern(self, distances) : 
        self.set_body_pattern_points(distances)
        self.set_body_pattern_links()
        self.center_points_on_screen(100)

    def set_body_pattern_points(self, distances) : 
        self.set_point("A", [0, distances.get("hauteur_buste")])
        self.set_point("B", [distances.get("inter_epaules"), distances.get("hauteur_buste")])
        self.set_point("C", [self.get_point_x_value("B"), distances.get("hauteur_buste")-distances.get("hauteur_cou")])
        self.set_point("D", [self.get_point_x_value("B"), 0])
        self.set_point("E", [250, self.get_point_y_value("D")]) #replace 50 ! 
        self.set_point("F", [0,0])
        self.set_point("G", [5, self.get_point_y_value("C")]) #here, replace 5 with small offset so A and G are not completely aligned
        self.set_point("H", [50,230]) # replace with real values
        self.set_point("I", [0, int((self.get_point_y_value("G") + self.get_point_y_value("A"))/2)])
        self.set_point("J", [0, self.get_point_y_value("H")]) #replace 50 ! 

    def set_body_pattern_links(self) : 
        self.links = {
            "AB" : CustomLine("A", "B"), 
            "BC" : CustomLine("B", "C"), 
            "CE" : CustomEllipseCurve(20, 20, "D", "C", "E"), 
            "EG" : CustomLine("E", "G"),
            "GH" : CustomLine("G", "H"), 
            "HI" : CustomEllipseCurve(20, 20, "J", "C", "E"), 
            "IA" : CustomLine("I", "A")
        }