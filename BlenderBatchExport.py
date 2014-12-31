#!/usr/bin/env python

'''
 ____  _                _             ____        _       _       _____                       _            
| __ )| | ___ _ __   __| | ___ _ __  | __ )  __ _| |_ ___| |__   | ____|_  ___ __   ___  _ __| |_ ___ _ __ 
|  _ \| |/ _ \ '_ \ / _` |/ _ \ '__| |  _ \ / _` | __/ __| '_ \  |  _| \ \/ / '_ \ / _ \| '__| __/ _ \ '__|
| |_) | |  __/ | | | (_| |  __/ |    | |_) | (_| | || (__| | | | | |___ >  <| |_) | (_) | |  | ||  __/ |   
|____/|_|\___|_| |_|\__,_|\___|_|    |____/ \__,_|\__\___|_| |_| |_____/_/\_\ .__/ \___/|_|   \__\___|_|   
                                                                            |_|                            

A self-contained script to export multiple Blender files.

----------------------------------------------------------------------------------------------------------------------------------
INSTRUCTIONS:
----------------------------------------------------------------------------------------------------------------------------------
1. Install Python prerequisites:
	a. 'sarge': e.g., 'pip install sarge'
2. Specify paths to the following by editing the strings and array below:
	b. input path - where the .blend files are locate
	c. input filenames - the list of blend files
	d. output path - where the exported files are saved
3. Run this script, 'python BlenderBatchExport.py'.

   The first time through, you'll be prompted for the path to your Blender executable.  It will be saved in a config file and you
   won't be prompted again afterward.  If you want to change the path to Blender, either edit the config file or delete it and run
   this script again.

----------------------------------------------------------------------------------------------------------------------------------
NOTES:
----------------------------------------------------------------------------------------------------------------------------------
You will probably need to tweak some parts depending on the version of Blender you're using and your specific exporting needs.
For example, the export options vary between versions.  The ones below were tested on v2.72 for Wavefront .OBJ export.

This script is unique in that it 'bootstraps' itself, conditionally changing its behavior based on how it's executed:
* if run from command-line, it will run Blender and pass *itself* as the script that Blender will run at startup.
* if run inside Blender, it will operate as a Blender script and export the specified .blend file.

'''

# TODO Use Gooey to provide a nice UI to browse for these paths (and path to Blender executable), and specify list of .blend files to export.
# TODO Locate blender automatically? E.g., from well-known locations: registry, /usr/bin/, etc.

'''
Example defaults that will work out-of-the-box.  You can override these by either:
	(a) changing them by hand here
	(b) calling this script with command-line arguments to override these values
'''
#inputFolder=r"BlendFiles"
outputFolder=r"ExportFolder"
inputFilenames = [ 'BlendFiles/planet_baked.blend', ]

def RunAsCommandLineScript():
	#  _____ _     _                        _                             __                       _   _                                                          _   _ _            
	# |_   _| |__ (_)___   _ __   __ _ _ __| |_   _ __ _   _ _ __  ___   / _|_ __ ___  _ __ ___   | |_| |__   ___    ___ ___  _ __ ___  _ __ ___   __ _ _ __   __| | | (_)_ __   ___ 
	#   | | | '_ \| / __| | '_ \ / _` | '__| __| | '__| | | | '_ \/ __| | |_| '__/ _ \| '_ ` _ \  | __| '_ \ / _ \  / __/ _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` | | | | '_ \ / _ |
	#   | | | | | | \__ \ | |_) | (_| | |  | |_  | |  | |_| | | | \__ \ |  _| | | (_) | | | | | | | |_| | | |  __/ | (_| (_) | | | | | | | | | | | (_| | | | | (_| | | | | | | |  __/
	#   |_| |_| |_|_|___/ | .__/ \__,_|_|   \__| |_|   \__,_|_| |_|___/ |_| |_|  \___/|_| |_| |_|  \__|_| |_|\___|  \___\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_| |_|_|_| |_|\___|
	#                     |_|                                                                                                                                                        

	import os, sys, argparse, ConfigParser
	import sarge

	global inputFilenames, outputFolder

	parser = argparse.ArgumentParser(description='Batch export the contents of multiple .blend files.')
	parser.add_argument('--inputFilenames',
#		dest='accumulate',
		nargs='+',	# Accept zero or more filenames after '--inputFilenames' switch.
		default = inputFilenames,
#		action='store_const', const=sum, default=max,
		help='List of Blend files to export from.')
	parser.add_argument('--outputFolder',
		default = outputFolder,
		help='Folder to save the exported files into.')
	args = parser.parse_args()

	inputFilenames = args.inputFilenames
	outputFolder = args.outputFolder

