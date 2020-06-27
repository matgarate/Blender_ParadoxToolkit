from math import *
from mathutils import *


#########################################################
#
#   BASIC GEOMETRY OBJECT OPERATIONS
#
#########################################################

class GeometryFaceOperations:
    '''
    Basic Functions to obtain the vertex intex of a face.
    Basic Functions to append a vertex or face to the external Blender list.

    The child objects should define a variable valid_faces and vertex Ids
    '''


    #########################################################
    #
    #   BASIC FACE UTILITIES
    #
    #########################################################


    def get_ValidFaceList(self):
        '''
        Returns the six possible face identifiers
        '''
        return ["X+", "X-", "Y+", "Y-", "Z+", "Z-"]

    def remove_ValidFace(self, remove_face):
        '''
        Removes "remove_face" from the list self.valid_faces that is used to construct the Blender faces
        '''
        # Check if the face to be removed is in the valid_faces list
        if remove_face in self.valid_faces:
            self.valid_faces.remove(remove_face)

    #########################################################
    #
    #   GET FACE VERTEX IDS
    #
    #########################################################

    def get_VertexIds_PlaneFace(self, face):
        '''
        Returns the four vertex indexes of a plane in counterclockwise direction.
        Assumes that the vertex are given in the following order [x, y, z]:
        [-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1]
        [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]
        *This is the order in which the relative locations are appended
        ---------
        face: face from which to get the vertex
        vertex_Ids [array[4]]: array of four vertex indexes.
        valid_faces: List of desired faces to construct
        ---------
        Face Identifiers: "X-", "Y+", "X+", "Y-", "Z+", "Z-": Left, Front, Right, Back, Up, Down
        * If the face is only marked as "X", "Y", or "Z", the positive direction is assumed in this case
        Notice that the vertex Ids start counting from 0
        Notice that the vertex are returned in the counter-clockwise direction, around the face normal.
        '''

        # Correct in case the direction was ommited
        if face == "X" or face == "Y" or face == "Z":
            face = face + "+"


        ci = self.vertex_Ids
        face_vertex_Ids = ()
        if face == "X-" or face == "Y+" or face == "Z-":
            face_vertex_Ids = (ci[0], ci[1], ci[3], ci[2])
        if face == "X+" or face == "Y-" or face == "Z+":
            face_vertex_Ids = (ci[0], ci[2], ci[3], ci[1])
        return face_vertex_Ids

    def get_VertexIds_CubeFace(self, face):
        '''
        Returns the vertex belonging to the specified face of a cube given eight vertex
        Assumes that the vertex are given in the following order [x, y, z]:
        [-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1]
        [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]
        *This is the order in which the relative locations are appended
        ---------
        face: face from which to get the vertex
        vertex_Ids [array[8]]: array of eight vertex indexes.
        valid_faces: List of desired faces to construct
        ---------
        Face Identifiers: "X-", "Y+", "X+", "Y-", "Z+", "Z-": Left, Front, Right, Back, Up, Down
        Notice that the vertex Ids start counting from 0
        Notice that the vertex are given in couner-clockwise direction, around the face normal.
        '''

        ci = self.vertex_Ids
        face_vertex_Ids = ()
        if face == "X-":
            face_vertex_Ids = (ci[0], ci[1], ci[3], ci[2])
        if face == "Y+":
            face_vertex_Ids = (ci[2], ci[3], ci[7], ci[6])
        if face == "X+":
            face_vertex_Ids = (ci[6], ci[7], ci[5], ci[4])
        if face == "Y-":
            face_vertex_Ids = (ci[4], ci[5], ci[1], ci[0])
        if face == "Z+":
            face_vertex_Ids = (ci[7], ci[3], ci[1], ci[5])
        if face == "Z-":
            face_vertex_Ids = (ci[2], ci[6], ci[4], ci[0])

        return face_vertex_Ids


class GeometryAppendOperations:
    '''
    Basic Functions to append a vertex or face to the external Blender list.

    The child objects should define a variable valid_faces and vertex_absolute_location
    '''


    def append_Vertices(self, verts):
        '''
        Append the vertex associated to the current GeometryPoint to an external vertex list.
        ---------
        Inputs:
        verts: External array of vertex that will be passed into Blender
        '''
        vertex_absolute_location = self.vertex_absolute_location
        for i in range(len(vertex_absolute_location)):
            verts.append((vertex_absolute_location[i]))

    def append_Faces(self, faces):
        '''
        Append the faces associated to the current GeometryPoint to an external face list.
        ---------
        Inputs:
        faces: External array of faces that will be passed into Blender
        '''

        for i in range(len(self.valid_faces)):
            faces.append(self.get_VertexIds_CubeFace(self.valid_faces[i]))




#########################################################
#
#   GEOMETRY POINT BASE CLASS
#
#########################################################

