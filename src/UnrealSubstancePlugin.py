import tkinter.filedialog #imports tkinter.filedialog
from unreal import ToolMenus, ToolMenuContext, ToolMenuEntryScript, uclass, ufunction #imports tools from unreal
import sys #imports sys
import os #imports os
import importlib #imports importlib
import tkinter #imports tkinter

srcDir = os.path.dirname(os.path.abspath(__file__)) #gets the path of the script
if srcDir not in sys.path: #checks to see if the script is in the path
    sys.path.append(srcDir) #adds the path

import UnrealUtilities #imports UnrealUtilities
importlib.reload(UnrealUtilities) #reloads the UnrealUtilities to update it

@uclass() #allow unreal to read the class
class LoadFromDirEntryScript(ToolMenuEntryScript): #class for loading from directory
    @ufunction(override=True) #allows unreal to read the function and lets it override it
    def execute(self, context): #function to execute
        window = tkinter.Tk() #makes a window
        window.withdraw() #hides the window
        fileDir = tkinter.filedialog.askdirectory() #opens a window to select file directory
        window.destroy() #destroys the window
        UnrealUtilities.UnealUtility().LoadFromDir(fileDir) #loads the selected file

@uclass() #allow unreal to read the class
class BuildBaseMaterialEntryScript(ToolMenuEntryScript): #class to run the build base material script
    @ufunction(override=True) #allows unreal to read the function and lets it override it
    def execute(self, context: ToolMenuContext) -> None: #function to execute
        UnrealUtilities.UnealUtility().FindOrCreateBaseMaterial() #runs the build FindOrCreateBaseMaterial function 

class UnrealSubstancePlugin: #class for UnrealSubstancePlugin
    def __init__(self): #making init function
        self.subMenuName="SubstancePlugin" #names the sub menu
        self.subMenuLabel="Substance Plugin" #labels the sub menu
        self.InitUI() #runs InitUI function

    def InitUI(self): #making initUI function
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu") #finds the main menu
        self.subMenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", "SubstancePlugin", "Stubstance Plugin") #adds sub menu
        self.AddEntryScript("BuildBaseMaterail", "Build Base Material", BuildBaseMaterialEntryScript()) #makes button to run BuildBaseMaterialEntryScript
        self.AddEntryScript("LoadFromDir", "Load From Directory", LoadFromDirEntryScript()) #makes button to run LoadFromDirEntryScript
        ToolMenus.get().refresh_all_widgets() #refreshes the widgets

    def AddEntryScript(self, name, label, script: ToolMenuEntryScript): #making addentryscript function
        script.init_entry(self.subMenu.menu_name, self.subMenu.menu_name, "", name, label) # initialize the entry script
        script.register_menu_entry() #runs register menu entry

UnrealSubstancePlugin() #runs UnrealSubstancePlugin class