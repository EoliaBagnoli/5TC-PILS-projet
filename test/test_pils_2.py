import cv2
import numpy as np
from sympy import Point, Ellipse, Line
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

def draw_sleeve(distances, image) :
    points = {
        "a" : [0, 0],
        "b" : [0, 0],
        "c" : [0, 0],
        "d" : [0, 0],
        "e1" : [0, 0],
        "e2" : [0, 0],
        "e3" : [0, 0],
    }

    margin_left = 700
    margin_top = 100

    hauteur_ellipse = int(distances.get("hauteur_cou")/4)-distances.get("offset")
    largeur_ellipse = distances.get('largeur_epaules')

    points["d"] = [largeur_ellipse*2 + margin_left, margin_top]
    points["b"] = [points.get("d")[0], points.get("d")[1]+distances.get("hauteur_manches")]
    points["a"] = [points.get("b")[0]-distances.get("largeur_manches"), points.get("b")[1]]
    points["c"] = [points.get("b")[0]+distances.get("largeur_manches"), points.get("b")[1]]

    points["e1"] = [points.get("d")[0], points.get("d")[1]+hauteur_ellipse]
    cv2.ellipse(image,(points["e1"][0], points["e1"][1]),(largeur_ellipse,hauteur_ellipse),0,0,-180,255,3, lineType=cv2.LINE_AA)

    points["e2"] = [points.get("d")[0]-2*largeur_ellipse, points.get("d")[1]+hauteur_ellipse]
    cv2.ellipse(image,(points["e2"][0], points["e2"][1]),(largeur_ellipse,hauteur_ellipse),0,0,90,255,3, lineType=cv2.LINE_AA)

    points["e3"] = [points.get("d")[0]+2*largeur_ellipse, points.get("d")[1]+hauteur_ellipse]
    cv2.ellipse(image,(points["e3"][0], points["e3"][1]),(largeur_ellipse,hauteur_ellipse),0,180,90,255,3, lineType=cv2.LINE_AA)

    points["f"] = [points.get("e2")[0], points.get("e2")[1]+hauteur_ellipse]
    points["g"] = [points.get("e3")[0], points.get("e3")[1]+hauteur_ellipse]

    print("Drawing each point")
    for point in list(points.values()) :
        print(point)
        cv2.circle(image, (int(point[0]), int(point[1])), 3, (0, 255, 0), -1) # draw each point as a dot """

    image = draw_line_between("f", "a", points, image)
    image = draw_line_between("a", "c", points, image)
    image = draw_line_between("c", "g", points, image)

    return image


def draw_line_between(start, end, points, image) : 
    cv2.line(image, (points[start][0], points[start][1]), (points[end][0], points[end][1]), (255, 0, 0), 3)
    return image


def draw_arm_curve_between(start, end, points, distances, image) :
    offset = distances.get("offset")
    largeur = distances.get('largeur_epaules')
    mid_point = [int((points[start][0]+points[end][0])/2) , int(((points[start][1]+points[end][1])/2))+offset]

    points["h"] = [mid_point[0]+largeur, mid_point[1]]

    tangent_points = find_tangent_point(int(distances.get("hauteur_cou")/4)-offset, largeur, points.get("g"))

    print("TANGENT POINT")

    tangent_point = tangent_points[0] # The intersection_points list will contain the point where the tangent touches the ellipse

    print(tangent_point)

    tan_start_point = int(points.get(start)[0]), int(points.get(start)[1])
    tan_end_point = (int(tangent_point[0]), int(tangent_point[1]))

    # Step 2: Draw the tangent line using OpenCV
    cv2.line(image, tan_start_point, tan_end_point, (255, 0, 0), 3, lineType=cv2.LINE_AA)

    angle_start = 90
    line1 = Line(Point(mid_point[0], mid_point[1]), Point(tan_end_point[0], tan_end_point[1]))
    line2 = Line(Point(mid_point[0], mid_point[1]), Point(mid_point[0]+50, mid_point[1]))
    angle_rad = line1.angle_between(line2)

    # Convert the angle to degrees
    angle_end = angle_rad.evalf() * 180 / 3.141592653589793
    angle_end = float(angle_end) * -1

    print(f"The angle between the two lines is {angle_end} degrees")

    cv2.ellipse(image,(mid_point[0], mid_point[1]),(largeur,int(distances.get("hauteur_cou")/4)-offset),0,angle_start,angle_end,255,3, lineType=cv2.LINE_AA)

    return image



def test_pils():
    points = {
        "a" : [0, 0],
        "b" : [0, 0],
        "c" : [0, 0],
        "d" : [0, 0],
        "e" : [0, 0],
        "f" : [0, 0],
        "g" : [0, 0],
        "h" : [0, 0],
        "i" : [0, 0],
    }

    height, width = 700, 1500
    image = np.zeros((height, width, 3), np.uint8)
    margin = 100

    distances = {
        "inter_epaules" : 300,
        "hauteur_buste" : 550, 
        "hauteur_cou" : 500, 
        "largeur_epaules" : 100, 
        "offset" : 10, 
        "hauteur_manches" : 500,
        "largeur_manches" : 150
    }

    points["a"] = [margin, height-margin]
    points["b"] = [margin+distances.get("inter_epaules"), height-margin]
    points["c"] = [points.get("b")[0], points.get("b")[1]-distances.get("hauteur_cou")]
    points["d"] = [points.get("b")[0], points.get("b")[1]-distances.get("hauteur_buste")]
    points["f"] = [points.get("a")[0], points.get("a")[1]-distances.get("hauteur_buste")]
    points["g"] = [points.get("a")[0], points.get("a")[1]-distances.get("hauteur_cou")]

    points["e"] = [points.get("d")[0]-points.get("f")[0], points.get("d")[1]]
    points["i"] = [points.get("g")[0], int((points.get("a")[1]+points.get("g")[1])/2)]

    print("Drawing each point")
    for point in list(points.values()) :
        print(point)
        cv2.circle(image, (int(point[0]), int(point[1])), 3, (0, 255, 0), -1) # draw each point as a dot """

    cv2.ellipse(image,(points["d"][0], points["d"][1]),(points["d"][0]-points["e"][0], points["c"][1]-points["d"][1]),0,90,180,255,3)

    image = draw_line_between("e", "g", points, image)
    image = draw_arm_curve_between("g", "i", points, distances, image)
    #image = draw_line_between("g", "h", points, image)
    image = draw_line_between("i", "a", points, image)
    image = draw_line_between("a", "b", points, image)
    image = draw_line_between("b", "c", points, image)

    image = draw_sleeve(distances, image)

    cv2.imshow('img', image)



if __name__ == '__main__':
    try:
        test_pils()
        cv2.waitKey(0)
    except KeyboardInterrupt:
        print("Interrupted! Cleaning up...")
    finally:
        cv2.destroyAllWindows()