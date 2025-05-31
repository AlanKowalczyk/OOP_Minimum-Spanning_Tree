"""
Created on 23 Feb 2024
Last modification 25 Feb 2024 by AK

author Alan Kowalczyk
"""


class Point(object):
    """
    a class of Point()
    """

    def __init__(self, x, y):
        """
        the constructor of a class, initialise with coordinate <x,y>
        """
        self.x = x
        self.y = y

    def __str__(self):
        """
        return a string representation of coordinates in format <x,y>
        """
        return "<" + str(self.x) + "," + str(self.y) + ">"
    
    def get_distance_from(self, other):
        """
        return a float distance between {self} object and {other} object
        """
        x_dist = self.x - other.get_x()
        y_dist = self.y - other.get_y()
        return (x_dist ** 2 + y_dist ** 2) ** 0.5
    
    def get_x(self):
        """
        return a x value as int
        """
        return self.x
    
    def get_y(self):
        """
        return a y value as int
        """
        return self.y
    
    
class Edge(object):
    """ 
    class Edge() connecting two objects of class Point()
    """
    def __init__(self, left_point, right_point):
        """ 
        the constructor of a class, initialise with two Point() objects between which Edge() is connecting
        """
        self.left_point = left_point
        self.right_point = right_point
        self.weight = left_point.get_distance_from(right_point)
        
    def __str__(self):
        """ 
        return a string representation of the Edge()
        """
        return str(self.left_point) + '<->' + str(self.right_point)
        
    def get_left_point(self):
        """ 
        return a left point of class Point()
        """
        return self.left_point

    def get_right_point(self):
        """ 
        return a right point of class Point()
        """
        return self.right_point
    
    def get_weight(self):
        """ 
        return a weight of the {edge}, which is the distance between {points}, as float
        """
        return self.weight
    
    def __lt__(self, other):
        """ 
        return True if weight of {self} is smaller than weight of {other}, False otherwise -> for comparison in Priority Queue (hepq)
        """
        return self.weight < other.weight


class Graph(object):
    """ 
    class Graph() containing objects of class Point(), connected by object(s) class Edge()
    """
    def __init__(self):
        """ 
        the constructor of a class, initialise empty
        """
        self.points = {}
        self.edges = []
    
    def add_point(self, point):
        """     
        adding an {point} object to a Graph()
        """
        if point not in self.points:
            self.points[point] = []
        
    def add_edge(self, edge):
        """ 
        adding an {edge} between {points}, and if {points} are not previously explicitly declared, then add {points} too, as the {edge} has to connect two {points{} and can not exist without {points}
        """
        if edge.get_left_point() not in self.points:
            self.add_point(edge.get_left_point())
        if edge.get_right_point() not in self.points:
            self.add_point(edge.get_right_point())
        #add right_point to list of neigbours as value in a dict of points at key left_point
        self.points[edge.get_left_point()].append(edge.get_right_point())
        self.edges.append(edge)
        
    def get_points(self):
        """ 
        return a list of {points}
        """
        return list(self.points.keys())
    
    def get_edges(self):
        """ 
        return a list of {edges}
        """
        return self.edges
        
    def get_points_dict(self):
        """ 
        return a dictionary mapping each {point} to their neighbours
        """
        return self.points
