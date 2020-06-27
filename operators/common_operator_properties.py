import bpy
from bpy.props import *

from math import *

#########################################################
#
#   COMMON PROPERTIES FOR OBJECTS
#
#########################################################


class GeometryProperties:
    '''
    General geometry properties.
    '''
    size_value : FloatProperty(
        name = "Size",
        description = "Size",
        default = 10.0,
        min = 0.1,
        max = 200.0,
        unit = "LENGTH"
    )
    thickness_value : FloatProperty(
        name = "Thickness",
        description = "Thickness",
        default = 2.0,
        min = 0.02,
        max = 40.0,
        unit = "LENGTH"
    )
    # Additional Scale Controls
    side_scaling : FloatVectorProperty(
        name = "Thickness Scaling",
        description = "Thickness scaling in each direction",
        default = (1.0, 1.0, 1.0),
        min = 0.01,
        max = 5.0
    )


class IllusionAlignmentProperties:
    '''
    Properties related to the camera angle required to see the illusion.
    These properties affect how the figure is rescaled according the perspective satisfy the continuity illusion.
    '''
    illusion_alignment : EnumProperty(
        items=(('0', 'Isometric', 'Set isometric perspective'),
                ('1', 'Axonometric', 'Set X, Z perspective angles'),
                ('2', 'Camera', 'Use the camera perspective')),
        name = "Illusion Alignment",
        description = "Camera Perspective required to see the illusion"
    )

    axonometric_angles_xz : FloatVectorProperty(
        name = "Axonometric Perspective Angles (X,Z)",
        description = "Perspective angles required for the illusion (X, Z only)",
        default = (radians(54.736), radians(45.0)),
        min = radians(15),
        max = radians(75.0),
        size = 2,
        unit = "ROTATION"
    )


class RelativeCameraAlignmentProperties:
    '''
    Properties related to the alignment between the camera and the impossible object.
    These properties do not affect the object proportions.
    '''
    align_camera_object : EnumProperty(
        items=(('0', 'None', ''),
                ('1', 'Camera to Object', 'Aligns the camera rotation to match the object illusion.'),
                ('2', 'Object to Camera', 'Aligns the object rotation to match the camera view.')),
        name = "Camera-Object Alignment",
        description = "Align camera or object to preserve the illusion."
    )
    tilt_angle : FloatProperty(
        name = "Tilt",
        description = "Tilt object around camera line of sight.",
        default = 0.0,
        min = -radians(180.),
        max = radians(180.),
        unit = "ROTATION"
    )
