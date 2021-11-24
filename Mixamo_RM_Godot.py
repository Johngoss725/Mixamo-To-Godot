import bpy
import os
import ntpath

#Script Created By: Average Godot Enjoyer

        
def fixBones():
    #print('Running Mixamo Armature Renaming Script.')
    bpy.ops.object.mode_set(mode = 'OBJECT')
        
    if not bpy.ops.object:
            print('Please select the armature')

    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.context.object.show_in_front = True

    for rig in bpy.context.selected_objects:
        if rig.type == 'ARMATURE':
            for mesh in rig.children:
                for vg in mesh.vertex_groups:
                    #print(vg.name)
                    new_name = vg.name
                    new_name = new_name.replace("mixamorig:","")
                    #print(new_name)
                    rig.pose.bones[vg.name].name = new_name
                    vg.name = new_name
            for bone in rig.pose.bones:
                #print(bone.name.replace("mixamorig:",""))
                bone.name = bone.name.replace("mixamorig:","")



    for action in bpy.data.actions:
        print(action.name)
        fc = action.fcurves
        for f in fc:
            #print(f.data_path)
            f.data_path = f.data_path.replace("mixamorig:","")
        
def scaleAll():
    bpy.ops.object.mode_set(mode='OBJECT')

    prev_context=bpy.context.area.type
        
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')
    bpy.context.area.type = 'GRAPH_EDITOR'
    bpy.context.space_data.dopesheet.filter_text = "Location"
    bpy.context.space_data.pivot_point = 'CURSOR'
    bpy.context.space_data.dopesheet.use_filter_invert = False
        
    #print(bpy.context.selected_objects)
    bpy.ops.anim.channels_select_all(action='SELECT')   
        
    bpy.ops.transform.resize(value=(1, 0.01, 1), orient_type='GLOBAL',
    orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    orient_matrix_type='GLOBAL',
    constraint_axis=(False, True, False),
    mirror=True, use_proportional_edit=False,
    proportional_edit_falloff='SMOOTH',
    proportional_size=1,
    use_proportional_connected=False,
    use_proportional_projected=False)


def copyHips():
        
    bpy.context.area.ui_type = 'FCURVES'
    #SELECT OUR ROOT MOTION BONE 
    bpy.ops.pose.select_all(action='DESELECT')
    bpy.context.object.pose.bones['RootMotion'].bone.select = True
    # SET FRAME TO ZERO
    bpy.ops.graph.cursor_set(frame=0.0, value=0.0)
    #ADD NEW KEYFRAME
    bpy.ops.anim.keyframe_insert_menu(type='Location')
    #SELECT ONLY HIPS AND LOCTAIUON GRAPH DATA
    bpy.ops.pose.select_all(action='DESELECT')
    bpy.context.object.pose.bones['Hips'].bone.select = True        
    bpy.context.area.ui_type = 'DOPESHEET'
    bpy.context.space_data.dopesheet.filter_text = "Location"
    bpy.context.area.ui_type = 'FCURVES'
    #COPY THE LOCATION VALUES OF THE HIPS AND DELETE THEM         
    bpy.ops.graph.copy()
    bpy.ops.graph.select_all(action='DESELECT')
    
    myFcurves = bpy.context.object.animation_data.action.fcurves
    # print(myFcurves)
        
    for i in myFcurves:
        if str(i.data_path)=='pose.bones["Hips"].location':
            myFcurves.remove(i)
                
    bpy.ops.pose.select_all(action='DESELECT')
    bpy.context.object.pose.bones['RootMotion'].bone.select = True
    bpy.ops.graph.paste()        
        
    bpy.context.area.ui_type = 'VIEW_3D'

    
def deleteArmeture():
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action="SELECT")


    bpy.ops.object.delete(use_global=False, confirm=False)

def import_armeture(path):
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    bpy.ops.import_scene.fbx( filepath = path)
    
def add_root_bone():
    #we get our armeture
    armeture = bpy.data.objects[0]
    bpy.ops.object.mode_set(mode='EDIT')
    # add root Motion 
    bpy.ops.armature.bone_primitive_add() 
        
       
    bpy.ops.object.mode_set(mode='POSE')
    bpy.context.object.pose.bones["Bone"].name = "RootMotion"

    bpy.ops.object.mode_set(mode='EDIT')
        
    armeture.data.edit_bones['mixamorig:Hips'].parent = armeture.data.edit_bones['RootMotion']
    bpy.ops.object.mode_set(mode='OBJECT')
        
    
def get_all_anims():
# HERE IS WHERE WE PLACE OUR FILEPATH TO THE FOLDER WITH OUR ANIMATIONS. 
    path = ""
    
    files = os.listdir(path)
    use_num = len(files)
    counter = 0 
    
    for file in files:
        use_string = path+"/"+file
        import_armeture(use_string)
        print("We are now importing: " + use_string)
        counter += 1
        print(os.path.basename(use_string))
        bpy.data.actions[0].name = os.path.basename(use_string) 
           
        add_root_bone()
        fixBones()
        scaleAll()
        copyHips()
            
        if  counter != use_num:
            deleteArmeture()
            
        else: 
            pass           
            
    bpy.context.area.ui_type = 'TEXT_EDITOR'


if __name__ == "__main__":
    
    get_all_anims()
    
    #tHIS LOOPS THROUGH ALL OUR ACTIONS AND CREATES NLA STRIPS.
    for action in bpy.data.actions:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.area.type = 'DOPESHEET_EDITOR'
        
        bpy.context.space_data.ui_mode = 'ACTION'
        bpy.context.selected_objects[0].animation_data.action = action
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.area.type = 'DOPESHEET_EDITOR'
        
        bpy.context.space_data.ui_mode = 'ACTION'
        bpy.ops.action.push_down()
       
       
