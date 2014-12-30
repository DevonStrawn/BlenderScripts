
'''

Blender Python script that modifies ALL existing materials & textures in a scene to be 8-bit friendly:
	* 1.0 diffuse
	* 0.0 specular
	* NO MIP-MAPS or interpolation, with the smallest possible box filter kernel width

Simply open a scene with materials & textures you want to ALL be 8-bit style, load and execute this script and they'll all be changed.

You can further customize the materials by hand after running this script, or add heuristics here to conditionally set material properties, e.g., based on material name, etc.
To quickly find out the Python syntax to modify a material or texture property, right-click the field in the Blender Buttons panel and select "Copy Data Path".

'''

import bpy

# Make all materials
for mat in bpy.data.materials:
	mat.diffuse_intensity = 1.0
	mat.specular_intensity = 0.0

# Make all textures use nearest neighbor filtering with smallest possible filter size, and turn off interpolation.
for mat in bpy.data.materials:
	for texslot in mat.texture_slots:
		if texslot is not None and texslot.texture is not None:
#			print(type(texslot.texture))
			if type(texslot.texture) is bpy.types.ImageTexture:
				texslot.texture.use_mipmap = False

				texslot.texture.filter_type = 'BOX'
				texslot.texture.filter_size = 0.1
				texslot.texture.use_interpolation = False

#				print(texslot.texture.filter_type, type(texslot.texture.filter_type))
#				print(texslot.texture.filter_size, type(texslot.texture.filter_size))
#				print(dir(texslot.texture))