class GeometryPoint(GeometryAppendOperations, GeometryFaceOperations):
    '''
    Parent Class.
    Baisc unit to construct impossible geometry.
    Each Geometry point defines:
    - A central location
    - A collection of vertex around the central location
    - The collection of faces around the central location

    Inherits the basic functions from GeometryAppendOperations and GeometryFaceOperations
    '''

    def InitializePoint(self, base_ID = 0,
                        location = Vector((0, 0, 0)), thickness = 1.0, side_scaling = Vector((1, 1, 1)),
                        illusion_angle_x = radians(54.736), illusion_angle_z = radians(45),
                        apply_axonometric_correction = True,
                        axis_alignment = None,
                        point_type = None):
        '''
        Method to initialize a GeometryPoint.
        It must be called by the __init__ functions of the child objects
        ----------
        Inputs:
        base_ID: Starting external ID. Each vertex will be assigned an unique ID upon initialization.
        location: Central location of the GeometryPoint class.
        thickness: Thickness used to construct the vertices around the location
        side_scaling: Factors to rescale the thickness in each axis
        illusion_angle_x: X-Camera Rotation necessary to see the illusion
        illusion_angle_z: Z-Camera Rotation necessary to see the illusion
        apply_axonometric_correction: Correct the GeometryPoint location depending on the camera angle (following the penrose continuity constraint)
        axis_alignment: In the case of Illusion Points, Axis or Axis+Direction to which the illusion is oriented (e.g. X, Y, Z, X+, X-, Y+, Y-, Z+, Z-, etc).
        point_type: String that described the type of GeometryPoint (e.g. CUBE, IPLANE, ICUBE, etc).
        '''

        # Assign the point type to the GeometryPoint. It must be defined by the child objects.
        self.point_type = point_type

        # Assign the axis alignment, to which an illusion object is oriented.
        # A regular object may not have an axis_alignment
        self.axis_alignment = axis_alignment

        # Assign the GeometryPoint (Isometric) location
        self.location = location

        # Determine the relative position of the vertices around the GeometryPoint location (Defined by the child objects)
        self.vertex_relative_location = self.calculate_Vertex_RelativeLocation(thickness, side_scaling, illusion_angle_x, illusion_angle_z, axis_alignment)

        # Determine the absolute location of the vertex associated to the GeometryPoint
        # It considers the corrections made by the axonometric perspective
        self.vertex_absolute_location = self.calculate_Vertex_AbsoluteLocation(illusion_angle_x, illusion_angle_z, apply_axonometric_correction)

        # Assign each vertex a unique global ID that will match the order in which these are added to Blender Mesh
        self.vertex_Ids = self.assign_Vertex_Ids(base_ID)

        # This variable is used as reference to create the next GeometryPoint
        self.next_Id = self.vertex_Ids[-1] + 1


        # Initialize the valid faces to construct. (Empty by default. Child objects should fill this list)
        self.valid_faces = []



    #########################################################
    #
    #   GEOMETRIC CALCULATION FUNCTIONS
    #
    #########################################################

    def get_AxonometricFactor(self, illusion_angle_x, illusion_angle_z):
        '''
        Axonometric correction for the side proportions.
        ----------------
        Inputs:
        Float illusion_angle_x: X-Camera Rotation necessary to see the illusion [Radians]
        Float illusion_angle_z: Z-Camera Rotation necessary to see the illusion [Radians]
        ----------------
        Returns:
        Vector[3] Axonometric_Factors
        ----------------
        The axonometric factors are obtained from the continuity illusion constraint of the penrose triangle.
        When a applied (multiplied) to a figure corner locations, the figure is rescaled to preserve the continuity illusion.
        The axonometric factors also can be used to find to correct some illusion proportions.
        The axonometric factors are set by default to keep the sizes in the Z-axis constant.
        '''
        x_axonometric_factor = tan(illusion_angle_x) * sin(illusion_angle_z)
        y_axonometric_factor = tan(illusion_angle_x) * cos(illusion_angle_z)

        return Vector((x_axonometric_factor, y_axonometric_factor, 1.0))


    def get_IllusionCorrection(self, thickness, side_scaling, illusion_angle_x, illusion_angle_z, axis_alignment, enforce_orientation = None):
        '''
        Displacement required to align a face with the line of sight.
        --------------
        thickness: Figure thickness
        side_scaling[3]: Factors to rescale the thickness
        illusion_angle_x: X-Camera Rotation necessary to see the illusion
        illusion_angle_z: Z-Camera Rotation necessary to see the illusion

        axis_alignment: Axis to which the face normal is aligned (X, Y, Z).
        enforce_orientation: The illusion can be aligned along the:
                             (H) Horizontal axis of the face (valid for axis_alignment = X, Y),
                             (V) Vertical axis of the face (valid for axis_alignment = X, Y),
                             (D) Diagonal of the face (valid for axis_alignment = Z),
                             (X) X-Axis (valid for axis_alignment = Z)
                             (Y) Y-Axis (valid for axis_alignment = Z)
                             If None, then pick the shortest option for axis_alignment = X,Y, or Diagonal for axis_alignment = Z
        -------------------
        Returns:
        illusion_correction: Displacement to align the face to the line of sight
        illusion_orientation: Direction in which the correction is applied. Used to decide which vertex to move
        '''

        x_scale, y_scale, z_scale = side_scaling
        axonometric_factor = self.get_AxonometricFactor(illusion_angle_x, illusion_angle_z)

        # Find the correction for the camera angle to create the continuity illusion
        # Illusion face aligned to the Z axis
        if axis_alignment == "Z":
            # Align correction across the diagonal
            triangle_height = thickness * (x_scale * y_scale) / sqrt(x_scale**2.0 + y_scale**2.0)
            diagonal_angle = pi - atan(x_scale / y_scale) - (illusion_angle_z)
            diagonal_size = triangle_height / sin(diagonal_angle)

            # Height correction for the vertex at the illusion location
            illusion_correction_D = diagonal_size / tan(illusion_angle_x)


            # Align correction across the X axis (Get dZ, given dY)
            delta_Y = thickness * y_scale / 2
            illusion_correction_X = delta_Y * (sin(illusion_angle_z) * tan(illusion_angle_z) + cos(illusion_angle_z)) / tan(illusion_angle_x)

            # Align correction across the Y axis (Get dZ, given dX)
            delta_X = thickness * x_scale / 2
            illusion_correction_Y = delta_X * (sin(illusion_angle_z) + cos(illusion_angle_z) / tan(illusion_angle_z)) / tan(illusion_angle_x)

            # Illusion Orientation is Diagonal
            if enforce_orientation == "X":
                illusion_orientation = "X"
                illusion_correction = illusion_correction_X
            elif enforce_orientation == "Y":
                illusion_orientation = "Y"
                illusion_correction = illusion_correction_Y
            else:
                illusion_orientation = "D"
                illusion_correction = illusion_correction_D

        # Illusion face aligned to the X axis
        elif axis_alignment == "X":
            # Align correction across the Horizontal axis
            delta_Z = thickness * z_scale / 2
            illusion_correction_H = delta_Z * axonometric_factor[0]

            # Align correction across the Vertical axis
            delta_Y = thickness * y_scale / 2
            illusion_correction_V = delta_Y * axonometric_factor[0]/axonometric_factor[1]

            # If the orientation is not enforced, pick the smallest correction
            if (illusion_correction_H <= illusion_correction_V or enforce_orientation == "H") and enforce_orientation != "V":
                illusion_orientation = "H"
                illusion_correction = illusion_correction_H
            else:
                illusion_orientation = "V"
                illusion_correction = illusion_correction_V

        # Illusion face aligned to the Y axis
        elif axis_alignment == "Y":
            # Align correction across the Horizontal axis
            delta_Z = thickness * z_scale / 2
            illusion_correction_H = delta_Z * axonometric_factor[1]

            # Align correction across the Vertical axis
            delta_X = thickness * x_scale / 2
            illusion_correction_V = delta_X * axonometric_factor[1]/axonometric_factor[0]

            # If the orientation is not enforced, pick the smallest correction
            if (illusion_correction_H <= illusion_correction_V or enforce_orientation == "H") and enforce_orientation != "V":
                illusion_orientation = "H"
                illusion_correction = illusion_correction_H
            else:
                illusion_orientation = "V"
                illusion_correction = illusion_correction_V

        return illusion_correction, illusion_orientation


    def calculate_GeometryPoint_AxonometricLocation(self, location, illusion_angle_x, illusion_angle_z):
        '''
        Calculates the position of the GeometryPoint considering the axonometric angle correction
        ----------
        Inputs:
        Vector[3] location: Location of the Geometry Point (Given in the Isometric coordinates)
        Float illusion_angle_x: X-Camera Rotation necessary to see the illusion [Radians]
        Float illusion_angle_z: Z-Camera Rotation necessary to see the illusion [Radians]
        ----------------
        Return:
        Vector[3]: location (Corrected by the axonometric factors)
        '''

        axonometric_factor = self.get_AxonometricFactor(illusion_angle_x, illusion_angle_z)
        axonometric_location = location.copy()
        for i in range(len(location)):
            axonometric_location[i] *= axonometric_factor[i]
        return axonometric_location


    #########################################################
    #
    #   VERTEX CALCULATION FUNCTIONS
    #
    #########################################################

    def calculate_Vertex_RelativeLocation(self, thickness, side_scaling, illusion_angle_x, illusion_angle_z, axis_alignment = None):
        '''
        Abstract Function that should return the relative location of the vertex around a location.
        The child objects must implement the method to calculate these locations.
        '''
        vertex_relative_location = []
        return vertex_relative_location


    def calculate_Vertex_AbsoluteLocation(self, illusion_angle_x, illusion_angle_z, apply_axonometric_correction = True):
        '''
        Calculates the absolute location of the vertex using the relative locations and the point central location.
        It also uses the illusion angles to correct the location (which is given in isometric coordinates) to match the axonometric perspective
        Float illusion_angle_x: X-Camera Rotation necessary to see the illusion [Radians]
        Float illusion_angle_z: Z-Camera Rotation necessary to see the illusion [Radians]
        ----------
        Returns:
        List<Vector[3]> vertex_absolute_location: absolute location of the vertex around the GeometryPoint
        '''

        # Read the isometric location of the GeometryPoint and apply the axonometric correction if necessary
        absolute_location = self.location
        if apply_axonometric_correction:
            absolute_location = self.calculate_GeometryPoint_AxonometricLocation(self.location, illusion_angle_x, illusion_angle_z)


        vertex_relative_location = self.vertex_relative_location
        vertex_absolute_location = []

        for i in range(len(vertex_relative_location)):
            vertex_absolute_location.append((absolute_location + vertex_relative_location[i]))
        return vertex_absolute_location

    def assign_Vertex_Ids(self, base_ID):
        '''
        Assigns a unique (global) ID to each vertex associated to the GeometryPoint
        ----------
        Inputs:
        base_ID: External ID to start the unique ID assignment
        ----------
        Returns:
        List<Int> vertex_Ids: unique IDs for each vertex
        '''
        vertex_Ids = []
        for i in range(len(self.vertex_absolute_location)):
            vertex_Ids.append(base_ID)
            base_ID = base_ID + 1
        return vertex_Ids



