import os
# Disable all Qt logging
os.environ["QT_LOGGING_RULES"] = "*=false"
os.environ["QT_DEBUG_PLUGINS"] = "0"
os.environ["QT_VERBOSE"] = "0"

from bust_pattern import BustPattern
from affichage import Affichage

if __name__ == "__main__" : 

    # Initial values for the variables
    distances = {
            "inter_epaules" : 300,
            "inter_aisselles" : 330,
            "cou_epaule" : 230,
            "hauteur_buste" : 550, 
            "hauteur_cou" : 500, 
            "hauteur_aisselles" : 300,
            "largeur_epaules" : 64, 
            "offset" : 60, 
            "hauteur_manches" : 500,
            "largeur_manches" : 150
        }
    
    p1 = BustPattern()
    p1.create_body_pattern(distances=distances)
    a1 = Affichage()
    a1.print_pattern(p1)