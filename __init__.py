bl_info = {
    "name" : "Paradox Toolkit",
    "author" : "Matias Garate",
    "description" : "Tools for 3D optical illusions by Matias Garate",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}


import bpy




#########################################################
#
#   IMPORT CLASSES: OPERATORS; PANELS; MENUS; ICONS
#
#########################################################


from . operators.operators_camera_tools import *
from . operators.operators_illusion_tools import *
from . operators.operators_construct_geometry import *

from . ui.panels import *
from . ui.menus import *
from . ui.icons import *




# Classes that need to be registered
classes = [
    PARADOX_OT_construct_penrose_triangle,
    PARADOX_OT_construct_reutersvard_rectangle,
    PARADOX_OT_construct_impossible_arch,
    PARADOX_OT_construct_impossible_cube,
    PARADOX_OT_construct_penrose_stair,
    PARADOX_OT_add_axonometric_camera,
    PARADOX_OT_align_camera_to_object,
    PARADOX_OT_align_object_to_camera,
    PARADOX_OT_camera_orientation_transform,
    PARADOX_OT_illusion_translation,
    PARADOX_OT_illusion_duplicate,
    PARADOX_OT_illusion_bisect,
    OBJECT_PT_paradox_geometry,
    OBJECT_PT_paradox_camera,
    OBJECT_PT_paradox_illusion,
    VIEW3D_MT_paradox_add
    ]






#########################################################
#
#   REGISTER AND UNREGISTER CLASSES
#
#########################################################

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
    register_classes()
    icon_register()
    bpy.types.VIEW3D_MT_add.append(menu_function_paradox_add)

def unregister():
    unregister_classes()
    icon_unregister()
    bpy.types.VIEW3D_MT_add.remove(menu_function_paradox_add)


if __name__ == "__main__":
    register()