#########################################################
#
#   GEOMETRY POINT CHILD CLASSES
#
#########################################################

class CubePoint(GeometryPoint):
    '''
    Geometry Point with the vertices arrange around the central location in form of a cube.
    Child of GeometryPoint.
    '''
    def __init__(self, base_ID = 0,
                location = Vector((0, 0, 0)), thickness = 1.0, side_scaling = Vector((1, 1, 1)),
                illusion_angle_x = radians(54.736), illusion_angle_z = radians(45),
                apply_axonometric_correction = True):
        '''
        See GeometryPoint InitializePoint() description for more details.
        '''
        self.InitializePoint(base_ID, location, thickness, side_scaling,
                            illusion_angle_x, illusion_angle_z,
                            apply_axonometric_correction,
                            axis_alignment = None,
                            point_type = "CUBE")
        self.valid_faces = self.get_ValidFaceList()

    def calculate_Vertex_RelativeLocation(self, thickness, side_scaling, illusion_angle_x, illusion_angle_z, axis_alignment = None):
        '''
        Calculates the 8 vertices forming a cuboid (cube by default)
        ----------
        Inputs:
        Float thickness: Cube size
        Float[3] side_scaling: Factors to rescale the cube into a cuboid
        ----------
        Returns:
        List<Vector[3]> vertex_relative_location: List of Vectors that represent the relative location of the vertex around the GeometryPoint location
        ----------
        The vertex are returned in the following order:
        (X, Y, Z)
        0: (-1, -1, -1)
        1: (-1, -1, 1)
        2: (-1, 1, -1)
        3: (-1, 1, 1)
        4: (1, -1, -1)
        5: (1, -1, 1)
        6: (1, 1, -1)
        7: (1, 1, 1)
        '''
        vertex_relative_location = []
        x_scale, y_scale, z_scale = side_scaling
        for i in [-1,1]:
            for j in [-1,1]:
                for k in [-1,1]:
                    vertex_relative_location.append(Vector((i * x_scale * thickness/2, j * y_scale * thickness/2, k * z_scale * thickness/2)))
        return vertex_relative_location



