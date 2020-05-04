#!/usr/bin/env python
#
#            ########   ######     ##    ##  #######   ######  ########  #######                  
#            ##     ## ##    ##     ##  ##  ##     ## ##    ##    ##    ##     ##           
#            ##     ## ##            ####   ##     ## ##          ##    ##     ##        
#            ########   ######        ##    ##     ## ##          ##    ##     ##       
#            ##   ##         ##       ##    ##     ## ##          ##    ##     ##      
#            ##    ##  ##    ##       ##    ##     ## ##    ##    ##    ##     ##        
#            ##     ##  ######        ##     #######   ######     ##     #######         
#
#
#
# Robin Sebstian (https://github.com/robseb)
#
#
# Python Script to automatically create a Bitbake recipe for Python PiP Packages
# This recipe can then be used inside a meta layer for embedded Linux building with 
# the Yocto Project
#
# (2019-12-28) Vers.1.0 
#   first Version 

version = "1.004"

import os
import sys
import time
from datetime import datetime

try:
    import dload

except ImportError as ex:
    print('Msg: '+str(ex))
    print('This Python Application requirers "dload"')
    print('Use following pip command to install it:')
    print('==> pip install dload --no-cache-dir')
    sys.exit()


#rom git import RemoteProgress
import subprocess
import shutil
from subprocess import Popen, PIPE
import stat
import distutils.dir_util
import distutils.file_util 

#
#
#
############################################ Const ###########################################
#
#
#   
GITNAME          = "NIOSII_EclipseCompProject"
GIT_SCRIPT_URL   = "https://github.com/robseb/NIOSII_EclipseCompProject"

GIT_FREERTOS_URL = "https://github.com/FreeRTOS/FreeRTOS-Kernel.git"
GIT_HWLIB_URL    = "https://github.com/robseb/hwlib.git"

QURTUS_DEF_FOLDER       = "intelFPGA"
QURTUS_DEF_FOLDER_LITE  = "intelFPGA_lite"


SPLM = ['/','\\'] # Linux, Windows 
SPno = 0
NIOS_CMD_SHEL = ['nios2_command_shell.sh','Nios II Command Shell.bat']


DEMO_NAME_FREERTOSC = 'freertos_c1'

#
#
#
############################################ Github clone function ###########################################
#
#
#

# @brief to show process bar during github clone
#
#
'''
class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            sys.stdout.write("\033[F")
            print("    "+message)
'''
# @brief Copy cloned Github repository over an local temp folder to a final 
#        destination to remove write restricted files 
#
#
def copy_git_windows_frindy(source,temp, fileTemp,dest):

    os.mkdir(fileTemp)
    os.chmod(fileTemp, stat.S_IWRITE)

    try:
        for name in os.listdir(source):
            if  os.path.abspath(name):
                if(not name == ".git") and (not name == ".github") and (not name == ".gitignore"):
                    print('      '+name)
                    if(os.path.isdir(source+SPLM[SPno]+name)):
                        distutils.dir_util.copy_tree(source+SPLM[SPno]+name,temp+SPLM[SPno]+name)
                    else:
                        shutil.copy2(source+SPLM[SPno]+name,fileTemp)
    except Exception as ex:
        raise Exception('ERROR: Failed to copy github project files to local folder! Msg:'+str(ex))
    try:
        
        distutils.dir_util.copy_tree(fileTemp,temp+SPLM[SPno]+'source')

        distutils.dir_util.copy_tree(temp,dest)
    except Exception as ex:
        raise Exception('ERROR: Failed to copy Folder to the Quartus Project! Msg:'+str(ex))
    try:
        if(os.path.isdir(temp)):
            shutil.rmtree(temp, ignore_errors=False) 
        if(os.path.isdir(fileTemp)):
            shutil.rmtree(fileTemp, ignore_errors=False) 
    except Exception as ex:
        raise Exception('ERROR: Failed to remove the local temp folder! Msg: '+str(ex))

#
#
#
############################################ TCL File generation  ###########################################
#
#
#


