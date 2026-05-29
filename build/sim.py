import bpy

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# FR4 Substrate
bpy.ops.mesh.primitive_cube_add(size=1, location=(25, 25, -0.5), scale=(50, 50, 1))
bpy.context.scene.objects[-1].name = 'FR4_Substrate'

# Copper Traces
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 26, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(30, 28, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 13, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(29, 35, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(24, 27, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 19, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(15, 10, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 25, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(30, 27, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(29, 34, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 12, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(23, 27, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 18, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(14, 10, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 24, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(29, 27, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 11, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(22, 27, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(29, 33, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 17, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(13, 10, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 23, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(28, 27, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(21, 27, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 10, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(29, 32, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 16, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(12, 10, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(29, 38, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 22, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(27, 27, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(20, 27, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(18, 10, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(11, 10, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 15, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(29, 37, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(26, 27, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 21, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(17, 10, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 27, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(30, 29, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 14, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(29, 36, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(25, 27, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(19, 20, 0))
bpy.context.scene.objects[-1].name = 'Copper'
bpy.ops.mesh.primitive_cube_add(size=1, location=(16, 10, 0))
bpy.context.scene.objects[-1].name = 'Copper'
