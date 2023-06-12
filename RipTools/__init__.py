import bpy
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "RipTools",
    "author" : "Axebass",
    "description" : "Various tools to help with modifying and rigging ripped video game assets.",
    "blender" : (3, 5, 1),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : ""
}

from bpy.types import (Panel, Operator)
from bpy.props import PointerProperty

class MergeBonesOperator(bpy.types.Operator):
    bl_idname = "object.merge_bones"
    bl_label = "Merge Bones"



    def execute(self, context):
        source_armature = bpy.data.scenes["Scene"].source_armature_target
        dest_armature = bpy.data.scenes["Scene"].dest_armature_target
        bpy.ops.object.mode_set(mode='POSE')
        bones_source = source_armature.pose.bones
        bones_dest = dest_armature.pose.bones
        bpy.ops.object.mode_set(mode='EDIT')
        bones_dest_edit = dest_armature.data.edit_bones

        bone_dict_source = {bone.name: bone for bone in bones_source}
        bone_dict_dest = {bone.name: bone for bone in bones_dest}

        bones_queue = []
        bones_queue.append(bones_source[0].name)

        for bone_name in bones_queue:
            source_bone = bones_source[bone_name]
            dest_test = bones_dest.get(bone_name)
            if dest_test:
                bpy.ops.object.mode_set(mode='POSE')
                dest_bone = bones_dest[bone_name]
                if len(dest_bone.constraints) == 0:
                    const = dest_bone.constraints.new(type='CHILD_OF')
                    const.target = source_armature
                    const.subtarget = source_bone.name
                    bpy.ops.object.mode_set(mode='EDIT')
                    bone_dest_edit = bones_dest_edit[bone_name]
                    bone_dest_edit.parent = None


            for child_bone in source_bone.children:
                if child_bone.name not in bones_queue:
                    bones_queue.append(child_bone.name)

            bpy.context.view_layer.update()
        return {'FINISHED'}

class RigToolsPanel(bpy.types.Panel):
    bl_label =  "RipTools"
    bl_idname = "OBJECT_PT_RigTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RipTools"
    
    def draw(self, context):
        source_armature_target : PointerProperty(type=bpy.types.Armature)
        dest_armature_target : PointerProperty(type=bpy.types.Armature)
        scene = context.scene
        layout = self.layout
        obj = context.object
        row = layout.row()
        row.label(text="----BONE MERGING----")
        row = layout.row()
        row.label(text="Primary Armature")
        row = layout.row()
        row.prop(scene,"source_armature_target")
        row = layout.row()
        row.label(text="Following Armature")
        row = layout.row()
        row.prop(scene,"dest_armature_target")
        row = layout.row()
        row.operator(MergeBonesOperator.bl_idname, text = "Merge Bones", icon = "CONSTRAINT_BONE")

from bpy.utils import register_class, unregister_class

_classes = [
    MergeBonesOperator,
    RigToolsPanel
]

def register():
    print("registering")
    for cls in _classes:
        register_class(cls)
    bpy.types.Scene.source_armature_target = bpy.props.PointerProperty(type = bpy.types.Object)
    bpy.types.Scene.dest_armature_target = bpy.props.PointerProperty(type = bpy.types.Object)


def unregister():
    for cls in _classes:
        unregister_class(cls)
        
if __name__ == "__main__":
    register()