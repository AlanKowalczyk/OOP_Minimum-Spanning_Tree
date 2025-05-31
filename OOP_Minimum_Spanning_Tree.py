"""
Created on 31 Jan 2024
Last modification 25 Feb 2024 by AK

author Alan Kowalczyk
"""


distance_for_finding_neigbours = 20
file_name = 'week1.csv'


from hashlib import sha256
import drawsvg
from operator import attrgetter
from classes import *
import heapq
import datetime as dt


def read_file(file_name):
    """
    read_file - a function which is responsible for reading data from a file
    input:
        file_name - a string - name of file with data
    output:
        data - a list - list of y values as strings
    """
    try: 
        with open(file_name, 'r') as f:
            for row in f:
                data = row.strip().split(",") 
        return data
    except FileNotFoundError:
        print(f"There is no such file: {file_name}, check directory and spelling.")


def checksum(data):
    """ 
    checksum - a function which checks the validity of data using SHA256 checksum
    input:
        data - a list - list of y values as strings
    output:
        - a boolean - True if the checksum matches the provided checksum in the helper file, False otherwise
    """
    data_to_hash = ''
    for y in data:
        data_to_hash += y
    expected_checksum = "5c14e4599f1d2a39abe6b487ac2a5415c894c6882f5fdd4a40e02c7dd628829a"
    hashed_data = sha256(data_to_hash.encode('utf-8')).hexdigest()
    print(f"Concatenated y values from the file presented below: \n{data_to_hash}")
    print(f"Validity of test data by calculating SHA256 checksum: \n  Actual checksum: {hashed_data} \nExpected checksum: {expected_checksum}")
    return(f"Is a match?:       {hashed_data == expected_checksum}")
    

def instantiating_point_objects(data):
    """ 
    instantiating_point_object - a function which is instantiating Point objects
    input:
        data - a list - a list of y value as str
    output:
        points_list - a list - a list of Points objects
    """
    points_list = []
    x = 1
    for y in data:
            point = Point(x, int(y))
            points_list.append(point)
            x += 1
    return points_list


def neighbours(origin, list_of_points, distance):
    """
    neighbours - a function which is finding all neighbours from origin within a {distance} range
    input:
        origin - an object - a Point object
        list_of_points - a list - a list where function is looking for neighbours
        distance - an int - distance within we would like to find neighbours
    output:
        neighbours_list - a list - a list of neighbours
    """
    neighbours_list = []
    for point in list_of_points:
        dist = origin.get_distance_from(point)
        if dist <= distance and dist > 0:
           neighbours_list.append(point)
    return neighbours_list

 
def mst(graph):
    """ 
    mst - a function, which is generating a Minimum Spanning Tree
    input:
        graph - an object - an object class Graph
    output:
        mst - an object - an object class Graph as MST
    """
    sorted_edges = sorted(graph.get_edges(), key = attrgetter("weight"))
    dict_of_points = graph.get_points_dict()
    mst = Graph()

    # Adding the first shortest edge and both points to the MST
    mst.add_edge(sorted_edges[0])

    # Creating a priority queue
    priority_queue = []

    # Add all edges between existing points in MST and their neighbours to the priority queue
    for point in mst.get_points():
        for neighbour in dict_of_points[point]:
            if neighbour not in mst.get_points():
                heapq.heappush(priority_queue, Edge(point, neighbour))

    while len(mst.get_points()) < len(graph.get_points()):
        # Get the edge with the smallest weight from the priority queue
        edge = heapq.heappop(priority_queue)
        right_point = edge.get_right_point()

        if edge not in mst.get_edges() and right_point not in mst.get_points():
            mst.add_edge(edge)
            # Add edges between the new point and its neighbours to the priority queue
            for neighbour in dict_of_points[right_point]:
                if neighbour not in mst.get_points():
                    heapq.heappush(priority_queue, Edge(right_point, neighbour))
    return mst


def graph_to_svg(graph, filename):
    """ 
    graph_to_svg - a function, which is drawing an object class Graph() as an SVG image
    source HEP503 from Abertay University, unit 7.5, accessed: 21 Feb 2024, modified
    input:
        graph - an object - an object type Graph for drawing
        filename - a string - filename to which function will save a file
    output:
        none
    """
    height = 800 
    width = 800
    padding = 20 #to keep points away from the edge of the drawing
    today_date = dt.date.today()
    d = drawsvg.Drawing(width, height)
    
    # Add a white rectangle to be the background of the drawing
    d.append(drawsvg.Rectangle(0, 0, width, height, fill = "white"))
    
    for edge in graph.get_edges():
        # Flip the y-coordinates by subtracting from height, so the start point of axes (0,0) will be bottom left
        d.append(drawsvg.Line((edge.get_left_point().get_x() * 7.5 + padding), (height - edge.get_left_point().get_y() * 7.5 - padding),
                              (edge.get_right_point().get_x() * 7.5 + padding), (height - edge.get_right_point().get_y() * 7.5 - padding),
                              stroke = "blue", stroke_width = 2, fill = "none"))
          
    for point in graph.get_points():
        # Adjust point positions so the start point of axes (0,0) will be bottom left
        d.append(drawsvg.Circle((point.get_x() * 7.5 + padding), (height - point.get_y() * 7.5 - padding), 5,
                                fill = "red", stroke_width = 2, stroke = "black"))

    d.append(drawsvg.Text(f"author: Alan Kowalczyk, created on {today_date}", 14, 275, 15))
    
    with open(f"{filename}.svg", 'w') as f:
        f.write(d.as_svg())


#reading data from file
data_from_file = read_file(file_name)

#checking hash (checksum)
print(checksum(data_from_file))

#instantiating Points objects with "y" values from the file
list_of_points = instantiating_point_objects(data_from_file)

#finding all neighbours for all points and storing them in dictionary: key - point, value - list on neighbours of this point
dict_of_neighbours = {}
for point in list_of_points:
    dict_of_neighbours[point] = neighbours(point, list_of_points, distance_for_finding_neigbours)

#instantiating Graph object with Points objects as vertices and with distances between vertices as weights of edges    
graph = Graph()
for point in list_of_points:
    for neighbour in dict_of_neighbours[point]:
        graph.add_edge(Edge(point, neighbour))

#generating a minimum spanning tree
graph_as_mst = mst(graph)

#using an SVG for rendering Graphs objects as images
graph_to_svg(graph, "graph") #the original graph with all edges
graph_to_svg(graph_as_mst, "MST") #MST
