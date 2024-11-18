from sympy import Point, Ellipse 

e1 = Ellipse(Point(0, 0), 3, 2) 
  
# using tangent_lines() method 
l1 = e1.tangent_lines(Point(3, 0)) 
  
print(l1) 