import bpy
from . icons import get_ToolkitIconId

class OBJECT_PT_paradox_geometry(bpy.types.Panel):
    bl_idname = "OBJECT_PT_ParadoxGeometry"
    bl_label = "Construct Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Paradox Tools"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        layout.menu("VIEW3D_MT_paradox_add", text="Illusion Object", icon_value = get_ToolkitIconId())

class OBJECT_PT_paradox_camera(bpy.types.Panel):
    bl_idname = "OBJECT_PT_ParadoxCameraTools"
    bl_label = "Camera Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Paradox Tools"
    bl_context = "objectmode"



    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('object.paradox_add_axonometric_camera')
        row = layout.row()
        row.operator('object.paradox_camera_transform')

        row = layout.row()
        row.label(text = "Alignment Tools")
        row = layout.row()
        row.operator('object.paradox_align_camera_to_object')
        row = layout.row()
        row.operator('object.paradox_align_object_to_camera')



class OBJECT_PT_paradox_illusion(bpy.types.Panel):
    bl_idname = "OBJECT_PT_ParadoxIllusionTools"
    bl_label = "Illusion Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Paradox Tools"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('object.paradox_illusion_translation')

        row = layout.row()
        row.operator('object.paradox_illusion_duplicate')

        row = layout.row()
        row.operator('object.paradox_illusion_bisect')
