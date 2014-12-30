
'''

Gives each bone a unique name.
Useful for e.g., preparing duplicated armatures for export to Collada.

'''

import bpy

# Maps from a bone instance to its name.
boneAndNames = {}

# First, build the map from bone instances to the bone's name.
for ob in bpy.data.objects:
	if ob.type == 'ARMATURE':
		armature = ob.data
		for bone in armature.bones:
			boneAndNames[bone] = bone.name

beforeBoneNamesWithDuplicates = len(boneAndNames.values())
beforeBoneNamesUnique = len(set(boneAndNames.values()))
print('BEFORE: %d bone names, %d unique' % (beforeBoneNamesWithDuplicates, beforeBoneNamesUnique))

# Finally, give each bone a unique name.
for ob in bpy.data.objects:
	if ob.type == 'ARMATURE':
		armature = ob.data
		for bone in armature.bones:
			if bone.name in boneAndNames.values():
				newName = armature.name + '.' + bone.name
				bone.name = newName
				boneAndNames[bone] = newName

afterBoneNamesWithDuplicates = len(boneAndNames.values())
afterBoneNamesUnique = len(set(boneAndNames.values()))
print('AFTER: %d bone names, %d unique' % (afterBoneNamesWithDuplicates, afterBoneNamesUnique))
