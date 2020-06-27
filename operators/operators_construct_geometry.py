import bpy
from bpy.props import *

from math import *
from mathutils import *




#########################################################
#
#   GENERATE GEOMETRY OPERATORS
#
#########################################################

from . geometry_mesh_library import *

from . common_operator_properties import GeometryProperties, IllusionAlignmentProperties, RelativeCameraAlignmentProperties
from . common_operator_functions import add_Mesh, save_CustomProperties, assign_IllusionVertexGroups
from . common_operator_functions import get_IllusionAngles, align_CameraObject, check_ValidCamera

from . draw_operator_boxes import draw_Geometry_Box, draw_IllusionAlignment_Box, draw_RelativeAlignment_Box

#########################################################
#
#   PENROSE TRIANGLE
#
#########################################################

class PARADOX_OT_construct_penrose_triangle(bpy.types.Operator, GeometryProperties, IllusionAlignmentProperties, RelativeCameraAlignmentProperties):
    bl_idname = "object.paradox_construct_penrose_triangle"
    bl_label = "Penrose Triangle"
    bl_description = "Construct a Penrose Triangle"
    # bl_space_type = ""
    # bl_region_type = ""
    bl_options = {'REGISTER', 'UNDO'}

    #########################################################
    #
    #   PROPERTIES
    #
    #########################################################

    block_checkbox: BoolProperty(
        name = "Block Variant",
        description = "Construct a triangle using blocks.",
        default = False
    )

    def draw(self, context):
        layout = self.layout

        draw_Geometry_Box(self)
        draw_RelativeAlignment_Box(self)
        draw_IllusionAlignment_Box(self)

        box = layout.box()
        row = box.row()
        row.label(text = "Extra Options")
        row = box.row()
        row.prop(self, "block_checkbox", expand = False)

    def execute(self, context):

        # Get the camera angle required for the illusion
        illusion_angle_x, illusion_angle_z = get_IllusionAngles(self.illusion_alignment, self.axonometric_angles_xz, context.scene.camera, report = self.report)

        # Construct the object and add it to the scene
        # Constructe either the continuous or block variant
        if self.block_checkbox:
            verts, faces, groups = penrose_triangle_block(
                                    self.size_value,
                                    self.thickness_value,
                                    self.side_scaling,
                                    illusion_angle_x,
                                    illusion_angle_z
                                    )
        else:
            verts, faces, groups = penrose_triangle(
                                    self.size_value,
                                    self.thickness_value,
                                    self.side_scaling,
                                    illusion_angle_x,
                                    illusion_angle_z
                                    )
        mesh_object = add_Mesh(context, "Penrose", verts, faces)
        save_CustomProperties(mesh_object, illusion_angle_x, illusion_angle_z)
        assign_IllusionVertexGroups(mesh_object, groups)

        # Re-Align the object respect to the camera
        camera_distance = 3*self.size_value
        if check_ValidCamera(context.scene.camera):
            align_CameraObject(context.scene.camera, self.align_camera_object, mesh_object, illusion_angle_x, illusion_angle_z, self.tilt_angle, camera_distance = camera_distance, report = self.report)

        return {'FINISHED'}

#########################################################
#
#   REUTERSVARD RECTANGLE
#
#########################################################


