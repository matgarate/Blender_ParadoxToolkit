import bpy
from math import *
from mathutils import *

#########################################################
#
#   UTILITIES TO LINK PARAMETERS WITH OBJECT CREATION
#
#########################################################

def get_IllusionAngles(illusion_alignment, axonometric_angles_xz, camera = None, report = None):
    '''
    Gets the camera angle required to set the illusion based on the chosen alignment.

    axonometric_angles_xz[2]: input angles from the user if the Axonometric option was selected
    camera: Blender Camera Object.
    illusion_alignment: option to determine which angles must be used as illusion angles
    0: Isometric
    1: Axonometric
    2: Camera
    '''

    # Isometric Perspective
    if illusion_alignment == '0':
        illusion_angle_z = radians(45.)
        illusion_angle_x = radians(54.736)

    # Axonometric Perspective (Angles are already given in radians)
    elif illusion_alignment == '1':
        illusion_angle_x = axonometric_angles_xz[0]
        illusion_angle_z = axonometric_angles_xz[1]

    # Camera Perspective
    elif illusion_alignment == '2':
        if check_ValidCamera(camera):
            # Check if there is a camera object to read the rotation from.
            illusion_angle_x = camera.rotation_euler[0]
            illusion_angle_z = camera.rotation_euler[2]
        else:
            # If there is no camera then return the Isometric angle
            illusion_angle_z = radians(45.)
            illusion_angle_x = radians(54.736)

            if report is not None:
                report({'WARNING'}, "Camera not found. Isometric perspective will be used.")

    return illusion_angle_x, illusion_angle_z


def add_Mesh(context, name, verts, faces):
    '''
    Add the new mesh object to the scene.

    name
    verts[]: List of Locations. Each location is a 3D-vector or 3-tuples
    faces[]: List of faces. Each face is a list of 4 vertex index.
    '''
    mesh_data = bpy.data.meshes.new(name)       # Create new mesh data
    mesh_data.from_pydata(verts, [], faces)     # Create vertex and faces
    mesh_object = bpy.data.objects.new(name, mesh_data) # Create a new blender object and assign the mesh data
    context.collection.objects.link(mesh_object)        # Link object collection
    context.view_layer.objects.active = mesh_object     # Set object as active

    mesh_object.location = context.scene.cursor.location    # Position object at cursor

    # Deselect all objects and select the new object
    bpy.ops.object.select_all(action='DESELECT')
    mesh_object.select_set(True)
    return mesh_object

def save_CustomProperties(mesh_object, illusion_angle_x, illusion_angle_z, bool_illusion_object = True):
    '''
    Creates a custom property for the illusion angles.
    Marks if the object is a continuous illusion.
    -------------
    mesh_object: Blender object added by the construct_geometry operators

    illusion_angle_x: Camera rotation X used to define the axonometric proportion
    illusion_angle_z: Camera rotation Z used to define the axonometric proportion

    bool_illusion_object: Boolean to indicate if the mesh object is an illusion object
    '''
    mesh_object["IllusionAngles"] = [illusion_angle_x, illusion_angle_z]
    mesh_object["bool_IllusionObject"] = bool_illusion_object



def assign_IllusionVertexGroups(mesh_object, groups):
    '''
    Assigns the vertex groups to the object.
    Used to mark the illusion planes which are used then by the IllusionTools operators
    '''
    if type(groups) == list:
        for group_name, group_vertices in groups:
            new_group = mesh_object.vertex_groups.new(name = group_name)
            new_group.add(group_vertices, 1.0, "ADD")




def get_Illusion_LocationNormals(illusion_object):
    '''
    Returns the location and normal of the vertex groups names as "IllusionFront" and "IllusionBack"
    '''
    # Indexes of the illusion vertex groups
    illusion_groups_index = [illusion_object.vertex_groups['IllusionFront'].index, illusion_object.vertex_groups['IllusionBack'].index]

    ############################################
    # Iterate over the illusion groups to get their locations
    ############################################

    illusion_location = [] # List of positions of each illusion
    illusion_normals = []

    for illusion_ID in illusion_groups_index:

        # Get the vertex that belong to each vertex group
        illusion_vertices = []

        # Iterate over the vertex in the illusion object
        for vertex in illusion_object.data.vertices:
            # Check if the illusion_ID is among the group IDs associated to that vertex
            if illusion_ID not in [vertex_group.group for vertex_group in vertex.groups]:
                continue
            # Check that the weight of that vertex in the current illusion groups is 1.0
            if illusion_object.vertex_groups[illusion_ID].weight(vertex.index) != 1:
                continue
            # Append the vertex associated to the illusion group with weight 1.0
            illusion_vertices.append(vertex)




        # Find the average position of the illusion.
        illusion_location.append(Vector((0,0,0)))
        for vertex in illusion_vertices:
            # Get the global location of the vertex
            vertex_loc = illusion_object.matrix_world @ vertex.co

            illusion_location[-1] += vertex_loc
        illusion_location[-1] /= len(illusion_vertices)


        #Assuming that the vertex are given in the construction order
        vector_a = (illusion_object.matrix_world @ illusion_vertices[2].co) - (illusion_object.matrix_world @ illusion_vertices[0].co)
        vector_b = (illusion_object.matrix_world @ illusion_vertices[1].co) - (illusion_object.matrix_world @ illusion_vertices[0].co)

        illusion_normals.append(vector_a.cross(vector_b).normalized())

    return illusion_location, illusion_normals