#	print(sys.argv)
#	exit()

	thisScriptsPath = os.path.realpath(__file__)
	configFilePath = os.path.join(os.path.split(thisScriptsPath)[0], '_BlenderBatchExport.cfg')

	print(configFilePath)

	# Load settings from configuration file.
	config = ConfigParser.SafeConfigParser()
	config.add_section('BlenderConfig')
	config.read(configFilePath)

	try:
		blenderPath = config.get('BlenderConfig', 'BlenderPath', None)
	except ConfigParser.NoOptionError:
		blenderPath = None

	# If blender path is not specified, prompt the user to provide it.
	if blenderPath == None:
		# Prompt for path to Blender exe.
		import Tkinter, tkFileDialog
		root = Tkinter.Tk()
		root.withdraw()
		blenderPath = tkFileDialog.askopenfilename(title='Please specify the path to Blender executable')

		# Store provided path in config file.
		config.set('BlenderConfig', 'BlenderPath', blenderPath)
		with open(configFilePath, 'wb') as configfile:
			config.write(configfile)

	print('\n')
	print(blenderPath)
	print(inputFilenames)
	print(outputFolder)
#	sys.exit()

	# TODO Cache result in file alongside this script, or in user settings, registry, etc.

	# Clear out PYTHONPATH so that Blender finds its own Python.
	# TODO Find a cleaner way to do this...
	del os.environ['PYTHONPATH']

	#IFS=	# disable word splitting.
	#FILES=("$inputFolder"/*.blend)
	#for f in "$inputFolder\*.blend"; do
	for inputFilename in inputFilenames:
#		inputFilename = os.path.join(inputFolder, inputFilename)
		print("Processing file %s" % inputFilename)
		# TODO !!!
	#	"$blenderPath" --background --python BlenderBatchExport.py -- "$inputFolder" "$outputFolder"
		commandLine = '"%s" --background --python %s -- "%s" "%s"' % (os.path.abspath(blenderPath), thisScriptsPath, os.path.abspath(inputFilename), os.path.abspath(outputFolder))
		print("\tRunning Blender with cmd line: %s" % commandLine)
		result = sarge.run(commandLine, async=False)

def RunAsBlenderScript():

	#  _____ _     _                        _                            _         ____  _                _           
	# |_   _| |__ (_)___   _ __   __ _ _ __| |_   _ __ _   _ _ __  ___  (_)_ __   | __ )| | ___ _ __   __| | ___ _ __ 
	#   | | | '_ \| / __| | '_ \ / _` | '__| __| | '__| | | | '_ \/ __| | | '_ \  |  _ \| |/ _ \ '_ \ / _` |/ _ \ '__|
	#   | | | | | | \__ \ | |_) | (_| | |  | |_  | |  | |_| | | | \__ \ | | | | | | |_) | |  __/ | | | (_| |  __/ |   
	#   |_| |_| |_|_|___/ | .__/ \__,_|_|   \__| |_|   \__,_|_| |_|___/ |_|_| |_| |____/|_|\___|_| |_|\__,_|\___|_|   
	#                     |_|                                                                                         

	import sys, os
	import bpy

#	print(sys.argv)

	# TODO Specify arguments via e.g., command-line switches.
	inputFilename = bpy.path.abspath(sys.argv[5])
	outputFolder = bpy.path.abspath(sys.argv[6])

#	print([inputFilename])
#	print(outputFolder)

	# Deselect all objects
	def DeselectAll():
	    for obj in bpy.context.scene.objects:
	        obj.select = False

	def Export(file_path):
		bpy.ops.export_scene.obj(
			filepath = file_path,
			check_existing = True,		# Check and warn on overwriting existing files
			filter_glob = "*.obj;*.mtl",
			use_selection = False,		# Selection Only
	#		use_all_scenes = False,
			use_animation = False,
	#		use_apply_modifiers = True,
	#		use_rotate_x90 = True,
			use_edges = True,
			use_normals = False,
	#		use_hq_normals = True,
			use_uvs = True,
			use_materials = True,		# Write Materials
	#		copy_images = False,
			use_triangles = True,		# Triangulate Faces
			use_vertex_groups = False,
			use_nurbs = False,
			use_blen_objects = True,	# Objects as OBJ Objects
			group_by_object = False,	# Objects as OBJ Groups
			group_by_material = False,	# Material Groups
			keep_vertex_order = False,

			path_mode = 'COPY',		# Path Mode - controls how file paths are referenced.  'COPY' means the files are copied to the output dir.
			axis_forward = '-Z',
			axis_up = 'Y',
			use_mesh_modifiers = True)	# Apply Modifiers

	outputFilename = os.path.join(outputFolder, os.path.splitext(os.path.split(inputFilename)[1])[0] + '.obj')

	print('Opening blender file "%s"' % inputFilename)
	bpy.ops.wm.open_mainfile(filepath=inputFilename)

	DeselectAll()
	print('Exporting to "%s"' % outputFilename)
	Export(outputFilename)

try:
	import bpy
	RunAsBlenderScript()
except ImportError:
	RunAsCommandLineScript()
