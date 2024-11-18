import cv2
import numpy as np
from sympy import Point, Ellipse, Line

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

height, width = 700, 1500
is_initailizing = True


def draw_body_pattern(image):
    margin = 100
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

    points["a"] = [margin, height-margin]
    points["b"] = [margin+distances.get("inter_epaules"), height-margin]
    points["c"] = [points.get("b")[0], points.get("b")[1]-distances.get("hauteur_cou")]
    points["d"] = [points.get("b")[0], points.get("b")[1]-distances.get("hauteur_buste")]
    points["f"] = [points.get("a")[0], points.get("a")[1]-distances.get("hauteur_buste")]
    points["g"] = [points.get("a")[0], points.get("a")[1]-distances.get("hauteur_cou")]

    points["e"] = [points.get("d")[0]-points.get("f")[0], points.get("d")[1]]
    points["i"] = [points.get("g")[0], int((points.get("a")[1]+points.get("g")[1])/2)]

    for point in list(points.values()) :
        cv2.circle(image, (int(point[0]), int(point[1])), 3, (0, 255, 0), -1) # draw each point as a dot """

    cv2.ellipse(image,(points["d"][0], points["d"][1]),(points["d"][0]-points["e"][0], points["c"][1]-points["d"][1]),0,90,180,255,3)

    image = draw_line_between("e", "g", points, image)
    image = draw_arm_curve_between("g", "i", points, distances, image)
    #image = draw_line_between("g", "h", points, image)
    image = draw_line_between("i", "a", points, image)
    image = draw_line_between("a", "b", points, image)
    image = draw_line_between("b", "c", points, image)

    return image


def draw_line_between(start, end, points, image) : 
    cv2.line(image, (points[start][0], points[start][1]), (points[end][0], points[end][1]), (255, 0, 0), 3)
    return image


def draw_arm_curve_between(start, end, points, distances, image) :
    offset = distances.get("offset")
    largeur = distances.get('largeur_epaules')
    mid_point = [int((points[start][0]+points[end][0])/2) , int(((points[start][1]+points[end][1])/2))+offset]

    points["h"] = [mid_point[0]+largeur, mid_point[1]]

    e1 = Ellipse(Point(mid_point[0], mid_point[1]), int(distances.get("hauteur_cou")/4)-offset, largeur) 
    l1 = e1.tangent_lines(Point(points[start][0],points[end][0])) 

    tangent = l1[1]
    intersection_points = e1.intersection(tangent)
    tangent_point = intersection_points[0] # The intersection_points list will contain the point where the tangent touches the ellipse

    tan_start_point = int(points.get(start)[0]), int(points.get(start)[1])
    tan_end_point = (int(tangent_point.x), int(tangent_point.y))

    # Step 2: Draw the tangent line using OpenCV
    cv2.line(image, tan_start_point, tan_end_point, (255, 0, 0), 3, lineType=cv2.LINE_AA)

    angle_start = 90
    line1 = Line(Point(mid_point[0], mid_point[1]), Point(tan_end_point[0], tan_end_point[1]))
    line2 = Line(Point(mid_point[0], mid_point[1]), Point(mid_point[0]+50, mid_point[1]))
    angle_rad = line1.angle_between(line2)

    # Convert the angle to degrees
    angle_end = angle_rad.evalf() * 180 / 3.141592653589793
    angle_end = float(angle_end) * -1

    cv2.ellipse(image,(mid_point[0], mid_point[1]),(largeur,int(distances.get("hauteur_cou")/4)-offset),0,angle_start,angle_end,255,3, lineType=cv2.LINE_AA)

    return image


def draw_sleeve_pattern(image):
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

    for point in list(points.values()) :
        cv2.circle(image, (int(point[0]), int(point[1])), 3, (0, 255, 0), -1) # draw each point as a dot """

    image = draw_line_between("f", "a", points, image)
    image = draw_line_between("a", "c", points, image)
    image = draw_line_between("c", "g", points, image)

    return image

"""
************************************************ FONCTIONS D'AFFICHAGE ************************************************
"""

# Callback function for the trackbars
def update_image(val):
    global distances

    if is_initailizing:
        return
    
    # Get current positions of the trackbars
    distances["inter_epaules"] = cv2.getTrackbarPos('inter_epaules', 'Image')
    distances["hauteur_buste"] = cv2.getTrackbarPos('hauteur_buste', 'Image')
    distances["hauteur_cou"] = cv2.getTrackbarPos('hauteur_cou', 'Image')
    distances["largeur_epaules"] = cv2.getTrackbarPos('largeur_epaules', 'Image')
    distances["offset"] = cv2.getTrackbarPos('offset', 'Image')
    distances["hauteur_manches"] = cv2.getTrackbarPos('hauteur_manches', 'Image')
    distances["largeur_manches"] = cv2.getTrackbarPos('largeur_manches', 'Image')
    
    # Redraw the image with updated values
    draw_image()


# Function to draw the image with the rectangle
def draw_image():
    # Create a blank white image
    image = np.ones((height, width, 3), np.uint8) * 255

    image = draw_body_pattern(image)
    image = draw_sleeve_pattern(image)
    
    # Show the image
    cv2.imshow('Image', image)


if __name__ == "__main__":
    # Create a window
    cv2.namedWindow('Image')

    # Create trackbars for height and width
    cv2.createTrackbar('inter_epaules', 'Image', distances["inter_epaules"], width, update_image)
    cv2.createTrackbar('hauteur_buste', 'Image', distances["hauteur_buste"], width, update_image)
    cv2.createTrackbar('hauteur_cou', 'Image', distances["hauteur_cou"], width, update_image)
    cv2.createTrackbar('largeur_epaules', 'Image', distances["largeur_epaules"], width, update_image)
    cv2.createTrackbar('offset', 'Image', distances["offset"], width, update_image)
    cv2.createTrackbar('hauteur_manches', 'Image', distances["hauteur_manches"], width, update_image)
    cv2.createTrackbar('largeur_manches', 'Image', distances["largeur_manches"], width, update_image)

    is_initailizing = False
    # Initial image display
    draw_image()

    # Wait until the user presses a key, then exit
    cv2.waitKey(0)
    cv2.destroyAllWindows()