#
# @brief Generate TCL script header for Software Components 
#
#
def generate_tcl_file_header_package(FileName,PackageName,VersionNo,BspSubdir):
    return '#                                                                \n'+ \
           '# '+FileName+'\n'+ \
           '#                                                                \n'+ \
           '# Auto generated TCL Script by "'+GITNAME+'.py"  in Vers: '+str(version)+'\n'+ \
           '# Date: '+str(datetime.now())+ '\n'+  \
           '# designed by Robin Sebastian (https://github.com/robseb) \n'+ \
           '#                                                                \n'+ \
           '# Script for adding the Software package "'+PackageName+'" in Version '+VersionNo+'\n'+ \
           '#                                                                \n'+ \
           '                                                                 \n'+ \
           '# Create new software package named "'+PackageName+'"            \n'+ \
           'create_sw_package '+PackageName+'                                \n'+ \
           '                                                                 \n'+ \
           '# The version Number of this software                            \n'+ \
           'set_sw_property version '+VersionNo+'                             \n'+ \
           '                                                                 \n'+ \
           '# Location to copy the source code to it                         \n'+ \
           'set_sw_property bsp_subdirectory '+BspSubdir+'                    \n'+ \
           '                                                                 \n'+ \
           '                                                                 \n'

#
# @brief Generate TCL script header for Operating Systems Components 
#
#
def generate_tcl_file_header_os(FileName,OSName,DisplayName,VersionNo,BspSubdir):
    return '#                                                                \n'+ \
           '# '+FileName+'\n'+ \
           '#                                                                \n'+ \
           '# Auto generated TCL Script by "'+GITNAME+'.py"                  \n'+ \
           '# Date: '+str(datetime.now())+ '\n'+  \
           '# designed by Robin Sebastian (https://github.com/robseb) \n'+ \
           '#                                                                \n'+ \
           '# Script for generating a new operating system: "'+OSName+'" in Version '+VersionNo+'\n'+ \
           '#                                                                \n'+ \
           '                                                                 \n'+ \
           '# Create new OS called "'+OSName+'"                              \n'+ \
           'create_os '+OSName+'                                             \n'+ \
           '                                                                 \n'+ \
           '# Chose UI Display Name: "'+DisplayName+'"                       \n'+ \
           'set_sw_property display_name '+DisplayName+'                      \n'+ \
           '                                                                 \n'+ \
           '# The OS should extends the HAL BSP                              \n'+ \
           'set_sw_property extends_bsp_type HAL                             \n'+ \
           '                                                                 \n'+ \
           '# The version Number of this software                            \n'+ \
           'set_sw_property version '+VersionNo+'                             \n'+ \
           '                                                                 \n'+ \
           '# Location in generated BSP that above sources will be copied into \n'+ \
           'set_sw_property bsp_subdirectory '+ OSName+'                     \n' + \
           '                                                                 \n'+ \
           '# Enable preemtion Interupt support for the OS                   \n'+ \
           'set_sw_property isr_preemption_supported true                    \n'+ \
           '                                                                 \n'+ \
           '                                                                 \n'
#
# @brief Global Variable for adding the include paths to the TCL script
#
#
class glob:
    TCL_Header_include_path_list = []

#
# @brief Check the in "generate_tcl_file_sources" founded file and write 
#        them to the TCL script file
#
def add_files_to_list(fileName,pathRel,MainFolder):
    pathRel = pathRel.replace('\\','/')
    folderPath = pathRel[1:]
    locFilePath    = folderPath+'/'+fileName

    tcl_str = ''
    if fileName.endswith('.c'):
        tcl_str= tcl_str+'add_sw_property c_source '+locFilePath+' \n'
    elif fileName.endswith('.h'):
        tcl_str= tcl_str+'add_sw_property include_source '+locFilePath+' \n' 
        if not folderPath in glob.TCL_Header_include_path_list:
            glob.TCL_Header_include_path_list.append(folderPath)
    elif fileName.endswith('.S'):
        tcl_str= tcl_str+'add_sw_property asm_source '+locFilePath+' \n'
        
    return tcl_str

