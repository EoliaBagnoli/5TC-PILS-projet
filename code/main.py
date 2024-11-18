from bust_pattern import BustPattern
from affichage import Affichage

if __name__ == "__main__" : 

    # Initial values for the variables
    distances = {
            "inter_epaules" : 300,
            "hauteur_buste" : 550, 
            "hauteur_cou" : 500, 
            "largeur_epaules" : 64, 
            "offset" : 60, 
            "hauteur_manches" : 500,
            "largeur_manches" : 150
        }
    
    p1 = BustPattern()
    p1.create_body_pattern(distances=distances)
    a1 = Affichage()
    a1.print_pattern(p1)