class PlanePoint(GeometryPoint):
    '''
    Geometry Point with the vertices arrange around the central location in form of an Illusion plane.
    Child of GeometryPoint.
    '''
    def __init__(self, base_ID = 0,
                location = Vector((0, 0, 0)), thickness = 1.0, side_scaling = Vector((1, 1, 1)),
                illusion_angle_x = radians(54.736), illusion_angle_z = radians(45),
                apply_axonometric_correction = True,
                axis_alignment = "Z"):
        self.InitializePoint(base_ID, location, thickness, side_scaling,
                            illusion_angle_x, illusion_angle_z,
                            apply_axonometric_correction,
                            axis_alignment = axis_alignment,
                            point_type = "PLANE")
        self.valid_faces = []

    def calculate_Vertex_RelativeLocation(self, thickness, side_scaling, illusion_angle_x, illusion_angle_z, axis_alignment = "Z"):
        '''
        Returns the 4 vertices around a plane.
        --------------
        Inputs:
        Float thickness: Figure thickness
        Vector[3] side_scaling: Factors to rescale the thickness
        axis_alignment: Axis to which the face normal is aligned (X, Y, Z).
        ----------
        Returns:
        List<Vector[3]> vertex_relative_location: List of Vectors that represent the relative location of the vertex around the GeometryPoint location
        ----------
        The vertex are returned in the following order:
        (X, Y, Z)
        0: (-1, -1, -1)
        1: (-1, -1, 1)
        2: (-1, 1, -1)
        3: (-1, 1, 1)
        4: (1, -1, -1)
        5: (1, -1, 1)
        6: (1, 1, -1)
        7: (1, 1, 1)
        '''
        x_scale, y_scale, z_scale = side_scaling

        # Obtain the vertex locations, relative to the illusion points
        vertex_relative_location = []
        for i in [-1,1]:
            for j in [-1,1]:
                # Plane aligned with the Z axis
                if axis_alignment == 'Z':
                    vertex_relative_location.append(Vector((i * x_scale * thickness/2, j * y_scale * thickness/2, 0.0)))

                # Plane aligned with the X axis
                elif axis_alignment == 'X':
                    vertex_relative_location.append(Vector((0.0, i * y_scale * thickness/2, j * z_scale * thickness/2)))

                # Plane aligned with the Y axis
                elif axis_alignment == 'Y':
                    vertex_relative_location.append(Vector((i * x_scale * thickness/2, 0.0, j * z_scale * thickness/2)))
        return vertex_relative_location