#
# @brief Add the path of every available file inside a folder structure to the 
#        TCL script file 
#
def generate_tcl_file_sources(folderSourceAbs,MainFolder):
    tcl_str ='\n###### \n'+ \
             '# Source file listing     \n'+ \
             '###### \n'+'\n' 
    print('--> Progress every file in folder structure "'+MainFolder+'\n"')
   
    # Find every file in every folders 
    try:
        depthList = []
        depthListAbs = []
        depthPath =[]
        listOfProgressedFolders =[]
        listOfProgressedFiles =[]
        pathsuffix= ''
        pathsuffix_old =''
        MultiJump =False

        while True:
            folderList =[]
            for file in os.listdir(folderSourceAbs+pathsuffix):
               
                if(os.path.isfile(folderSourceAbs+pathsuffix+SPLM[SPno]+file)):
                    # Progress File 
                    if( (not folderSourceAbs+pathsuffix+SPLM[SPno]+file in listOfProgressedFiles)):
                        print('    File: '+file)
                        tcl_str = tcl_str+ add_files_to_list(file,pathsuffix,MainFolder)
                        listOfProgressedFiles.append(folderSourceAbs+pathsuffix+SPLM[SPno]+file)
                elif ( not folderSourceAbs+pathsuffix+SPLM[SPno]+file in listOfProgressedFolders):
                    # Add folder to the list
                    print('    Folder: '+file)
                    folderList.append(file)

            # Some folders in current level found
            if not (len(folderList) ==0):
                tcl_str=tcl_str+'\n'
                curFolder = folderList[-1]
                
                # Save absolute folder path for depth tracking  
                folderListAbs =[]
                for obj in folderList:
                    folderListAbs.append(folderSourceAbs+pathsuffix+SPLM[SPno]+obj)
                depthListAbs.append(folderListAbs)
                
                listOfProgressedFolders.append(folderSourceAbs+pathsuffix+SPLM[SPno]+curFolder)
                pathsuffix_old = SPLM[SPno]+curFolder
                pathsuffix = pathsuffix+ pathsuffix_old
                print('    --> '+ pathsuffix)

                # Add folders to depth list
                depthList.append(folderList)

                MultiJump = False

            elif (not len(depthList) == 0):
                pathsuffix=pathsuffix.replace(pathsuffix_old,'')
                print('    <-- '+ pathsuffix)
                tcl_str=tcl_str+'\n'   
                
                # Multi Jump to a other path required 
                if(MultiJump):
                    #Find a folder that is not progressed jet
                    tempC =0
                    len2goBack =0
                    Folder2find = ''
                    for deep in depthListAbs[:]:
                        tempC = tempC+1
                        for l in deep:
                            if not l is listOfProgressedFolders:
                                len2goBack = tempC
                                Folder2find = l
                                break
                        if not Folder2find=='':
                            break

                    if(Folder2find == ''):
                        break
                    
                    Folder2find = Folder2find.replace(folderSourceAbs,'')

                    pathsuffix = Folder2find
                    listOfProgressedFolders.append(pathsuffix)
                    print('    <<<<---- '+pathsuffix)
                
                # Go a single level back 
                del depthList[-1]
                MultiJump = True

            else:
                break

    except Exception as ex:
        raise Exception('ERROR: Failed to read ! Msg:'+str(ex))
    print('    ==== File processing done ====\n')

    print('--> Generate include folders for "'+MainFolder+'"')

    tcl_str=tcl_str+'\n\n'+      \
    '#                      \n'+ \
    '## Include paths       \n'+ \
    '#                      \n'

    for incl in glob.TCL_Header_include_path_list:
        print('   Add include path: '+incl)
        tcl_str = tcl_str+ 'add_sw_property include_directory '+ incl+ '\n'


    glob.TCL_Header_include_path_list = []
    return tcl_str


#
#
#
############################################ XML Template File generation  ###########################################
#
#
#