class PARADOX_OT_construct_reutersvard_rectangle(bpy.types.Operator, GeometryProperties, IllusionAlignmentProperties, RelativeCameraAlignmentProperties):
    bl_idname = "object.paradox_construct_reutersvard_rectangle"
    bl_label = "Reutersvard Rectangle"
    bl_description = "Construct a Reutersvard Rectangle"
    # bl_space_type = ""
    # bl_region_type = ""
    bl_options = {'REGISTER', 'UNDO'}

    #########################################################
    #
    #   PROPERTIES
    #
    #########################################################
    height_value : FloatProperty(
        name = "Height",
        description = "Height",
        default = 10.0,
        min = 0.1,
        max = 100.0,
        unit = "LENGTH"
    )
    width_value : FloatProperty(
        name = "Width",
        description = "Width",
        default = 6.0,
        min = 0.1,
        max = 100.0,
        unit = "LENGTH"
    )


    def draw(self, context):
        layout = self.layout

        geometry_params = [["Height", "height_value"], ["Width", "width_value"]]
        draw_Geometry_Box(self, geometry_params)
        draw_RelativeAlignment_Box(self)
        draw_IllusionAlignment_Box(self)

    def execute(self, context):

        # Get the camera angle required for the illusion
        illusion_angle_x, illusion_angle_z = get_IllusionAngles(self.illusion_alignment, self.axonometric_angles_xz, context.scene.camera, report = self.report)

        # Construct the object and add it to the scene
        verts, faces, groups = reutersvard_rectangle(
                                self.height_value,
                                self.width_value,
                                self.thickness_value,
                                self.side_scaling,
                                illusion_angle_x,
                                illusion_angle_z
                                )
        mesh_object = add_Mesh(context, "Rectangle", verts, faces)
        save_CustomProperties(mesh_object, illusion_angle_x, illusion_angle_z)
        assign_IllusionVertexGroups(mesh_object, groups)

        # Re-Align the object respect to the camera
        camera_distance = 2.* sqrt(self.height_value**2 + self.width_value**2)
        if check_ValidCamera(context.scene.camera):
            align_CameraObject(context.scene.camera, self.align_camera_object, mesh_object, illusion_angle_x, illusion_angle_z, self.tilt_angle, camera_distance = camera_distance, report = self.report)

        return {'FINISHED'}

#########################################################
#
#   IMPOSSIBLE ARCH
#
#########################################################


class PARADOX_OT_construct_impossible_arch(bpy.types.Operator, GeometryProperties, IllusionAlignmentProperties, RelativeCameraAlignmentProperties):
    bl_idname = "object.paradox_construct_impossible_arch"
    bl_label = "Impossible Arch"
    bl_description = "Construct an Impossible Arch"
    # bl_space_type = ""
    # bl_region_type = ""
    bl_options = {'REGISTER', 'UNDO'}

    #########################################################
    #
    #   PROPERTIES
    #
    #########################################################

    height_value : FloatProperty(
        name = "Height",
        description = "Height",
        default = 12.0,
        min = 0.1,
        max = 100.0,
        unit = "LENGTH"
    )
    width_values: FloatVectorProperty(
        name = "Width",
        description = "Width",
        default = (4.0, 4.0),
        min = 0.1,
        max = 100.0,
        size = 2,
        unit = "LENGTH"
    )


    def draw(self, context):
        layout = self.layout

        geometry_params = [["Height", "height_value"], ["Width", "width_values"]]
        draw_Geometry_Box(self, geometry_params)
        draw_RelativeAlignment_Box(self)
        draw_IllusionAlignment_Box(self)

    def execute(self, context):

        # Get the camera angle required for the illusion
        illusion_angle_x, illusion_angle_z = get_IllusionAngles(self.illusion_alignment, self.axonometric_angles_xz, context.scene.camera, report = self.report)

        # Construct the object and add it to the scene
        verts, faces, groups = impossible_arch(
                                self.height_value,
                                self.width_values[0],
                                self.width_values[1],
                                self.thickness_value,
                                self.side_scaling,
                                illusion_angle_x,
                                illusion_angle_z
                                )
        mesh_object = add_Mesh(context, "Arch", verts, faces)
        save_CustomProperties(mesh_object, illusion_angle_x, illusion_angle_z)
        assign_IllusionVertexGroups(mesh_object, groups)

        # Re-Align the object respect to the camera
        camera_distance = 2.* sqrt(self.height_value**2 + self.width_values[0]**2)
        if check_ValidCamera(context.scene.camera):
            align_CameraObject(context.scene.camera, self.align_camera_object, mesh_object, illusion_angle_x, illusion_angle_z, self.tilt_angle, camera_distance = camera_distance, report = self.report)

        return {'FINISHED'}


#########################################################
#
#   IMPOSSIBLE CUBE
#
#########################################################

