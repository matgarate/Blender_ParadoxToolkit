import bpy
from . icons import get_ToolkitIconId


def menu_function_paradox_add(self, context):
    '''
    Includes the Paradox Object option to the Add Object menu
    '''
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'
    layout.separator()
    layout.menu("VIEW3D_MT_paradox_add", text="Illusion Object", icon_value = get_ToolkitIconId())
    layout.separator()

class VIEW3D_MT_paradox_add(bpy.types.Menu):
    '''
    List of impossible objects. Includes the axonometric camera.
    '''
    bl_idname = "VIEW3D_MT_paradox_add"
    bl_label = "Paradox Add Menu"
    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'



        layout.operator("object.paradox_construct_penrose_triangle", text="Penrose Triangle")
        layout.operator("object.paradox_construct_reutersvard_rectangle", text="Reutersvard Rectangle")
        layout.operator("object.paradox_construct_impossible_arch", text="Impossible Arch")
        layout.operator("object.paradox_construct_penrose_stair", text="Penrose Stair")
        layout.operator("object.paradox_construct_impossible_cube", text="Impossible Cube")
        layout.separator()


