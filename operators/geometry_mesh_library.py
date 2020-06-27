from math import *
from mathutils import *




from . geometry_classes import CubePoint, PlanePoint, GeometryEdge, IllusionPlanePoint, IllusionCubePoint
from . geometry_builder_functions import *

#########################################################
#
#   LIBRARY OF IMPOSSIBLE FIGURES
#
#########################################################
'''
The functions in this file return a list of vertex, a list of faces, and a list of vertex groups (paired with an indentifier)
These are then used by the blender API to construct a mesh object.
The functions in this file are called by the operators_construct_geometry.
'''

#####################################
#####################################
def penrose_triangle(size, thickness, side_scaling, illusion_angle_x, illusion_angle_z, illusion_slider_factor = 0.5):
    '''
    Returns the Vertex and Faces of a Penrose Triangle.
    The illusion is produced at the middle point of the vertical side.

    ---------
    size: Lenght of each side of the triangle
    thickness: Thickness of the side of the triangle
    side_scaling[3]: Factor to rescale the side thickness

    illusion_angle_x: Camera rotation X used to define the axonometric proportion
    illusion_angle_z: Camera rotation Z used to define the axonometric proportion

    illusion_slider_factor: At which height should the illusion be located (as a factor)

    '''

    #########################################################
    #
    #   CONSTRUCTION GUIDELINES
    #
    #########################################################
    '''
    Penrose Triangle constraint:
    L1*y - L2*x - L3*z = (0, 0)
    Default = (1, 1, 1)
    '''

    # Lenght of the figure sides
    L1 = Vector((0, size, 0))
    L2 = Vector((-size, 0, 0))

    # Lenght of the sides with illusion point(s), halfway the vertical edge of the triangle
    L0_ia = Vector((0, 0, -(1. - illusion_slider_factor) *  size ))
    L3_ib = Vector((0, 0, -illusion_slider_factor * size))

    vector_directions = [L0_ia, L1, L2, L3_ib]
    vector_origin =  Vector((size/2, -size/2, size/2))


    #########################################################
    #
    #   GENERATE VERTEX AND FACES
    #
    #########################################################

    geometry_locations = generate_locations_from_directions(vector_directions, vector_origin)
    GeometryPoint_List, GeometryEdge_List = generate_closed_illusion_geometry(geometry_locations, thickness, side_scaling, illusion_angle_x, illusion_angle_z)
    verts, faces = generate_vertex_and_faces(GeometryPoint_List, GeometryEdge_List)

    illusion_vertex_groups = generate_illusion_vertex_groups(IllusionPair = [GeometryPoint_List[0], GeometryPoint_List[-1]])

    return verts, faces, illusion_vertex_groups





#####################################
#####################################
def penrose_triangle_block(size, thickness, side_scaling, illusion_angle_x, illusion_angle_z):
    '''
    Returns the Vertex and Faces of a Penrose Triangle in the block variant.
    The illusion is produced at the middle point of the vertical side.

    ---------
    size: Lenght of each side of the triangle
    thickness: Thickness of each cube of the triangle
    side_scaling[3]: Factor to rescale the sides thickness

    illusion_angle_x: Camera rotation X used to define the axonometric proportion
    illusion_angle_z: Camera rotation Z used to define the axonometric proportion

    '''
    #########################################################
    #
    #   CONSTRUCTION GUIDELINES
    #
    #########################################################

    # L: Separation between the cubes.
    # By default there are 5 cubes per side.
    L = 0.25 * size

    # Vector separation between the cubes
    Ai = Vector((0, L, 0))
    Bi = Vector((-L, 0, 0))
    Ci = Vector((0, 0, -L))

    vector_directions = []
    for i in range(2):
        vector_directions.append(Ci)
    for i in range(4):
        vector_directions.append(Ai)
    for i in range(4):
        vector_directions.append(Bi)
    for i in range(2):
        vector_directions.append(Ci)

    vector_origin =  Vector((size/2, -size/2, size/2))


    #########################################################
    #
    #   GENERATE VERTEX AND FACES
    #
    #########################################################

    geometry_locations = generate_locations_from_directions(vector_directions, vector_origin)
    GeometryPoint_List = generate_block_illusion_geometry(geometry_locations, thickness, side_scaling, illusion_angle_x, illusion_angle_z)
    verts, faces = generate_vertex_and_faces(GeometryPoint_List)

    illusion_vertex_groups = generate_illusion_vertex_groups(IllusionPair = [GeometryPoint_List[0], GeometryPoint_List[-1]])


    return verts, faces, illusion_vertex_groups