#
# @brief Generate the XML Template File for the Demo project 
#        TCL script file 
#
def generate_xml_template_file(DemoName,AppName,BSPname,TypeName,DemoDesc):
    return     '<?xml version="1.0" encoding="UTF-8"?>      \n' +\
               '<template_settings>                         \n' +\
	           '    <template                               \n' +\
		       '        	name="'+DemoName+'"             \n' +\
		       '            description="'+DemoDesc+'"      \n' +\
		       '            file_to_open="main.c"           \n' +\
               '            details=" Demo project for working with FreeRTOS and Intel hwlib. \n' + \
               '            \\n                              \n'+\
               '                      This project was auto generated by the Python Script '+GITNAME+'.py \n' +\
               '                      (URL:'+GIT_SCRIPT_URL+'; Vers.:'+str(version)+'; Gen date:'+str(datetime.now())+') designed by Robin Sebastian\n' +\
               '                    ">                      \n'+\
               '    </template>                             \n'+\
               '    <stf>                                   \n'+\
		       '        <os_spec name="FreeRTOS">           \n'+\
			   '            <sw_component name="Intel hwlib" id="hwlib"> \n'+\
			   '            </sw_component>                 \n'+\
		       '        </os_spec>                          \n'+\
	           '  </stf>                                    \n'+\
               '  <create-this>                             \n'+\
		       '    <app name="'+AppName+'"                 \n'+\
			   '         nios2-app-generate-makefile-args=" --set OBJDUMP_INCLUDE_SOURCE 1 --src-files main.c "\n'+\
			   '         bsp="'+BSPname+'">                 \n'+\
		       '   </app>                                   \n'+\
               '   <bsp name="'+BSPname+'"                  \n'+\
			   '         type="'+TypeName+'"                \n'+\
			   '         nios2-bsp-args="--cmd enable_sw_package hwlib">  \n'+\
		       '  </bsp>                                    \n'+\
               ' </create-this>                             \n'+\
               '</template_settings>                        \n'



