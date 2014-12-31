BlenderScripts
==============

Scripts for to make Blender do things better:

* BlenderMakeBoneNamesUnique.py - Gives each bone a unique name.  Useful for e.g., preparing duplicated armatures for export to Collada.
* BlenderMakeMaterials8Bit.py - Modifies ALL existing materials & textures in a scene to be 8-bit friendly: perfectly diffuse with sharp texture interpolation.
* BlenderBatchExport.py - Shell script to export multiple .blend files.  Useful for integrating Blender into a content pipeline.  Works out of the box with included example .blend file, but should be modified to your specific needs.

**Example:**

Export the example .blend file included in this repo: `./BlenderBatchExport.py`

![Batch Export](BlendFiles/Example_Export.png?raw=true "Export")

**Credits:**

* "Low poly tiny planet" by kavabanga, <a href="http://creativecommons.org/licenses/by/3.0/">CC-By</a>
