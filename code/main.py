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

    for i in distances_init :
        distances_init[i] = int(distances_init[i]*100)

    # lateral distances are divided by 2 to make a half pattern
    distances_final["cou"] = int(distances_init.get("cou")) / 2
    distances_final["inter_epaules"] = int(distances_init.get("inter_epaules")) / 2
    distances_final["inter_aisselles"] = int(distances_init.get("inter_aisselles")) / 2
    distances_final["tour_de_taille"] = 40 / 2 # change to actual value when json is ready

    distances_final["cou_epaule"] = distances_init.get("epaule_cou")
    distances_final["hauteur_buste"] = distances_init.get("epaule_hanche")
    distances_final["hauteur_cou"] = distances_init.get("hauteur_cou")
    distances_final["hauteur_aisselles"] = distances_init.get("hauteur_aisselle")
    distances_final["hauteur_manches"] = distances_init.get("poignet_epaule")

    print(distances_final)

    # ensure all values in the dict are ints
    for value in distances_final:
        distances_final[value] = int(distances_final[value]) * 10

    distances_final["largeur_epaules"] = distances_init.get("poignet_epaule") # this value is random
    distances_final["offset"] = 60
    distances_final["largeur_manches"] = 150

    return distances_final


def invoke_pattern(json_path, style, sleeves) : 
    # Initial values for the variables
    with open(json_path, 'r') as file:
        data = json.load(file)
        print(data)

    distances = convert_dict_files(data)
    
    distances["f-g"] = abs(distances.get("hauteur_buste") - distances.get("hauteur_cou"))
    distances["f-i"] = distances.get("hauteur_buste") - distances.get("hauteur_aisselles")
    distances["f-e"] = distances.get("inter_aisselles") - distances.get("cou")
    distances["f-k"] = abs(distances.get("inter_aisselles") - distances.get("tour_de_taille"))
    distances["f-l"] = abs(distances.get("inter_aisselles") - int(distances.get("tour_de_taille") * 1.4))
    
    print(distances)

    p1 = BustPattern(style=style, sleeves=sleeves)
    a1 = Affichage(distances=distances, pattern=p1, name=json_path)
    a1.print_pattern()


if __name__ == "__main__" : 
    invoke_pattern('../mesures_2.json', style='fit', sleeves='short')
    invoke_pattern('../mesures_2.json', style='loose', sleeves='long')