def align_CameraObject(camera, align_camera_object, mesh_object, illusion_angle_x, illusion_angle_z, tilt_angle, camera_distance = 15., report = None):
    '''
    Align the camera-to-object, the object-to-camera, and/or tilt the object around camera line of sight
    ------------
    camera: Blender Camera Object. This function assumes that the camera object was checked in advance.
    align_camera_object: options to align [0: None, 1: Camera-to-Object, 2: Object-to-Camera]
    mesh_object: object to align the camera at.

    illusion_angle_x: Camera rotation X used to define the axonometric proportion
    illusion_angle_z: Camera rotation Z used to define the axonometric proportion

    tilt_angle: rotation around the camera local z-axis
    camera_distance: distance to reposition the camera from the object.
    '''

    # Align Camera to Object
    if align_camera_object == '1':
        # Adjust the camera to match the illusion angle of the object.
        # Adjust the distance to the object as well
        target_rotation = (illusion_angle_x, 0.0, illusion_angle_z)
        target_direction = Vector((sin(illusion_angle_x) * cos(illusion_angle_z - pi/2.),
                                  sin(illusion_angle_x) * sin(illusion_angle_z - pi/2.),
                                  cos(illusion_angle_x)))
        target_location = target_direction * camera_distance + mesh_object.location

        camera.rotation_euler = target_rotation
        camera.location = target_location


    # Align Object to Camera
    elif align_camera_object == '2':
        # Reset the object rotation to zero
        mesh_object.rotation_euler = (0, 0, 0)

        # Reset the camera y rotation to zero
        if camera.rotation_euler[1] != 0.0 and report is not None:
            report({'WARNING'}, "Camera Y rotation will be set to 0.")
        camera.rotation_euler[1] = 0.0

        # Align the object with the camera along the azimuth
        mesh_object.rotation_euler[2] = camera.rotation_euler[2] - illusion_angle_z

        # Rotate the camera along the X-Axis of the camera view
        bpy.ops.transform.rotate(
            value = camera.rotation_euler[0] -  illusion_angle_x,
            orient_axis = 'X',
            orient_matrix = camera.rotation_euler.to_matrix())

    # Tilt object around camera local Z axis
    if tilt_angle != 0.0:
        bpy.ops.transform.rotate(
            value = tilt_angle,
            orient_axis = 'Z',
            orient_matrix = camera.rotation_euler.to_matrix())





def check_ValidProperty_IllusionObject(mesh_object, report = None):
    '''
    Checks if a mesh_object has the bool_IllusionObject property, and checks that it is marked as True.
    '''

    try:
        # Look for the bool_IllusionObject Property
        bool_illusion_object = mesh_object["bool_IllusionObject"]
    except (KeyError, TypeError):
        # Key: catch the exception when the object does not has that property
        # Type: Catch the case when no active object is seleceted, i.e. mesh_object = None
        if report is not None:
            if mesh_object is not None:
                report({'ERROR'}, "Active Object is not an illusion object.")
            else:
                report({'ERROR'}, "No Active Object Detected.")
        return False

    if not bool_illusion_object:
        report({'ERROR'}, "Active object cannot be used for illusion operations.")
        return False

    return True


def check_ValidCamera(camera, check_otrographic = True, report = None):
    '''
    Checks if the camera object is okay.
    Print warnings if the camera is not ortographic, or has a y_rotation
    '''
    if camera is None:
        if report is not None:
            report({'ERROR'}, "Camera not found.")
        return False
    if camera.data.type != 'ORTHO' and check_otrographic:
        if report is not None:
            report({'WARNING'}, "Camera is not ortographic.")
    return True
