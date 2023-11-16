import bpy
from bpy.props import *
from math import *
from mathutils import *





from . common_operator_functions import check_ValidProperty_IllusionObject
from . common_operator_functions import get_Illusion_LocationNormals


#########################################################
#
#   TRANSLATION TOOL
#
#########################################################
class PARADOX_OT_illusion_translation(bpy.types.Operator):
    bl_idname = "object.paradox_illusion_translation"
    bl_label = "Illusion Translation"
    bl_description = "Moves the selected objects across the line of sight, according to the active illusion object"
    # bl_space_type = ""
    # bl_region_type = ""
    bl_options = {'REGISTER', 'UNDO'}

    # Set the origin and target destitation for the illusion
    direction : EnumProperty(
        items=(('0', 'Backward', 'Move backwards'),
                ('1', 'Forward', 'Move forward')),
        name = "Direction",
        description = "Moves forward or backward, relative to the camera."
    )

    def execute(self, context):

        ############################################
        # Check if the active object has the illusion properties
        ############################################
        illusion_object = context.active_object
        if not check_ValidProperty_IllusionObject(illusion_object, self.report):
            return {'CANCELLED'}


        ############################################
        # Get the location and Normals of the illusion planes
        ############################################
        illusion_loc, illusion_norm = get_Illusion_LocationNormals(illusion_object)


        # Unselect the illusion object
        illusion_object.select_set(False)

        ############################################
        # Move the selected objects
        ############################################

        # Find the origin and target location for the object
        if self.direction == '0':
            origin_illusion = 0
            target_illusion = 1
        elif self.direction == '1':
            origin_illusion = 1
            target_illusion = 0

        # Distance and direction in which to translate the duplicate object
        translate_vector = illusion_loc[target_illusion] - illusion_loc[origin_illusion]
        bpy.ops.transform.translate(value = translate_vector, orient_type = 'GLOBAL', orient_matrix = ((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type = 'GLOBAL')

        # Reselect the illusion object
        illusion_object.select_set(True)
        context.view_layer.objects.active = illusion_object
        return {'FINISHED'}


#########################################################
#
#   DUPLICATE TOOL
#
#########################################################
class PARADOX_OT_illusion_duplicate(bpy.types.Operator):
    bl_idname = "object.paradox_illusion_duplicate"
    bl_label = "Illusion Duplicate"
    bl_description = "Duplicates the selected objects, and moves the copy along the line of sight, according to the active illusion object"
    # bl_space_type = ""
    # bl_region_type = ""
    bl_options = {'REGISTER', 'UNDO'}

    # Set the origin and target destitation for the illusion
    direction : EnumProperty(
        items=(('0', 'Backward', 'Duplicate and move backward'),
                ('1', 'Forward', 'Duplicate and move forward')),
        name = "Direction",
        description = "Move the duplicate forward or backwards, relative to the camera."
    )

    
    linked_duplicate : BoolProperty(
        name = "Linked Duplicate",
        description = "Make a linked duplicate",
        default = False
    )

    def execute(self, context):

        ############################################
        # Check if the active object has the illusion properties
        ############################################
        illusion_object = context.active_object
        if not check_ValidProperty_IllusionObject(illusion_object, self.report):
            return {'CANCELLED'}



        ############################################
        # Get the location and Normals of the illusion planes
        ############################################
        illusion_loc, illusion_norm = get_Illusion_LocationNormals(illusion_object)

        ############################################
        # Loop over the selected objects to perform the duplicate
        ############################################

        # List of the selected objects, omitting the illusion active object
        selected_objects = context.selected_objects
        selected_objects.remove(illusion_object)
        duplicated_objects = []

        for select_obj in selected_objects:
            # Find the origin and target location for the object
            if self.direction == '0':
                origin_illusion = 0
                target_illusion = 1
            elif self.direction == '1':
                origin_illusion = 1
                target_illusion = 0

            # Select only the duplicate object
            bpy.ops.object.select_all(action='DESELECT')
            select_obj.select_set(True)
            context.view_layer.objects.active = select_obj

            # Distance and direction in which to translate the duplicate object
            translate_vector = illusion_loc[target_illusion] - illusion_loc[origin_illusion]
            translate_input = {"value":translate_vector, "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL'}
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":self.linked_duplicate, "mode":'TRANSLATION'}, TRANSFORM_OT_translate=translate_input)

            # Get the duplicated object
            dupli_obj = context.selected_objects[0]
            duplicated_objects.append(dupli_obj)
            
            if False:
                context.view_layer.objects.active = dupli_obj
                context_constraint = bpy.context.copy()

                # Set the rotation and scale to the default value, otherwise the constraints cause problems
                original_rotation = select_obj.rotation_euler.copy()
                original_scale = select_obj.scale.copy()
                select_obj.rotation_euler = Vector((0,0,0))
                dupli_obj.rotation_euler = Vector((0,0,0))
                select_obj.scale = Vector((1,1,1))
                dupli_obj.scale = Vector((1,1,1))

                # Location constraint
                bpy.ops.object.constraint_add(type='CHILD_OF')
                child_constraint = context.object.constraints[-1]
                child_constraint.name = "Child Of - Illusion"
                child_constraint.target = select_obj

                context_constraint["constraint"] = child_constraint
                bpy.ops.constraint.childof_set_inverse(context_constraint, constraint=child_constraint.name, owner='OBJECT')

                child_constraint.use_rotation_x = False
                child_constraint.use_rotation_y = False
                child_constraint.use_rotation_z = False
                child_constraint.use_scale_x = False
                child_constraint.use_scale_y = False
                child_constraint.use_scale_z = False

                # Rotation and Scale constraint
                bpy.ops.object.constraint_add(type='COPY_ROTATION')
                rotation_constraint = context.object.constraints[-1]
                rotation_constraint.name = "Copy Rotation - Illusion"
                rotation_constraint.target = select_obj

                bpy.ops.object.constraint_add(type='COPY_SCALE')
                scale_constraint = context.object.constraints[-1]
                scale_constraint.name = "Copy Scale - Illusion"
                scale_constraint.target = select_obj


                # Return the rotation and constraint to the original value.
                select_obj.rotation_euler = original_rotation
                select_obj.scale = original_scale

        ############################################
        # Re-Select the original objects and the active illusion
        ############################################
        bpy.ops.object.select_all(action='DESELECT')
        for select_obj in selected_objects:
            select_obj.select_set(True)
        for dupli_obj in duplicated_objects:
            dupli_obj.select_set(True)

        illusion_object.select_set(True)
        context.view_layer.objects.active = illusion_object

        return {'FINISHED'}

#########################################################
#
#   BISECT TOOL
#
#########################################################
class PARADOX_OT_illusion_bisect(bpy.types.Operator):
    bl_idname = "object.paradox_illusion_bisect"
    bl_label = "Illusion Bisect"
    bl_description = "Bisects the selected objects across the illusion of the active illusion object"
    # bl_space_type = ""
    # bl_region_type = ""
    bl_options = {'REGISTER', 'UNDO'}


    clear : EnumProperty(
        items=(('0', 'None', 'Bisects only'),
                ('1', 'Front', 'Clear using the front illusion normal'),
                ('2', 'Back', 'Clear using the back illusion normal'),
                ('3', 'Closest', 'Clear using the closest illusion normal')),
        name = "Illusion Clear",
        description = "Remove the geometry across the illusion plane",
        default = '1'
    )

    '''
    clear : BoolProperty(
        name = "Clear",
        description = "Remove the geometry across the illusion plane",
        default = True
    )

    clear_invert : BoolProperty(
        name = "Invert",
        description = "Inverts the geometry removed",
        default = False
    )
    '''
    def execute(self, context):
        ############################################
        # Check if the active object has the illusion properties
        ############################################
        illusion_object = context.active_object
        if not check_ValidProperty_IllusionObject(illusion_object, self.report):
            return {'CANCELLED'}



        ############################################
        # Get the location and Normals of the illusion planes
        ############################################
        illusion_loc, illusion_norm = get_Illusion_LocationNormals(illusion_object)

        ############################################
        # Loop over the selected objects to bisect
        ############################################

        # List of the selected objects, omitting the illusion active object
        selected_objects = context.selected_objects
        selected_objects.remove(illusion_object)

        for select_obj in selected_objects:
            # Check if the selected object is a mesh. Otherwise skip.
            if select_obj.type != 'MESH':
                self.report({'WARNING'}, select_obj.name + " cannot be bisected.")
                continue


            # Select only the bisect object
            bpy.ops.object.select_all(action='DESELECT')
            select_obj.select_set(True)
            context.view_layer.objects.active = select_obj

            # Enter into edit mode
            bpy.ops.object.editmode_toggle()
            # Select all the vertices for the object
            bpy.ops.mesh.select_all(action='SELECT')

            # Bisect clearing options
            if self.clear == '0':
                # Bisect Only
                illusion_target = 0
                clear_inner = False
                clear_outer = False
            elif self.clear == '1':
                # Clear using the front illusion
                illusion_target = 0
                clear_inner = False
                clear_outer = True
            elif self.clear == '2':
                # Clear using the back illusion,
                # Clearing bools to be updated once the normal calculation is correct
                illusion_target = 1
                clear_inner = True
                clear_outer = False
            elif self.clear == '3':
                # Clear using the closest illusion

                illusion_target = 0
                illusion_distance = (illusion_loc[illusion_target] - select_obj.location).length
                # Find the closest illusion
                for i in range(len(illusion_loc)):
                    if (illusion_loc[i] - select_obj.location).length < illusion_distance:
                        illusion_target = i
                        illusion_distance = (illusion_loc[illusion_target] - select_obj.location).length

                # Clearing bools to be updated once the normal calculation is correct
                if illusion_target == 0:
                    clear_inner = False
                    clear_outer = True
                else:
                    clear_inner = True
                    clear_outer = False

            # Bisect
            bpy.ops.mesh.bisect(plane_co=illusion_loc[illusion_target], plane_no=illusion_norm[illusion_target], clear_inner = clear_inner, clear_outer = clear_outer)

            # Exit the edit mode
            bpy.ops.object.editmode_toggle()


        ############################################
        # Re-Select the original objects and the active illusion
        ############################################
        bpy.ops.object.select_all(action='DESELECT')
        for select_obj in selected_objects:
            select_obj.select_set(True)

        illusion_object.select_set(True)
        context.view_layer.objects.active = illusion_object

        return {'FINISHED'}