class IllusionPlanePoint(GeometryPoint):
    '''
    Geometry Point with the vertices arrange around the central location in form of an Illusion plane.
    Child of GeometryPoint.
    '''
    def __init__(self, base_ID = 0,
                location = Vector((0, 0, 0)), thickness = 1.0, side_scaling = Vector((1, 1, 1)),
                illusion_angle_x = radians(54.736), illusion_angle_z = radians(45),
                apply_axonometric_correction = True,
                axis_alignment = "Z"):
        self.InitializePoint(base_ID, location, thickness, side_scaling,
                            illusion_angle_x, illusion_angle_z,
                            apply_axonometric_correction,
                            axis_alignment = axis_alignment,
                            point_type = "IPLANE")
        self.valid_faces = []

    def calculate_Vertex_RelativeLocation(self, thickness, side_scaling, illusion_angle_x, illusion_angle_z, axis_alignment = "Z"):
        '''
        Returns the 4 vertices around a plane illusion.
        --------------
        Inputs:
        Float thickness: Figure thickness
        Vector[3] side_scaling: Factors to rescale the thickness
        Float illusion_angle_x: X-Camera Rotation necessary to see the illusion
        Float illusion_angle_z: Z-Camera Rotation necessary to see the illusion

        axis_alignment: Axis to which the face normal is aligned (X, Y, Z).
        ----------
        Returns:
        List<Vector[3]> vertex_relative_location: List of Vectors that represent the relative location of the vertex around the GeometryPoint location
        ----------
        The vertex are returned in the following order:
        (X, Y, Z)
        0: (-1, -1, -1)
        1: (-1, -1, 1)
        2: (-1, 1, -1)
        3: (-1, 1, 1)
        4: (1, -1, -1)
        5: (1, -1, 1)
        6: (1, 1, -1)
        7: (1, 1, 1)
        '''
        x_scale, y_scale, z_scale = side_scaling

        # Get the displacement required to align the plane with the line of sight
        illusion_correction, illusion_orientation = self.get_IllusionCorrection(thickness, side_scaling, illusion_angle_x, illusion_angle_z, axis_alignment)

        # Obtain the vertex locations, relative to the illusion points
        vertex_relative_location = []
        for i in [-1,1]:
            for j in [-1,1]:
                # Plane aligned with the Z axis
                if axis_alignment == 'Z':
                    # Set the direction of the correction according to the orientation
                    if illusion_orientation == "D":
                        if i*j == -1:
                            sign = i
                        else:
                            sign = 0.
                    elif illusion_orientation == "X":
                        sign = -j
                    elif illusion_orientation == "Y":
                        sign = i
                    vertex_relative_location.append(Vector((i * x_scale * thickness/2, j * y_scale * thickness/2, sign * illusion_correction)))

                # Plane aligned with the X axis
                elif axis_alignment == 'X':
                    # Set the direction of the correction according to the orientation
                    if illusion_orientation == 'H':
                        sign = j
                    elif illusion_orientation == "V":
                        sign = -i
                    vertex_relative_location.append(Vector((sign * illusion_correction, i * y_scale * thickness/2, j * z_scale * thickness/2)))

                # Plane aligned with the Y axis
                elif axis_alignment == 'Y':
                    # Set the direction of the correction according to the orientation
                    if illusion_orientation == 'H':
                        sign = -j
                    elif illusion_orientation == "V":
                        sign = -i
                    vertex_relative_location.append(Vector((i * x_scale * thickness/2, sign * illusion_correction, j * z_scale * thickness/2)))
        return vertex_relative_location