#####################################
#####################################
def reutersvard_rectangle(height, width, thickness, side_scaling, illusion_angle_x, illusion_angle_z, illusion_slider_factor = 0.5):
    '''
    Returns the Vertex and Faces of a Reutersvard Rectangle.
    The illusion is produced at the middle point of the long vertical side.

    ---------
    height: Lenght of the long vertical side
    width: Lenght of the X,Y sides
    thickness: Thickness of the side
    side_scaling[3]: Factor to rescale the side thickness

    illusion_angle_x: Camera rotation X used to define the axonometric proportion
    illusion_angle_z: Camera rotation Z used to define the axonometric proportion

    illusion_slider_factor: At which height should the illusion be located (as a factor)
    '''


    #########################################################
    #
    #   CONSTRUCTION GUIDELINES
    #
    #########################################################
    '''
    Reutersvard rectangle constraint:
    L1*y + L2*z - L3*x - L4*z= (0, 0)
    Default = (3, 2, 3, 5)
    '''


    # Lenght of the Standard Sides
    L1 = Vector((0, width, 0))
    L2 = Vector((0, 0, height - width))
    L3 = Vector((-width, 0, 0))

    # Lenght of the Illusion Sides
    L0_ia = Vector((0, 0, -(1. - illusion_slider_factor) * height))
    L4_ib = Vector((0, 0, -illusion_slider_factor * height ))

    vector_directions = [L0_ia, L1, L2, L3, L4_ib]
    vector_origin =  Vector((width/2, -width/2, height/2))


    #########################################################
    #
    #   GENERATE VERTEX AND FACES
    #
    #########################################################

    geometry_locations = generate_locations_from_directions(vector_directions, vector_origin)
    GeometryPoint_List, GeometryEdge_List = generate_closed_illusion_geometry(geometry_locations, thickness, side_scaling, illusion_angle_x, illusion_angle_z)
    verts, faces = generate_vertex_and_faces(GeometryPoint_List, GeometryEdge_List)

    illusion_vertex_groups = generate_illusion_vertex_groups(IllusionPair = [GeometryPoint_List[0], GeometryPoint_List[-1]])


    return verts, faces, illusion_vertex_groups




#####################################
#####################################
def impossible_arch(height, width_A, width_B, thickness, side_scaling, illusion_angle_x, illusion_angle_z, illusion_slider_factor = 0.5):
    '''
    Returns the Vertex and Faces of a Impossible Arch.
    The illusion is produced at the middle point of the long vertical side.

    ---------
    height: Lenght of the long vertical side
    width_A, width_B: Lenght of the X,Y sides
    thickness: Thickness of the side
    side_scaling[3]: Factor to rescale the side thickness

    illusion_angle_x: Camera rotation X used to define the axonometric proportion
    illusion_angle_z: Camera rotation Z used to define the axonometric proportion

    illusion_slider_factor: At which height should the illusion be located (as a factor)
    '''

    #########################################################
    #
    #   CONSTRUCTION GUIDELINES
    #
    #########################################################
    '''
    Impossible Arch constraint:
    L1*x + L2*y + L3*z - L4*x - L5*z= (0, 0)
    Default = (2, 2, 3, 4, 6)
    '''

    # Lenght of the Standard Sides
    L1 = Vector((width_A, 0, 0))
    L2 = Vector((0, width_B, 0))
    L3 = Vector((0, 0, height - width_B))
    L4 = Vector((-width_A - width_B, 0, 0))

    # Lenght of the Illusion Sides
    L0_ia = Vector((0, 0, -(1. - illusion_slider_factor) * height))
    L5_ib = Vector((0, 0, -illusion_slider_factor * height ))


    vector_directions = [L0_ia, L1, L2, L3, L4, L5_ib]
    vector_origin =  Vector((-width_A/2, -(width_A + width_B)/2, height/2))


    #########################################################
    #
    #   GENERATE VERTEX AND FACES
    #
    #########################################################

    geometry_locations = generate_locations_from_directions(vector_directions, vector_origin)
    GeometryPoint_List, GeometryEdge_List = generate_closed_illusion_geometry(geometry_locations, thickness, side_scaling, illusion_angle_x, illusion_angle_z)
    verts, faces = generate_vertex_and_faces(GeometryPoint_List, GeometryEdge_List)

    illusion_vertex_groups = generate_illusion_vertex_groups(IllusionPair = [GeometryPoint_List[0], GeometryPoint_List[-1]])


    return verts, faces, illusion_vertex_groups



