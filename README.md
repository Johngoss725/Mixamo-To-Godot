# Mixamo-To-Godot
This is a Blender 2.9 script for importing mixamo Models to Godot-3
 
The script does the following things 
1) Imports the mixamo models from the folder you specify.
2) Adds a root motion bone to the skeleton.
3) Renames the skeleton to godot appropriate conventions.
4) Creates NLA tracks for each action and names each action.

How to use:
Set the filepath in the script where it specifies to the folder that you want to get the animations from. Have only the animations that you want in that folder. Open blender delete eveything in the scene and then run the script from the text editor.  
Make sure that all of the mixamo files were downloaded with skin otherwise the script will not work. The actions in blender are named by whatever the name of the file is in the import folder. 

There are a few bugs but overall it works very well to quickly protrytpe a 3d Godot game. 

