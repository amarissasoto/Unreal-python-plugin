from unreal import (
    AssetToolsHelpers,
    AssetTools,
    EditorAssetLibrary,
    Material,
    MaterialFactoryNew,
    MaterialProperty,
    MaterialEditingLibrary,
    MaterialExpressionTextureSampleParameter2D as TexSample2D,
    AssetImportTask,
    FbxImportUI
) #imports the list 

import os #imports os

class UnealUtility: #class for UnrealUility
    def __init__(self): #making init function
        self.substanceRootDir = "/game/Substance/" #makes the substance directory /game/Substance/
        self.baseMaterialName = "M_SubstanceBase" #makes base Material Name "M_SubstanceBase
        self.substanceTempDir = "/game/Substance/Temp/" #sets the substance tmp directory /game/Substance/Temp/
        self.baseMaterialPath = self.substanceRootDir + self.baseMaterialName #makes the base materials path
        self.baseColorName = "BaseColor" #names the base color map BaseColor
        self.normalName = "Normal" #names the normal map Normal
        self.occRoughnessMetalicName = "OcclusionRoughnessMetalic" #names the occRoughnessMetalic map OcclusionRoughnessMetalic

    def FindOrCreateBaseMaterial(self): #makes FindOrCreateBaseMaterial function
        if EditorAssetLibrary.does_asset_exist(self.baseMaterialPath): #checks to see if the library has base material
            return EditorAssetLibrary.load_asset(self.baseMaterialPath) #makes the base material and returns
        
        baseMat = AssetToolsHelpers.get_asset_tools().create_asset(self.baseMaterialName, self.substanceRootDir, Material, MaterialFactoryNew()) #makes baseMat variable 

        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 0) #makes baseColor variable
        baseColor.set_editor_property("parameter_name", self.baseColorName) #edits the base color name
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR)#plugs in the base color into the material's base color

        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 400) #makes normal variable
        normal.set_editor_property("parameter_name", self.normalName) #edits the normal map's name
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal")) #edits the base color properties 
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL) #plugs in the normal into the material's normal map

        occRoughnessMetalic = MaterialEditingLibrary.create_material_expression(baseMat,TexSample2D, -800, 800) #makes occRoughnessMetalic variable
        occRoughnessMetalic.set_editor_property("parameter_name", self.occRoughnessMetalicName) #edits the occRoughnessMetalic's name
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION) #plugs in the occRoughnessMetalic into the material's ambient occlusion map
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "G", MaterialProperty.MP_ROUGHNESS) #plugs in the occRoughnessMetalic into the material's ambient roughness map
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "B", MaterialProperty.MP_METALLIC) #plugs in the occRoughnessMetalic into the material's ambient metallic map

        EditorAssetLibrary.save_asset(baseMat.get_path_name()) #saves the material
        return baseMat #returns the baseMat
    
    def LoadMeshFromPath(self, meshPath): #makes LoadMeshFromPath function
        print(f"trying to load mesh from path {meshPath}") #prints "trying to load mesh from path" to show in logs
        meshName = os.path.split(meshPath)[-1].replace(".fbx","") #makes the name of the mesh as the file"s name
        importTask = AssetImportTask() #makes importTask variable
        importTask.replace_existing = True #allows the import to replace existing imports
        importTask.filename = meshPath #makes the mesh's path the file's name
        importTask.destination_path = "/game/" + meshName #makes the import's destination /game/ meshname
        importTask.save = True #allows it to save the import
        importTask.automated = True #allows the import to be automated

        FbxImportOptions = FbxImportUI() #makes FbxImportOptions variable
        FbxImportOptions.import_mesh = True #imports the mesh
        FbxImportOptions.import_as_skeletal = False #does not import the rig
        FbxImportOptions.import_materials = False #does not import the materials
        FbxImportOptions.static_mesh_import_data.combine_meshes = True #combine the meshes when importing

        importTask.options = FbxImportOptions #makes the options on the import options

        AssetToolsHelpers.get_asset_tools().import_asset_tasks([importTask]) #imports
        return importTask.get_objects()[0] #returns the import task
    
    def LoadFromDir(self, fileDir): #makes a LoadFromDir function
        for file in os.listdir(fileDir): #a loop going though thr file directory
            if ".fbx" in file: #checks if the file is an fbx file
                self.LoadMeshFromPath(os.path.join(fileDir, file)) #loads the mesh