#####################################
#####################################
def penrose_stair(size, thickness, side_scaling, illusion_angle_x, illusion_angle_z):
    '''
    Returns the Vertex and Faces of a penrose stair

    ---------
    size: Stair longest side lenght
    thickness: Thickness of the steps
    side_scaling[3]: Factor to rescale the thickness

    illusion_angle_x: Camera rotation X used to define the axonometric proportion
    illusion_angle_z: Camera rotation Z used to define the axonometric proportion


    '''
    #########################################################
    #
    #   CONSTRUCTION GUIDELINES
    #
    #########################################################
    '''
    # Penrose Stair constraint:

    Side A: N1*(L1*y + L2*Z)
    Side B: N1*(-L1*x + L2*Z)
    Side C: N2*(-L1*y + L3*Z)
    Side D: N2*(L1*x + L3*Z)
    A + B + C + D = (0, 0)

    Default N1 = 2, N2 = 4
    Default L1 = 2, L2 = 0.5, L3 = 0.25
    '''

    # Vector Separation between the steps
    L1 = 2.0 * size/8.
    L2 = 0.5 * size/8.
    L3 = 0.25 * size/8.

    Ai = Vector((0, L1, L2))
    Bi = Vector((-L1, 0, L2))
    Ci = Vector((0, -L1, L3))
    Di = Vector((L1, 0, L3))


    vector_directions = []
    for i in range(2):
        vector_directions.append(Di)
    for i in range(2):
        vector_directions.append(Ai)
    for i in range(2):
        vector_directions.append(Bi)
    for i in range(4):
        vector_directions.append(Ci)
    for i in range(2):
        vector_directions.append(Di)

    vector_origin =  Vector((L1, -L1, 0))


    #########################################################
    #
    #   GENERATE VERTEX AND FACES
    #
    #########################################################

    geometry_locations = generate_locations_from_directions(vector_directions, vector_origin)
    GeometryPoint_List = generate_block_illusion_geometry(geometry_locations, thickness, side_scaling, illusion_angle_x, illusion_angle_z, cube_axis_alignment = ["X-", "X+"])
    verts, faces = generate_vertex_and_faces(GeometryPoint_List)


    # Notice that in the penrose stair the first illusion is in the back
    illusion_vertex_groups = generate_illusion_vertex_groups(IllusionPair = [GeometryPoint_List[-1], GeometryPoint_List[0]])

    return verts, faces, illusion_vertex_groups




#####################################
#####################################
def impossible_cube(size, thickness, side_scaling, illusion_angle_x, illusion_angle_z):
    '''
    Returns the Vertex and Faces of an Impossible Cube.
    The upper and lower levels are connected by an impossible bridge.
    The figure is only visible from the isometric perspective.
    The figure is constructed rotated, to align the illusion with the vertical direction. The figure is de-rotated in the operator call.

    ---------
    size: Lenght of the longest side
    thickness: Thickness of the side
    side_scaling[3]: Factor to rescale the side thickness

    illusion_angle_x: Camera rotation X used to define the axonometric proportion
    illusion_angle_z: Camera rotation Z used to define the axonometric proportion

    '''

    #########################################################
    #
    #   CONSTRUCTION GUIDELINES
    #
    #########################################################

    # Location of the standard cube points
    Loc = [Vector((-1, -1, -1)),
            Vector((-1, -1, 1)),
            Vector((-1, 1, -1)),
            Vector((-1, 1,  1)),
            Vector((1, -1, -1)),
            Vector(( 1, 1, -1)),
            Vector(( 1, 1,  1))]

    # Location of the illusion points
    ILoc = [Vector((-1, 1,  1 - 1)), Vector((1, -1, -1 + 3))]

    for i in range(len(Loc)):
        for j in range(3):
            Loc[i][j] *= size/2
    for i in range(len(ILoc)):
        for j in range(3):
            ILoc[i][j] *= size/2


    #########################################################
    #
    #   CONSTRUCT GEOMETRY POINTS
    #
    #########################################################

    ID_counter = 0
    PointList = []


    # Standard Cube GeometryPoints
    for i in range(len(Loc)):
        PointList.append(CubePoint(ID_counter, Loc[i], thickness, side_scaling, illusion_angle_x, illusion_angle_z))
        ID_counter = PointList[-1].next_Id


    # Illusion Plane Points
    P_ia = IllusionPlanePoint(PointList[-1].next_Id, ILoc[0], thickness, side_scaling, illusion_angle_x, illusion_angle_z)
    P_ib = IllusionPlanePoint(P_ia.next_Id, ILoc[1], thickness, side_scaling, illusion_angle_x, illusion_angle_z)
    PointList.append(P_ia)
    PointList.append(P_ib)

    # Edges
    EdgeList = []

    EdgeList.append(GeometryEdge(PointList[0], PointList[1]))
    EdgeList.append(GeometryEdge(PointList[0], PointList[2]))
    EdgeList.append(GeometryEdge(PointList[0], PointList[4]))
    EdgeList.append(GeometryEdge(PointList[1], PointList[3]))
    EdgeList.append(GeometryEdge(PointList[2], PointList[5]))
    EdgeList.append(GeometryEdge(PointList[3], PointList[6]))
    EdgeList.append(GeometryEdge(PointList[4], PointList[5]))
    EdgeList.append(GeometryEdge(PointList[5], PointList[6]))

    EdgeList.append(GeometryEdge(PointList[3], P_ia))
    EdgeList.append(GeometryEdge(PointList[4], P_ib))


    #########################################################
    #
    #   CREATE VERTICES AND FACES
    #
    #########################################################
    verts, faces = generate_vertex_and_faces(PointList, EdgeList)

    #########################################################
    #
    #   MARK THE ILLUSION VERTEX GROUPS
    #
    #########################################################

    illusion_vertex_groups = generate_illusion_vertex_groups(IllusionPair = [P_ib, P_ia])


    return verts, faces, illusion_vertex_groups










