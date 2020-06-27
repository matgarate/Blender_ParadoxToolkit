import bpy
import bpy.utils.previews
import os

preview_collections = {}

def icon_register():
    icon_dir = os.path.join(os.path.dirname(__file__), "icons")
    icon_preview = bpy.utils.previews.new()

    # Load the Icon for the add object menu
    icon_preview.load("penrose_icon", os.path.join(icon_dir, "penrose_icon.png"), 'IMAGE')
    preview_collections["main"] = icon_preview

def icon_unregister():
    for icon_preview in preview_collections.values():
        bpy.utils.previews.remove(icon_preview)
    preview_collections.clear()


def get_ToolkitIconId():
    icon_preview = preview_collections["main"]
    return icon_preview["penrose_icon"].icon_id
