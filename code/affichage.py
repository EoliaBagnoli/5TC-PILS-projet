import cv2
import numpy as np
import warnings

from bust_pattern import BustPattern
from custom_ellipse import CustomEllipseCurve
from custom_line import CustomLine

class Affichage : 
    def __init__(self):
        self.height, self.width = 700, 1500
        self.is_initailizing = True
        self.test_image = np.ones((self.height, self.width, 3), np.uint8) * 255

    def print_pattern(self, pattern : BustPattern) : 
        """ # Create a window
        cv2.namedWindow('Image')

        # Create trackbars for height and width
        cv2.createTrackbar('inter_epaules', 'Image', distances["inter_epaules"], self.width, self.update_image)
        cv2.createTrackbar('hauteur_buste', 'Image', distances["hauteur_buste"], self.width, self.update_image)
        cv2.createTrackbar('hauteur_cou', 'Image', distances["hauteur_cou"], self.width, self.update_image)
        cv2.createTrackbar('largeur_epaules', 'Image', distances["largeur_epaules"], self.width, self.update_image)
        cv2.createTrackbar('offset', 'Image', distances["offset"], self.width, self.update_image)
        cv2.createTrackbar('hauteur_manches', 'Image', distances["hauteur_manches"], self.width, self.update_image)
        cv2.createTrackbar('largeur_manches', 'Image', distances["largeur_manches"], self.width, self.update_image)
        self.is_initailizing = False """

        self.print_points_as_dots(pattern=pattern)
        self.print_links(pattern=pattern)
        self.draw_image()


    def draw_image(self) :
        cv2.imshow('Image', self.test_image)
        cv2.imwrite('../results/test_pattern.png', self.test_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    
    # Callback function for the trackbars
    def update_image(self):
        global distances

        if self.is_initailizing:
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
        self.draw_image()


    def print_points_as_dots(self, pattern : BustPattern) : 
        print(pattern.points)

        # Define text parameters
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_color = (0, 0, 255)  # Red color for text
        font_thickness = 1
        text_offset = (5, 5)  # Offset for text placement relative to point

        for point_name, coordinates in pattern.points.items():
            # Convert coordinates to integers for cv2
            x, y = int(coordinates[0]), int(coordinates[1])
            point_pos = (x, y)
            
            # Draw the point as a filled circle
            cv2.circle(self.test_image, point_pos, 3, (0, 255, 0), -1)  # Green dot
            
            # Add the point name next to the dot
            text_pos = (x + text_offset[0], y + text_offset[1])
            cv2.putText(self.test_image, point_name, text_pos, 
                    font, font_scale, font_color, font_thickness)


    def print_links(self, pattern : BustPattern) : 
        for link_name, link in pattern.links.items() : 
            if isinstance(link, CustomLine) :
                print("DRAWING LINE")
                self.draw_line(link, pattern)
            if isinstance(link, CustomEllipseCurve) :
                print("DRAWING CURVE")
                self.draw_ellipse(link, pattern)


    def draw_line(self, line : CustomLine, pattern : BustPattern) : 
        cv2.line(self.test_image, pattern.points.get(line.start_point), pattern.points.get(line.end_point), (255, 0, 0), 3)


    def draw_ellipse(self, ellipse : CustomEllipseCurve, pattern : BustPattern) : 
        cv2.ellipse(self.test_image, pattern.points.get(ellipse.center), ellipse.axes, 0, ellipse.compute_start_angle(pattern), ellipse.compute_end_angle(pattern), 255, 3)
        """
            Here : cv2.ellipse(image, center_coordinates as (x,y), axesLength as (a,b), angle, startAngle, endAngle, color, thickness) 
        """