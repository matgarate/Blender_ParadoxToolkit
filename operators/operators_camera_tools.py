import bpy
from bpy.props import *
from math import *
from mathutils import *



#########################################################
#
#   CREATE CAMERA
#
#########################################################

from . common_operator_properties import IllusionAlignmentProperties
from . draw_operator_boxes import draw_IllusionAlignment_Box
from . common_operator_functions import get_IllusionAngles, align_CameraObject, check_ValidProperty_IllusionObject, check_ValidCamera

class PARADOX_OT_add_axonometric_camera(bpy.types.Operator, IllusionAlignmentProperties):
    bl_idname = "object.paradox_add_axonometric_camera"
    bl_label = "Axonometric Camera"
    bl_description = "Add an axonometric camera"
    # bl_space_type = ""
    # bl_region_type = ""
    bl_options = {'REGISTER', 'UNDO'}

    #########################################################
    #
    #   PROPERTIES
    #
    #########################################################

    ortho_scale : FloatProperty(
        name = "Orthographic Scale",
        description = "Orthographic scale",
        default = 30.0,
        min = 0.01,
        max = 3000.0
    )
    set_active_camera : BoolProperty(
        name = "Set Active Camera",
        description = "Set new camera as active camera",
        default = True
    )

    # Replace the default illusion alignment with a reduced version.
    illusion_alignment : EnumProperty(
        items=(('0', 'Isometric', 'Set isometric perspective'),
                ('1', 'Axonometric', 'Set X, Z perspective angles')),
        name = "Illusion Alignment",
        description = "Camera Perspective required to see the illusion"
    )

    def draw(self, context):
        layout = self.layout

        box = layout.box()

        row = box.row()
        row.label(text = "Camera Parameters")

        row = box.row()
        row.prop(self, "set_active_camera", expand = False)

        row = box.row()
        row.label(text = "Orthogonal Scale")
        row.prop(self, "ortho_scale", expand = True, text ="")


        draw_IllusionAlignment_Box(self, title = "Camera Alignment")

    def execute(self, context):

        #########################################################
        #
        #   CAMERA ALIGNMENT
        #
        #########################################################

        illusion_angle_x, illusion_angle_z = get_IllusionAngles(self.illusion_alignment, self.axonometric_angles_xz)

        distance = 25
        target_location = (distance * sin(illusion_angle_x) * sin(illusion_angle_z), -distance * sin(illusion_angle_x) * cos(illusion_angle_z), distance * cos(illusion_angle_x))
        target_rotation = (illusion_angle_x, 0, illusion_angle_z)

        #########################################################
        #
        #   CREATE CAMERA
        #
        #########################################################

        bpy.ops.object.camera_add(
            enter_editmode=False,
            align='VIEW',
            location= target_location,
            rotation= target_rotation)

        context.object.data.type = 'ORTHO'
        bpy.context.object.data.ortho_scale = self.ortho_scale

        if self.set_active_camera:
            bpy.ops.view3d.object_as_camera()

        return {'FINISHED'}


#########################################################
#
#   ALIGNMENT OPTIONS
#
#########################################################

class PARADOX_OT_align_camera_to_object(bpy.types.Operator):
    bl_idname = "object.paradox_align_camera_to_object"
    bl_label = "Camera to Object"
    bl_description = "Rotates the camera to match the illusion of the selected object"
    # bl_space_type = ""
    # bl_region_type = ""
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        # Check if the active object has the illusion properties
        illusion_object = context.active_object
        if not check_ValidProperty_IllusionObject(illusion_object, self.report):
            return {'CANCELLED'}

        # Read the IllusionAngles property
        illusion_angle_x, illusion_angle_z = illusion_object["IllusionAngles"]


        # Check that the camera is valid
        camera = context.scene.camera
        if not check_ValidCamera(camera, report = self.report):
            return {'CANCELLED'}

        distance = (illusion_object.location -  camera.location).length

        # Set the orientation according to the illusion in the global orientation system
        # Notice that in this case the distance is set to zero
        align_CameraObject(camera, '1', illusion_object, illusion_angle_x, illusion_angle_z, 0.0, camera_distance = 0.0, report = self.report)

        # Correct with the rotation of the impossible object
        camera.rotation_euler.rotate(illusion_object.rotation_euler)
        # Correct with the camera distance
        camera.location = camera.location + camera.rotation_euler.to_matrix() @ Vector((0,0,distance))

        return {'FINISHED'}

class PARADOX_OT_align_object_to_camera(bpy.types.Operator):
    bl_idname = "object.paradox_align_object_to_camera"
    bl_label = "Object to Camera"
    bl_description = "Rotates an selected illusion object to matches the camera perspective"
    # bl_space_type = ""
    # bl_region_type = ""
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        ############################################
        # Check if the active object has the illusion properties
        ############################################
        illusion_object = context.active_object
        if not check_ValidProperty_IllusionObject(illusion_object, self.report):
            return {'CANCELLED'}

        # Read the IllusionAngles property
        illusion_angle_x, illusion_angle_z = illusion_object["IllusionAngles"]

        camera = context.scene.camera
        if not check_ValidCamera(camera, report = self.report):
            return {'CANCELLED'}


        distance = (illusion_object.location -  camera.location).length
        align_CameraObject(camera, '2', illusion_object, illusion_angle_x, illusion_angle_z, 0.0, camera_distance = distance, report = self.report)

        return {'FINISHED'}



#########################################################
#
#   TRANSFORMATION ALONG CAMERA ORIENTATION
#
#########################################################


class PARADOX_OT_camera_orientation_transform(bpy.types.Operator):
    bl_idname = "object.paradox_camera_transform"
    bl_label = "Camera Transform"
    bl_description = "Creates a transformation along the camera orientation"
    # bl_space_type = ""
    # bl_region_type = ""
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        camera = context.scene.camera
        if not check_ValidCamera(camera, report = self.report):
            return {'CANCELLED'}


        previous_active_object = context.view_layer.objects.active

        # Create the transform along the camera orientation
        context.view_layer.objects.active = camera
        bpy.ops.transform.create_orientation(name = "Illusion Camera", overwrite = True)
        bpy.ops.transform.select_orientation(orientation = "Illusion Camera")

        if previous_active_object is not None:
            context.view_layer.objects.active = previous_active_object



        return {'FINISHED'}
