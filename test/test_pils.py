import cv2
import numpy as np

global points 

def draw_rectangle(base_point, height, width, image) :
    x1, y1 = base_point
    x2 = x1 + width
    y2 = y1 - height
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2) 
    return image


def test_pils():

    height, width = 700, 700
    image = np.zeros((height, width, 3), np.uint8)
    margin = 100

    points = {
        "bottom_left_corner" : [0, 0],
        "bottom_right_corner" : [0, 0],
        "neck_center" : [0, 0],
        "shoulder_neck" : [0, 0],
        "shoulder_edge" : [0, 0],
        "armpit" : [0, 0]
    }   

    distances = {
        "inter_epaules" : 350,
        "hauteur_buste" : 580, 
        "hauteur_cou" : 500
    }

    print(points)
    points["bottom_left_corner"] = [margin, height-margin]
    points["bottom_right_corner"] = [margin+distances.get("inter_epaules"), height-margin]
    print(points)

    # first rectangle
    x1, y1 = points.get("bottom_left_corner")
    x2 = x1 + distances.get("inter_epaules")
    y2 = y1 - distances.get("hauteur_buste")
    points["shoulder_neck"] = [x1+(distances.get("inter_epaules")/2), y2]
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2) 

    # second rectangle
    x1, y1 = points.get("bottom_left_corner")
    x2 = x1 + distances.get("inter_epaules")
    y2 = y1 - distances.get("hauteur_cou")
    points["neck_center"] = [x2, y2]
    points["shoulder_edge"] = [x1, y2]
    points["armpit"] = [x1, y2+(distances.get("hauteur_cou")/2)]
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2) 

    print("Drawing each point")
    for point in list(points.values()) :
        print(point)
        cv2.circle(image, (int(point[0]), int(point[1])), 3, (0, 255, 0), -1) # draw each point as a dot """

    print("Relying the points")
    precedent = points.get("armpit")
    for point in list(points.values()) : 
        print(precedent)
        print(point)
        x1, y1 = precedent
        x2, y2 = point
        cv2.line(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 3)
        precedent = point

    print("drawing armcourbe")
    armpit = points.get("armpit")
    x_armpit, y_armpit = armpit
    shoulder_edge = points.get("shoulder_edge")
    x_shoulder_edge, y_shoulder_egde = shoulder_edge
    offset = 10
    mid_point = [x_armpit, int((y_shoulder_egde+y_armpit)/2)+offset]
    print(mid_point)
    cv2.ellipse(image,(mid_point[0], mid_point[1]),(50,int(distances.get("hauteur_cou")/4)-offset),0,0,90,255,3)

    print("drawing neckcourbe")
    armpit = points.get("armpit")
    x_armpit, y_armpit = armpit
    shoulder_edge = points.get("shoulder_edge")
    x_shoulder_edge, y_shoulder_egde = shoulder_edge
    offset = 10
    mid_point = [x_armpit, int((y_shoulder_egde+y_armpit)/2)+offset]
    print(mid_point)
    cv2.ellipse(image,(mid_point[0], mid_point[1]),(50,int(distances.get("hauteur_cou")/4)-offset),0,0,90,255,3)

    cv2.imshow('img', image)


if __name__ == '__main__':
    try:
        test_pils()
        cv2.waitKey(0)
    except KeyboardInterrupt:
        print("Interrupted! Cleaning up...")
    finally:
        cv2.destroyAllWindows()