############################################                                ############################################
############################################             MAIN               ############################################
############################################                                ############################################
if __name__ == '__main__':

    print("\nAUTOMATIC SCRIPT FOR GENERATING A NIOS II BSP Layer")
    print(" with FreeRTOS, Intel hwlib  ")
    print(" by Robin Sebastian (https://github.com/robseb) Vers.: "+version+"\n")

    ############################################ Runtime environment check ###########################################

    # Runtime environment check
    if sys.version_info[0] < 3:
        print("Use Python 3 for this script!")
        sys.exit()

    ############################################ Find Quartus Installation Path #######################################
    
    if sys.platform =='linux':
        Quartus_Folder_def_suf_dir = os.path.join(os.path.join(os.path.expanduser('~'))) + '/'
        SPno = 0
    else: 
        Quartus_Folder_def_suf_dir = 'C:\\' 
        SPno = 1

    QURTUS_NIOSSHELL_DIR    = SPLM[SPno]+"nios2eds"+SPLM[SPno]+NIOS_CMD_SHEL[SPno]

    # 1.Step: Find the Qurtus installation path
    print('--> Try to find the default Quartus instalation path')

    quartus_standard_ver = False
    # Loop to dected the case that the free Version of EDS (EDS Standard [Folder:intelFPGA]) and 
    #    the free Version of Quartus Prime (Quartus Lite [Folder:intelFPGA_lite]) are installed together 
    while(True):
        if (os.path.exists(Quartus_Folder_def_suf_dir+QURTUS_DEF_FOLDER)) and (not quartus_standard_ver):
            Quartus_Folder=Quartus_Folder_def_suf_dir+QURTUS_DEF_FOLDER
            quartus_standard_ver = True
        elif(os.path.exists(Quartus_Folder_def_suf_dir+QURTUS_DEF_FOLDER_LITE)):
            Quartus_Folder=Quartus_Folder_def_suf_dir+QURTUS_DEF_FOLDER_LITE
            quartus_standard_ver = False
        else:
            print('ERROR: No Qurtus Installation Folder was found!')
            sys.exit()

        # 2.Step: Find the latest Quartus Version No.
        avlVer = []
        for name in os.listdir(Quartus_Folder):
            if  os.path.abspath(name):
                try:
                    avlVer.append(float(name))
                except Exception:
                    pass

        if (len(avlVer)==0):
            print('ERROR: No vailed Quartus Version was found')
            sys.exit()

        avlVer.sort(reverse = True) 

        highestVer = avlVer[0]
        Quartus_Folder = Quartus_Folder + SPLM[SPno]+ str(highestVer)   

        if (not(os.path.realpath(Quartus_Folder))):
            print('ERROR: No Qurtus Installation Folder was found!')
            sys.exit()


        # Check if the NIOS II Command Shell is available 
        if((not(os.path.isfile(Quartus_Folder+QURTUS_NIOSSHELL_DIR)) )):
            if( not quartus_standard_ver):
                print('ERROR: Intel NIOS II Command Shell was not found!')
                sys.exit()
        else:
            break

    print('     Following Quartus Installation Folder was found:')
    print('     '+Quartus_Folder)

    ############################### Check that the script runs inside the Github folder ###############################
    excpath = os.getcwd()
    try:
    
        if(len(excpath)<len(GITNAME)):
            raise Exception()

        # Find the last slash in the execution path 
        slashpos =0
        for str_ in excpath:
            slashpos_pos=excpath.find(SPLM[SPno],slashpos)
            if(slashpos_pos == -1):
                break
            slashpos= slashpos_pos+len(SPLM[SPno])

        if(not excpath[slashpos:] == GITNAME):
             raise Exception()

        if(not os.path.isdir(os.getcwd()+SPLM[SPno]+'Demos')):
            raise Exception()

    except Exception:
        print('ERROR: The script was not executed inside the cloned Github folder')
        print('       Please clone this script from Github and execute the script')
        print('       directly inside the cloned folder!')
        print('URL: '+GIT_SCRIPT_URL)
        sys.exit()

    ##############################################  Input a project name ############################################## 

    #projectName = input('Please input a project name:')

    projectName= "Test"

    print ('Name: %s \n' % (projectName))
    
    print('Starting the generation...\n')

    ################################################ Create Project Folder ###########################################

    if( not (os.path.isdir(projectName))):
        os.mkdir(projectName)
        print('--> Create a new project folder')
    
    ################################################ Clone the latest FreeRTOS Version ###############################

    if(os.path.isdir(projectName+SPLM[SPno]+"FreeRTOS-Kernel")):
        print('--> FreeRTOS Kernel is available: pull the latest version')
        
        #g = git.cmd.Git(projectName+SPLM[SPno]+"FreeRTOS-Kernel")
        #g.pull()
    else:
        print('--> Clone the latest FreeRTOS Kernel Version \n')
        if( dload.git_clone(GIT_FREERTOS_URL, os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]) == 'Invalid clone_dir'):
            print('ERROR: The downloaded FreeRTOS Folder is not in a vialed format!')
            sys.exit()
        #git.Repo.clone_from(GIT_FREERTOS_URL, projectName+SPLM[SPno]+"FreeRTOS-Kernel", progress=CloneProgress())
        if(os.path.isdir(os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'FreeRTOS-Kernel-master')):
            os.rename(os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'FreeRTOS-Kernel-master',os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'FreeRTOS-Kernel')
    	

    ########################################### Check if the FreeRTOS format is okay ################################

    print('--> Check if the FreeRTOS folder looks okay')
    if(not (os.path.isdir(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable")) and (os.path.isdir(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"include"))
    and (os.path.isdir(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable"+SPLM[SPno]+"GCC"))and (os.path.isdir(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable"+SPLM[SPno]+"GCC"+SPLM[SPno]+"NiosII"))):
        print('ERROR: The downloaded FreeRTOS Folder is not in a vialed format!')
        sys.exit()
    else:
        print('    looks okay')

    ########################################### Remove BSP driver for other Platforms ###############################

    # 1. Step: Remove support for other compilers (Only the GCC complier should be supported)
    print('--> Remove support of diffrent compliers as GCC')
    
    # Allow only the folder "GCC" and "MemMang" inside /FreeRTOS-Kernel/portable
    for name in os.listdir(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable"):
        if  os.path.abspath(name):
            if (not (name == 'GCC')):
                if (not (name == 'MemMang')):
                    if (os.path.isdir(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable"+SPLM[SPno]+name)):
                        try:
                            shutil.rmtree(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable"+SPLM[SPno]+name)
                        except Exception as ex:
                            print('Msg: '+str(ex))
                            print('Warning: Failed to delate folder: /FreeRTOS-Kernel/portable/'+name)
    
    # 2. Step: Remove support for other platform
    print('--> Remove support of diffrent Platform as Intel NIOS II')
    # Alow only the NIOS II folder inside /FreeRTOS-Kernel/portable/GCCs
    for name in os.listdir(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable"+SPLM[SPno]+"GCC"):
        if  os.path.abspath(name):
            if (not (name == 'NiosII')):
                if (os.path.isdir(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable"+SPLM[SPno]+"GCC"+SPLM[SPno]+name)):
                    try:
                        shutil.rmtree(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable"+SPLM[SPno]+"GCC"+SPLM[SPno]+name)
                    except Exception as ex:
                        print('Msg: '+str(ex))
                        print('Warning: Failed to delate folder: /FreeRTOS-Kernel/portable/GCC/'+name)

    # 3. Step: Remove vintage FreeRTOS Memory Management
    if(os.path.isdir(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable"+SPLM[SPno]+"MemMang")):
        print('--> Remove vintage Memory Management')
        try:
            if (os.path.isfile(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable"+SPLM[SPno]+"MemMang"+SPLM[SPno]+"heap_1.c")):
                os.remove(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable"+SPLM[SPno]+"MemMang"+SPLM[SPno]+"heap_1.c")
            if (os.path.isfile(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable"+SPLM[SPno]+"MemMang"+SPLM[SPno]+"heap_2.c")):
                os.remove(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable"+SPLM[SPno]+"MemMang"+SPLM[SPno]+"heap_2.c")
        except Exception as ex:
            print('Msg: '+str(ex))
            print('Warning: Failed to delate vintage memory management files')


    ################################################ Clone the latest hwlib Version ###############################

    if(os.path.isdir(projectName+SPLM[SPno]+"hwlib")):
        print('--> hwlib is available: pull the latest version')
        #g = git.cmd.Git(projectName+SPLM[SPno]+"hwlib")
        #g.pull()
    else:
        print('--> Clone the latest hwlib Version \n')
        dload.git_clone(GIT_HWLIB_URL, os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno])

        #git.Repo.clone_from(GIT_HWLIB_URL, projectName+SPLM[SPno]+"hwlib", progress=CloneProgress())
        if(os.path.isdir(os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'hwlib-master')):
            os.rename(os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'hwlib-master',os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'hwlib')

    ########################################### Check if the hwlib format is okay ################################

    print('--> Check if the hwlib folder looks okay')
    if(not (os.path.isdir(projectName+SPLM[SPno]+"hwlib"))):
        print('ERROR: The downloaded hwlib Folder is not in a vialed format!')
        sys.exit()
    else:
        print('    looks okay')

    
    ################################################ Set Quartus Folder Directories ###############################

    Quartus_componet_folder = Quartus_Folder+SPLM[SPno]+'nios2eds'+SPLM[SPno]+'components'
    Quartus_example_folder  = Quartus_Folder+SPLM[SPno]+'nios2eds'+SPLM[SPno]+'examples'+SPLM[SPno]+'software'


    ######################################### Copy to the Quartus component folder ################################
   
    # 1. Step: Copy the FreeRTOS Kernel to the component folder
    
   
    if(os.path.isdir(Quartus_componet_folder+SPLM[SPno]+'FreeRTOS')):
        print('--> Remove old component folder: FreeRTOS')
        try:
            shutil.rmtree(Quartus_componet_folder+SPLM[SPno]+'FreeRTOS', ignore_errors=False) 
        except Exception as ex:
            print('ERROR: Failed to remove the old FreeRTOS Quartus Component folder!')
            print('Msg: '+str(ex))
            sys.exit()

    print('--> Generate FreeRTOS Kernel code file structure and')
    print('    Copy the FreeRTOS Kernel to the Quartus Component folder')

    try:
        copy_git_windows_frindy(os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'FreeRTOS-Kernel',os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'FreeRTOS'+SPLM[SPno],
                            os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'source',Quartus_componet_folder+SPLM[SPno]+'FreeRTOS')
    except Exception as ex:
        print('Error during FreeRTOS-Kernel data processing')
        print(str(ex))
        sys.exit()

    # 2. Step: Copy the hwlib to the component folder

    if(os.path.isdir(Quartus_componet_folder+SPLM[SPno]+'hwlib')):
        print('--> Remove old component folder: hwlib')
        try:
            shutil.rmtree(Quartus_componet_folder+SPLM[SPno]+'hwlib')
        except Exception as ex:
            print('ERROR: Failed to remove the old hwlib Quartus Component folder!')
            print('Msg: '+str(ex))
            sys.exit()

    print('--> Generate hwlib Kernel code file structure and')
    print('    Copy the FreeRTOS Kernel to the Quartus Component folder')

    try:
        copy_git_windows_frindy(os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'hwlib',os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'hwlibNIOS'+SPLM[SPno],
                            os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'top'+SPLM[SPno],Quartus_componet_folder+SPLM[SPno]+'hwlib')
    except Exception as ex:
        print('Error during FreeRTOS-Kernel data processing')
        print(str(ex))
        sys.exit()

    
    ################################################# Generate the TCL scripts #################################################
    
    # ==================================== HWLIB TCL SCRIPT ====================================
    # 1.Step: Create TCL component file for 'hwlib'
    print('--> Generate TCL component TCL script for hwlib')
    tcl_hwlib_str = ''

    # 1.a: Create file header for Component files 
    tcl_hwlib_str= tcl_hwlib_str+ generate_tcl_file_header_package('hwlib_sw.tcl','hwlib',str(highestVer),'hwlib')

    # 1.b: Add files to import to the TCL script
    try:
        tcl_hwlib_str= tcl_hwlib_str+ generate_tcl_file_sources(Quartus_componet_folder+SPLM[SPno]+'hwlib','hwlib')
    except Exception as ex:
        print('ERROR: Failed to generate the hwlib TCL script file!')
        print('Msg: '+str(ex))
        sys.exit()

    # 1.c: Link hwlib together with FreeRTOS
    tcl_hwlib_str=tcl_hwlib_str+'\n\n' +\
    '# Support only FreeRTOS\n' + \
    'add_sw_property supported_bsp_type FreeRTOS \n'

    # Remove the old TCL script file
    if(os.path.isfile(Quartus_componet_folder+SPLM[SPno]+'hwlib'+SPLM[SPno]+"hwlib_sw.tcl")):
        os.remove(Quartus_componet_folder+SPLM[SPno]+'hwlib'+SPLM[SPno]+"hwlib_sw.tcl")

    with open(Quartus_componet_folder+SPLM[SPno]+'hwlib'+SPLM[SPno]+"hwlib_sw.tcl","a") as f:
        f.write(tcl_hwlib_str)

    print('   Generatation of TCL component TCL script for hwlib done')

    # ==================================== FREERTOS TCL SCRIPT ===================================
    print('--> Generate TCL component TCL script for the FreeRTOS Kernel')
    tcl_freeRTOS_str = ''

    # 2.a: Create file header for OS files 
    tcl_freeRTOS_str= tcl_freeRTOS_str+ generate_tcl_file_header_os('FreeRTOS_sw.tcl','FreeRTOS','FreeRTOS robseb',str(highestVer),'FreeRTOS')

    # 2.b: Add files to import to the TCL script
    try:
        tcl_freeRTOS_str= tcl_freeRTOS_str+ generate_tcl_file_sources(Quartus_componet_folder+SPLM[SPno]+'FreeRTOS','FreeRTOS')
    except Exception as ex:
        print('ERROR: Failed to generate the FreeRTOS TCL script file!')
        print('Msg: '+str(ex))
        sys.exit()


    # Remove the old TCL script file
    if(os.path.isfile(Quartus_componet_folder+SPLM[SPno]+'FreeRTOS'+SPLM[SPno]+"FreeRTOS_sw.tcl")):
        os.remove(Quartus_componet_folder+SPLM[SPno]+'FreeRTOS'+SPLM[SPno]+"FreeRTOS_sw.tcl")

    with open(Quartus_componet_folder+SPLM[SPno]+'FreeRTOS'+SPLM[SPno]+"FreeRTOS_sw.tcl","a") as f:
        f.write(tcl_freeRTOS_str)

    print('   Generatation of TCL OS TCL script for FreeRTOS done')

    ################################################## Generate Demo project Files #################################################

    print('--> Copy Demo files to the Quartus Example folder')


    if(os.path.isdir(Quartus_example_folder+SPLM[SPno]+DEMO_NAME_FREERTOSC)):
        print('--> Remove old component folder: '+DEMO_NAME_FREERTOSC)
        try:
            shutil.rmtree(Quartus_example_folder+SPLM[SPno]+DEMO_NAME_FREERTOSC)
        except Exception as ex:
            print('ERROR: Failed to remove the old'+DEMO_NAME_FREERTOSC+' Quartus Example folder!')
            print('Msg: '+str(ex))
            sys.exit()

   
                       

    try:
        distutils.dir_util.copy_tree(os.getcwd()+SPLM[SPno]+'Demos'+SPLM[SPno]+DEMO_NAME_FREERTOSC,Quartus_example_folder+SPLM[SPno]+DEMO_NAME_FREERTOSC)
    except Exception as ex:
        print('Error during Example Project folder data processing')
        print(str(ex))
        sys.exit()



    ################################################ Generate XML Demo project File ################################################

    print('--> Generate XML Demo project template File')

    xml_file = generate_xml_template_file('FreeRTOS - robseb','freertos_robseb','freertos_hwlib','freertos','FreeRTOS Demo with hwlib')

    # Remove the old TCL script file
    if(os.path.isfile(Quartus_example_folder+SPLM[SPno]+DEMO_NAME_FREERTOSC+SPLM[SPno]+"template.xml")):
        os.remove(Quartus_example_folder+SPLM[SPno]+DEMO_NAME_FREERTOSC+SPLM[SPno]+"template.xml")

    with open(Quartus_example_folder+SPLM[SPno]+DEMO_NAME_FREERTOSC+SPLM[SPno]+"template.xml","a") as f:
        f.write(xml_file)


    ##################################################### Wait for user input #####################################################

    print('wait for input ...')
    x = input('')

    ############################################ NIOS II-Commnad Shell: Execute TCL Scripts ####################################
    print('--> Open the Intel NIOS II Command Shell')
    try:
        with Popen(Quartus_Folder+QURTUS_NIOSSHELL_DIR,stdin=subprocess.PIPE) as niosCmdSH:

            # Navigate to the Quartus Project folder
            print('--> Navigate to the Quartus Project Folder')
            if sys.platform =='linux':
                b = bytes(' cd '+Quartus_componet_folder+"\n", 'utf-8')
            else:
                if(quartus_standard_ver):
                    b = bytes(' cd C:/'+QURTUS_DEF_FOLDER+'/'+str(highestVer)+'/nios2eds/components'"\n", 'utf-8')
                else:
                    b = bytes(' cd C:/'+QURTUS_DEF_FOLDER_LITE+'/'+str(highestVer)+'/nios2eds/components'"\n", 'utf-8')
            niosCmdSH.stdin.write(b) 

            #b = bytes('ls -la\n', 'utf-8')
            #niosCmdSH.stdin.write(b) #expects a bytes type object

            print('--> Generate now Eclipse for NIOS components by executing the tcl scripts')
            b = bytes('ip-make-ipx --source-directory=. --output=components.ipx\n', 'utf-8')
            niosCmdSH.stdin.write(b)
        
            niosCmdSH.communicate()
    except Exception as ex:
       print('ERROR: Failed to start the Intel NIOS II Command Shell! '+ str(ex))
       sys.exit()

    

print('\n----------------------------------------------------------------------------')
print(' .. Script end.. \n')
