from math import *
from mathutils import *


from . geometry_classes import CubePoint, GeometryEdge, IllusionPlanePoint, IllusionCubePoint




#########################################################
#
#   FUNCTIONS TO CREATE GEOMETRY OBJECTS AND GENERATE VERTEX/FACES
#
#########################################################

def generate_locations_from_directions(vector_directions, vector_origin = Vector((0, 0, 0))):
    '''
    Returns an array of vector locations based on an array of directions and an origin point.
    -----------
    vector_directions: Array of vectors that represent the sides of the figure.
    vector_origin: Origin point of the figure.
    '''

    geometry_locations = [vector_origin]
    for direction in vector_directions:
        geometry_locations.append(geometry_locations[-1] + direction)

    return geometry_locations


def generate_closed_illusion_geometry(geometry_locations, thickness, side_scaling, illusion_angle_x, illusion_angle_z, initial_Id = 0, plane_axis_alignment = "Z"):
    '''
    Returns the GeometryPoints and GeometryEdges from a closed illusion figure, such as the penrose triangle, or the reutersvard rectangle.
    It assumes that the locations are given in a sequential order.
    The first and the last points will be illusions planes.
    ---------
    geometry_locations: Array of vectors that indicate where to build the geometry

    thickness: Thickness of the side of the triangle
    side_scaling[3]: Factor to rescale the side thickness

    illusion_angle_x: Camera rotation X used to define the axonometric proportion
    illusion_angle_z: Camera rotation Z used to define the axonometric proportion

    initial_Id: Id of the first vertex to be created by this routine
    plane_axis_alignment: Orientation of the illusion planes
    '''


    # List of Points Objects
    PointList = []
    # List of Edge Objects
    EdgeList = []

    # Construct the first illusion plane
    P_ia = IllusionPlanePoint(initial_Id, geometry_locations[0], thickness, side_scaling, illusion_angle_x, illusion_angle_z, axis_alignment = plane_axis_alignment)
    PointList.append(P_ia)

    # For the intermediate locations construct a cube point
    for i in range(1, len(geometry_locations) - 1):
        new_point = CubePoint(PointList[-1].next_Id, geometry_locations[i], thickness, side_scaling, illusion_angle_x, illusion_angle_z)
        PointList.append(new_point)

    # Construct the last illusion plane
    P_ib = IllusionPlanePoint(PointList[-1].next_Id, geometry_locations[-1], thickness, side_scaling, illusion_angle_x, illusion_angle_z, axis_alignment = plane_axis_alignment)
    PointList.append(P_ib)

    # Construct the edges between the points
    for i in range(len(PointList) - 1):
        EdgeList.append(GeometryEdge(PointList[i], PointList[i + 1]))


    return PointList, EdgeList

def generate_block_illusion_geometry(geometry_locations, thickness, side_scaling, illusion_angle_x, illusion_angle_z, initial_Id = 0, cube_axis_alignment = ["Z+", "Z-"]):
    '''
    Returns the GeometryPoints from a block illusion figure, such as the penrose triangle (block variant), or the penrose stair.
    It assumes that the locations are given in a sequential order.
    The first and the last points will be illusions cubes.
    ---------
    geometry_locations: Array of vectors that indicate where to build the geometry

    thickness: Thickness of the side of the triangle
    side_scaling[3]: Factor to rescale the side thickness

    illusion_angle_x: Camera rotation X used to define the axonometric proportion
    illusion_angle_z: Camera rotation Z used to define the axonometric proportion

    initial_Id: Id of the first vertex to be created by this routine
    cube_axis_alignment: Orientation of the illusion cubes
    '''

    # List of Points Objects
    PointList = []
    # List of Edge Objects
    EdgeList = []

    # Construct the first illusion cube
    P_ia = IllusionCubePoint(initial_Id, geometry_locations[0], thickness, side_scaling, illusion_angle_x, illusion_angle_z, axis_alignment = cube_axis_alignment[0])
    PointList.append(P_ia)

    # For the intermediate locations construct a cube point
    for i in range(1, len(geometry_locations) - 1):
        new_point = CubePoint(PointList[-1].next_Id, geometry_locations[i], thickness, side_scaling, illusion_angle_x, illusion_angle_z)
        PointList.append(new_point)

    # Construct the last illusion cube
    P_ib = IllusionCubePoint(PointList[-1].next_Id, geometry_locations[-1], thickness, side_scaling, illusion_angle_x, illusion_angle_z, axis_alignment = cube_axis_alignment[1])
    PointList.append(P_ib)

    return PointList


def generate_vertex_and_faces(GeometryPoint_List, GeometryEdge_List = []):
    '''
    Takes a list of GeometryPoints and GeometryEdges objects and returns the corresponding vertex and faces.
    The vertex and faces can be passed into blender to construct the 3D geometry
    '''
    verts = []
    faces = []

    for Point in GeometryPoint_List:
        Point.append_Vertices(verts)
        Point.append_Faces(faces)

    for Edge in GeometryEdge_List:
        Edge.append_Faces(faces)

    return verts, faces


def generate_illusion_vertex_groups(IllusionPair = [], GroupNames = ["IllusionFront", "IllusionBack"]):
    '''
    Generates an array with pairs [GroupName, vertex_Ids], that will be used by blender to assign the vertex groups to the mesh.
    --------
    IllusionPair = Pair of IllusionPoint Objects that will be used to obtain the vertex Ids.
    GroupNames = Pair of names to identify the illusion vertex groups
    '''

    illusion_vertex_groups = []
    for i in range(2):

        # Check if the illusion point is a plane or a cube
        if IllusionPair[i].point_type == "IPLANE":
            vertex_group =  IllusionPair[i].get_VertexIds_PlaneFace(IllusionPair[i].axis_alignment)
        elif IllusionPair[i].point_type == "ICUBE":
            vertex_group =  IllusionPair[i].get_VertexIds_CubeFace(IllusionPair[i].axis_alignment)

        # Append the Name, Group pair
        illusion_vertex_groups.append([GroupNames[i], vertex_group])

    return illusion_vertex_groups