class IllusionCubePoint(GeometryPoint):
    '''
    Geometry Point with the vertices arrange around the central location in form of an Illusion Cube.
    Child of GeometryPoint.
    '''
    def __init__(self, base_ID = 0,
                location = Vector((0, 0, 0)), thickness = 1.0, side_scaling = Vector((1, 1, 1)),
                illusion_angle_x = radians(54.736), illusion_angle_z = radians(45),
                apply_axonometric_correction = True,
                axis_alignment = "Z+"):
        self.InitializePoint(base_ID, location, thickness, side_scaling,
                            illusion_angle_x, illusion_angle_z,
                            apply_axonometric_correction,
                            axis_alignment = axis_alignment,
                            point_type = "ICUBE")
        self.valid_faces = self.get_ValidFaceList()
        self.remove_ValidFace(axis_alignment)

    def calculate_Vertex_RelativeLocation(self, thickness, side_scaling, illusion_angle_x, illusion_angle_z, axis_alignment = "Z+"):
        '''
        Returns the vertex around a half-cube illusion.
        --------------
        Inputs:
        Float thickness: Figure thickness
        Vector[3] side_scaling: Factors to rescale the thickness
        Float illusion_angle_x: X-Camera Rotation necessary to see the illusion
        Float illusion_angle_z: Z-Camera Rotation necessary to see the illusion

        axis_alignment: Axis to which the cube Illusion normal is aligned (X-, X+, Y-, Y+, Z-, Z+).
        Depending on the orientation the cube can be the half Left, Right, Back, Front, Down, Up.
        ----------
        Returns:
        List<Vector[3]> vertex_relative_location: List of Vectors that represent the relative location of the vertex around the GeometryPoint location
        ----------
        The vertex are returned in the following order:
        (X, Y, Z)
        0: (-1, -1, -1)
        1: (-1, -1, 1)
        2: (-1, 1, -1)
        3: (-1, 1, 1)
        4: (1, -1, -1)
        5: (1, -1, 1)
        6: (1, 1, -1)
        7: (1, 1, 1)
        '''
        x_scale, y_scale, z_scale = side_scaling
        #Correction for the illusion plane in the illusion cube. Valid only for the x axis
        #illusion_correction = z_scale * thick / 2

        illusion_correction, illusion_orientation = self.get_IllusionCorrection(thickness, side_scaling, illusion_angle_x, illusion_angle_z, axis_alignment[0])

        # A regular cube has i, j, k from -1, 1.
        i_min = -1
        i_max = 1

        j_min = -1
        j_max = 1

        k_min = -1
        k_max = 1

        # Find out which half of the illusion cube is being constructed
        # The axis alignment defines in which direction the illusion is pointing.
        # A half cube has one of its values i, j, k values set to 0
        if axis_alignment == "X+":
            # Correspond to the left half of X oriented block
            i_max = 0
        elif axis_alignment == "X-":
            # Correspond to the right half of X oriented block
            i_min = 0

        elif axis_alignment == "Y+":
            # Correspond to the back half of Y oriented block
            j_max = 0
        elif axis_alignment == "Y-":
            # Correspond to the front (up) half of Y oriented block
            j_min = 0

        elif axis_alignment == "Z+":
            # Correspond to the bottom half of Z oriented block
            k_max = 0
        elif axis_alignment == "Z-":
            # Correspond to the top half of Z oriented block
            k_min = 0


        vertex_relative_location = []
        for i in [i_min, i_max]:
            for j in [j_min, j_max]:
                for k in [k_min, k_max]:
                    # Location of the vertex in the illusion plane (Z - alignment)
                    if k == 0 and i*j == -1:
                        sign = i
                        vertex_relative_location.append(Vector((i * x_scale * thickness/2, j * y_scale * thickness/2, sign * illusion_correction)))

                    # Location of the vertex in the illusion plane (Y - alignment)
                    elif j == 0:
                        if illusion_orientation == "H":
                            sign = -k
                        elif illusion_orientation == "V":
                            sign = -i
                        vertex_relative_location.append(Vector((i * x_scale * thickness/2, sign * illusion_correction, k * z_scale * thickness/2)))

                    # Location of the vertex in the illusion plane (X - alignment)
                    elif i == 0:
                        if illusion_orientation == "H":
                            sign = k
                        elif illusion_orientation == "V":
                            sign = -j
                        vertex_relative_location.append(Vector((sign * illusion_correction, j * y_scale * thickness/2, k * z_scale * thickness/2)))

                    # Location of the vertex in a standard cube
                    else:
                        vertex_relative_location.append(Vector((i * x_scale * thickness/2, j * y_scale * thickness/2, k * z_scale * thickness/2)))
        return vertex_relative_location