class PARADOX_OT_construct_impossible_cube(bpy.types.Operator, GeometryProperties, RelativeCameraAlignmentProperties):
    bl_idname = "object.paradox_construct_impossible_cube"
    bl_label = "Impossible Cube"
    bl_description = "Construct an Isometric Impossible Cube"
    # bl_space_type = ""
    # bl_region_type = ""
    bl_options = {'REGISTER', 'UNDO'}

    #########################################################
    #
    #   PROPERTIES
    #
    #########################################################


    def draw(self, context):
        layout = self.layout

        draw_Geometry_Box(self)
        draw_RelativeAlignment_Box(self)

    def execute(self, context):

        # Get the camera angle required for the illusion
        illusion_angle_x = radians(54.736)
        illusion_angle_z = radians(45.)

        # Rearrange the side_scaling because the object will be rotated later
        sorted_side_scaling  = Vector((self.side_scaling[1], self.side_scaling[2], self.side_scaling[0]))

        # Construct the object and add it to the scene
        verts, faces, groups = impossible_cube(
                                self.size_value,
                                self.thickness_value,
                                sorted_side_scaling,
                                illusion_angle_x,
                                illusion_angle_z
                                )
        mesh_object = add_Mesh(context, "Cube", verts, faces)
        save_CustomProperties(mesh_object, illusion_angle_x, illusion_angle_z)
        assign_IllusionVertexGroups(mesh_object, groups)

        # The object is easier to construct with another alignment
        # Here we de-rotate it to take its default shape
        bpy.ops.transform.rotate(
            value = radians(240.),
            orient_axis = 'Z',
            orient_matrix = Euler((illusion_angle_x, 0, illusion_angle_z), 'XYZ') .to_matrix())
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        # Re-Align the object respect to the camera
        camera_distance = 2.5* self.size_value
        if check_ValidCamera(context.scene.camera):
            align_CameraObject(context.scene.camera, self.align_camera_object, mesh_object, illusion_angle_x, illusion_angle_z, self.tilt_angle, camera_distance = camera_distance, report = self.report)


        return {'FINISHED'}



#########################################################
#
#   PENROSE STAIR
#
#########################################################

class PARADOX_OT_construct_penrose_stair(bpy.types.Operator, GeometryProperties, IllusionAlignmentProperties, RelativeCameraAlignmentProperties):
    bl_idname = "object.paradox_construct_penrose_stair"
    bl_label = "Penrose Stair"
    bl_description = "Construct a Penrose Stair"
    # bl_space_type = ""
    # bl_region_type = ""
    bl_options = {'REGISTER', 'UNDO'}

    #########################################################
    #
    #   PROPERTIES
    #
    #########################################################
    thickness_value : FloatProperty(
        name = "Thickness",
        description = "Thickness",
        default = 2.5,
        min = 0.02,
        max = 40.0,
        unit = "LENGTH"
    )
    # Additional Scale Controls
    side_scaling : FloatVectorProperty(
        name = "Thickness Scaling",
        description = "Thickness scaling in each direction",
        default = (1.0, 1.0, 0.75),
        min = 0.01,
        max = 2.0
    )

    def draw(self, context):
        layout = self.layout

        draw_Geometry_Box(self)
        draw_RelativeAlignment_Box(self)
        draw_IllusionAlignment_Box(self)


    def execute(self, context):

        # Get the camera angle required for the illusion
        illusion_angle_x, illusion_angle_z = get_IllusionAngles(self.illusion_alignment, self.axonometric_angles_xz, context.scene.camera, report = self.report)

        # Construct the object and add it to the scene
        verts, faces, groups = penrose_stair(
                                self.size_value,
                                self.thickness_value,
                                self.side_scaling,
                                illusion_angle_x,
                                illusion_angle_z
                                )
        mesh_object = add_Mesh(context, "Stair", verts, faces)
        save_CustomProperties(mesh_object, illusion_angle_x, illusion_angle_z)
        assign_IllusionVertexGroups(mesh_object, groups)

        # Re-Align the object respect to the camera
        camera_distance = 3.* self.size_value
        if check_ValidCamera(context.scene.camera):
            align_CameraObject(context.scene.camera, self.align_camera_object, mesh_object, illusion_angle_x, illusion_angle_z, self.tilt_angle, camera_distance = camera_distance, report = self.report)

        return {'FINISHED'}














