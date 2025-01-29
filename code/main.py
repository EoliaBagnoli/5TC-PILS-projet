import os
import json
# Disable all Qt logging
os.environ["QT_LOGGING_RULES"] = "*=false"
os.environ["QT_DEBUG_PLUGINS"] = "0"
os.environ["QT_VERBOSE"] = "0"

from bust_pattern import BustPattern
from affichage import Affichage


def convert_dict_files(distances_init) :
    distances_final = {}
    # lateral distances are divided by 2 to make a half pattern
    distances_final["cou"] = int(distances_init.get("cou")) / 2
    distances_final["inter_epaules"] = int(distances_init.get("inter_epaules")) / 2
    distances_final["inter_aisselles"] = int(distances_init.get("inter_aisselles")) / 2

    distances_final["cou_epaule"] = distances_init.get("epaules_cou")
    distances_final["hauteur_buste"] = distances_init.get("hauteur_cou_1")
    distances_final["hauteur_cou"] = distances_init.get("hauteur_cou_2")
    distances_final["hauteur_aisselles"] = distances_init.get("hauteur_aisselle")
    distances_final["hauteur_manches"] = distances_init.get("poignet_epaules")
    distances_final["hauteur_manches"] = distances_init.get("hauteur_cou_2")

    # ensure all values in the dict are ints
    for value in distances_final:
        distances_final[value] = int(distances_final[value]) * 8

    distances_final["largeur_epaules"] = distances_init.get("poignet_epaules") # this value is random
    distances_final["offset"] = 60
    distances_final["largeur_manches"] = 150

    return distances_final

def invoke_pattern(json_path) : 
    # Initial values for the variables
    with open(json_path, 'r') as file:
        data = json.load(file)

    distances = convert_dict_files(data)
    
    distances["f-g"] = distances.get("hauteur_buste") - distances.get("hauteur_cou")
    distances["f-i"] = distances.get("hauteur_buste") - distances.get("hauteur_aisselles")
    distances["f-e"] = distances.get("inter_aisselles") - distances.get("cou")
    
    print(distances)

    p1 = BustPattern()

    a1 = Affichage(distances=distances, pattern=p1, name=json_path)
    a1.print_pattern()
    a1.save_pattern_image()


if __name__ == "__main__" : 
    invoke_pattern('../distances_ewan.json')
    invoke_pattern('../distances_raf.json')
    invoke_pattern('../distances_eolia.json')