#########################################################
#
#   GEOMETRY EDGE CLASS
#
#########################################################

class GeometryEdge(GeometryAppendOperations, GeometryFaceOperations):
    '''
    Geometry Object that represent the connection between two GeometryPoint objects
    It is used to construct the faces in between the different points.

    It inherits basic functions from the classes GeometryAppendOperations and GeometryFaceOperations
    '''
    def __init__(self,  point_A, point_B):
        '''
        GeometryPoint Point_A: Starting point of the GeometryEdge
        GeometryPoint Point_B: Ending point of the GeometryEdge
        '''

        # Assign point_A and point_B
        self.point_A = point_A
        self.point_B = point_B


        # Use the locations of point_A and point_B to determine the axis alignment
        axis_alignment = self.calculate_AxisAlignment()

        # Determine which of the vertex in point_A and point_B belong to the edge
        self.vertex_Ids = self.get_Vertex_EdgeIds(axis_alignment)

        # Get the valid faces of the edge
        self.valid_faces = self.get_ValidFaceList()
        self.remove_EdgeFaces(axis_alignment)


    def calculate_AxisAlignment(self):
        '''
        Determines the alignment of GeometryEdge using the GeometryPoint A and B locations.
        The orientation is defined as "Going from A to B"
        -----------
        Returns:
        axis_alignment: X+, X-, Y+, Y-, Z+, Z-.
        '''
        axis_alignment = ""

        loc_A = self.point_A.location
        loc_B = self.point_B.location

        # Calculate the distance in each axis
        x_distance = abs(loc_B[0] - loc_A[0])
        y_distance = abs(loc_B[1] - loc_A[1])
        z_distance = abs(loc_B[2] - loc_A[2])
        coordinate_index = 0

        # Find which axis contains the largest separation between the points A and B
        if x_distance >= y_distance and x_distance >= z_distance:
            axis_alignment = "X"
            coordinate_index = 0
        if y_distance >= x_distance and y_distance >= z_distance:
            axis_alignment = "Y"
            coordinate_index = 1
        if z_distance >= x_distance and z_distance >= y_distance:
            axis_alignment = "Z"
            coordinate_index = 2

        # Find the direction in which A and B are oriented (positive or negative)
        if loc_B[coordinate_index] - loc_A[coordinate_index] >= 0 :
            axis_alignment += "+"
        else:
            axis_alignment += "-"

        return axis_alignment



    def get_Vertex_EdgeIds(self, axis_alignment):
        '''
        Determines the 8 vertex that define the edge faces based on the points A and B, and the axis alignment.
        ---------
        Returns:
        vertex_Ids: 8 Ids of the points A and B that define a cuboid (in this case the GeometryEdge). The Ids are returned in the cubic construction order.
        '''
        point_A = self.point_A
        point_B = self.point_B

        a_id = point_A.vertex_Ids
        b_id = point_B.vertex_Ids

        vertex_Ids = []

        # Determine the type of connection based on the GeometryPoint Types
        bool_TwoCubes = (point_A.point_type == "CUBE" or point_A.point_type == "ICUBE") and (point_B.point_type == "CUBE" or point_B.point_type == "ICUBE")
        bool_CubePlane = (point_A.point_type == "CUBE" or point_A.point_type == "ICUBE") and (point_B.point_type == "PLANE" or point_B.point_type == "IPLANE")
        bool_PlaneCube = (point_B.point_type == "CUBE" or point_B.point_type == "ICUBE") and (point_A.point_type == "PLANE" or point_A.point_type == "IPLANE")
        bool_PlanePlane = (point_A.point_type == "PLANE" or point_A.point_type == "IPLANE") and (point_B.point_type == "PLANE" or point_B.point_type == "IPLANE")


        if bool_TwoCubes:
            # CUBE-CUBE connection
            if axis_alignment == "X+":
                vertex_Ids = [a_id[4], a_id[5], a_id[6],a_id[7], b_id[0], b_id[1], b_id[2], b_id[3]]
            if axis_alignment == "X-":
                vertex_Ids = [b_id[4], b_id[5], b_id[6],b_id[7], a_id[0], a_id[1], a_id[2], a_id[3]]

            if axis_alignment == "Y+":
                vertex_Ids = [a_id[2], a_id[3], b_id[0], b_id[1], a_id[6], a_id[7], b_id[4], b_id[5]]
            if axis_alignment == "Y-":
                vertex_Ids = [b_id[2], b_id[3], a_id[0], a_id[1], b_id[6], b_id[7], a_id[4], a_id[5]]

            if axis_alignment == "Z+":
                vertex_Ids = [a_id[1], b_id[0], a_id[3], b_id[2], a_id[5], b_id[4], a_id[7], b_id[6]]
            if axis_alignment == "Z-":
                vertex_Ids = [b_id[1], a_id[0], b_id[3], a_id[2], b_id[5], a_id[4], b_id[7], a_id[6]]

        if bool_CubePlane:
            # CUBE-PLANE connection
            if axis_alignment == "X+":
                vertex_Ids = [a_id[4], a_id[5], a_id[6],a_id[7], b_id[0], b_id[1], b_id[2], b_id[3]]
            if axis_alignment == "X-":
                vertex_Ids = [b_id[0], b_id[1], b_id[2],b_id[3], a_id[0], a_id[1], a_id[2], a_id[3]]

            if axis_alignment == "Y+":
                vertex_Ids = [a_id[2], a_id[3], b_id[0], b_id[1], a_id[6], a_id[7], b_id[2], b_id[3]]
            if axis_alignment == "Y-":
                vertex_Ids = [b_id[0], b_id[1], a_id[0], a_id[1], b_id[2], b_id[3], a_id[4], a_id[5]]

            if axis_alignment == "Z+":
                vertex_Ids = [a_id[1], b_id[0], a_id[3], b_id[1], a_id[5], b_id[2], a_id[7], b_id[3]]
            if axis_alignment == "Z-":
                vertex_Ids = [b_id[0], a_id[0], b_id[1], a_id[2], b_id[2], a_id[4], b_id[3], a_id[6]]

        if bool_PlaneCube:
            # PLANE-CUBE connection
            if axis_alignment == "X+":
                vertex_Ids = [a_id[0], a_id[1], a_id[2],a_id[3], b_id[0], b_id[1], b_id[2], b_id[3]]
            if axis_alignment == "X-":
                vertex_Ids = [b_id[4], b_id[5], b_id[6],b_id[7], a_id[0], a_id[1], a_id[2], a_id[3]]

            if axis_alignment == "Y+":
                vertex_Ids = [a_id[0], a_id[1], b_id[0], b_id[1], a_id[2], a_id[3], b_id[4], b_id[5]]
            if axis_alignment == "Y-":
                vertex_Ids = [b_id[2], b_id[3], a_id[0], a_id[1], b_id[6], b_id[7], a_id[2], a_id[3]]

            if axis_alignment == "Z+":
                vertex_Ids = [a_id[0], b_id[0], a_id[1], b_id[2], a_id[2], b_id[4], a_id[3], b_id[6]]
            if axis_alignment == "Z-":
                vertex_Ids = [b_id[1], a_id[0], b_id[3], a_id[1], b_id[5], a_id[2], b_id[7], a_id[3]]

        if bool_PlanePlane:
            # PLANE-PLANE connection
            if axis_alignment == "X+":
                vertex_Ids = [a_id[0], a_id[1], a_id[2],a_id[3], b_id[0], b_id[1], b_id[2], b_id[3]]
            if axis_alignment == "X-":
                vertex_Ids = [b_id[0], b_id[1], b_id[2],b_id[3], a_id[0], a_id[1], a_id[2], a_id[3]]

            if axis_alignment == "Y+":
                vertex_Ids = [a_id[0], a_id[1], b_id[0], b_id[1], a_id[2], a_id[3], b_id[2], b_id[3]]
            if axis_alignment == "Y-":
                vertex_Ids = [b_id[0], b_id[1], a_id[0], a_id[1], b_id[2], b_id[3], a_id[2], a_id[3]]

            if axis_alignment == "Z+":
                vertex_Ids = [a_id[0], b_id[0], a_id[1], b_id[1], a_id[2], b_id[2], a_id[3], b_id[3]]
            if axis_alignment == "Z-":
                vertex_Ids = [b_id[0], a_id[0], b_id[1], a_id[1], b_id[2], a_id[2], b_id[3], a_id[3]]

        return vertex_Ids

    def remove_EdgeFaces(self, axis_alignment):
        '''
        Use the axis alignment to remove the connecting faces from GeometryEdge, and from point_A and point_B
        '''
        # Remove the faces from the Edge
        self.remove_ValidFace(axis_alignment[0]+"+")
        self.remove_ValidFace(axis_alignment[0]+"-")

        # Remove the faces from the Points
        if axis_alignment[1] == "+":
            self.point_A.remove_ValidFace(axis_alignment[0] + "+")
            self.point_B.remove_ValidFace(axis_alignment[0] + "-")

        if axis_alignment[1] == "-":
            self.point_A.remove_ValidFace(axis_alignment[0] + "-")
            self.point_B.remove_ValidFace(axis_alignment[0] + "+")
