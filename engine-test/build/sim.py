import bpy

# Clear existing objects
bpy.ops.wm.read_factory_settings(use_empty=True)

# Generate FR4 Substrate
bpy.ops.mesh.primitive_cube_add(size=1, location=(5.0, 5.0, -0.5), scale=(10.0, 10.0, 1))
board = bpy.context.scene.objects[-1]
board.name = 'FR4_Substrate'

# Generate Copper Voxels
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(2.0, 2.0, 0.5))
bpy.context.scene.objects[-1].name = 'Copper_Trace'
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(3.0, 2.0, 0.5))
bpy.context.scene.objects[-1].name = 'Copper_Trace'
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(4.0, 2.0, 0.5))
bpy.context.scene.objects[-1].name = 'Copper_Trace'
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(5.0, 2.0, 0.5))
bpy.context.scene.objects[-1].name = 'Copper_Trace'
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(6.0, 2.0, 0.5))
bpy.context.scene.objects[-1].name = 'Copper_Trace'
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(7.0, 2.0, 0.5))
bpy.context.scene.objects[-1].name = 'Copper_Trace'
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(8.0, 2.0, 0.5))
bpy.context.scene.objects[-1].name = 'Copper_Trace'
