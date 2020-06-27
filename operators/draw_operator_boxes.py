import bpy
from bpy.props import *

#########################################################
#
#   DRAW FUNCTIONS FOR COMMON PROPERTIES
#
#########################################################


def draw_Geometry_Box(operator, geometry_params = [["Size", "size_value"]]):
    '''
    Draw the default geometry parameters.
    -------------
    geometry_params[]: Array of basic parameters, each element is [Label, property name]
    '''

    layout = operator.layout

    box = layout.box()

    # Basic geometry parameters (by default: Size)
    # Allows to include additional paramters (Height, Width, etc).
    row = box.row()
    row.label(text = "Geometry Parameters")
    for param_text, param_name  in geometry_params:
        row = box.row()
        row.label(text = param_text+":")
        row.prop(operator, param_name, expand = True, text="")

    # Thickness and scaling of the object sides
    row = box.row()
    row.label(text = "Thickness:")
    row.prop(operator, "thickness_value", expand = True, text="")

    row = box.row()
    row.prop(operator, "side_scaling", expand = False, text="Scale")


def draw_IllusionAlignment_Box(operator, title = "Illusion Alignment"):
    '''
    Draw the default Illusion Alignment options.
    Sets the perspective required to see the illusion.
    The object proportions may change depending on the perspective.
    '''

    layout = operator.layout
    box = layout.box()

    row = box.row()
    row.label(text = title)
    row = box.row()
    row.prop(operator, "illusion_alignment", expand = True)

    # If the perspective is set to "Axonometric", ask for the (X, Z) angle input
    if operator.illusion_alignment == '1':
        row = box.row()
        row.prop(operator, "axonometric_angles_xz", expand = True, text = "Angles (X,Z)")


def draw_RelativeAlignment_Box(operator):
    '''
    Draw the default Camera-Object Alignment options.
    '''
    layout = operator.layout

    box = layout.box()
    row = box.row()
    row.label(text = "Camera-Object Alignment")

    row = box.row()
    row.prop(operator, "align_camera_object", expand = False, text = "Align")

    row = box.row()
    row.label(text = "Tilt:")
    row.prop(operator, "tilt_angle", expand = True, text="")
