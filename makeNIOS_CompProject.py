#!/usr/bin/env python3.7
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
# Robin Sebastian (https://github.com/robseb)
#
#
# Python Script to automatically generate an Intel NIOS II Eclipse Project with FreeRTOS,
# the Intel hwlib for the SoC-FPGAs and more
#
# (2020-05-10) Vers.1.0 
#   first Version 
#
# (2020-06-05) Vers.1.01
#   Fixed Linux Support with PythonGit
#
# (2020-06-06) Vers.1.02
#   Windows 10 Quartus 19.1 with WSL support
#
# (2020-08-28) Vers.1.03
#   socfpgaHAL support for accessing Hard-IP with the NIOS II  
#
# (2020-09-13) Vers.1.04
#   Adding socfpgaHAL Demo project
#

version = "1.04"

import os
import sys
import time
from datetime import datetime
import io

if sys.platform =='linux':
    try:
        import git
        from git import RemoteProgress


    except ImportError as ex:
        print('Msg: '+str(ex))
        print('This Python Application requirers "git"')
        print('Use following pip command to install it:')
        print('==> pip3 install GitPython')
        sys.exit()
else:
    try:
        import dload

    except ImportError as ex:
        print('Msg: '+str(ex))
        print('This Python Application requirers "dload"')
        print('Use following pip command to install it:')
        print('==> pip3 install dload')
        sys.exit()

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
GITNAME            = "NIOSII_EclipseCompProject"
GIT_SCRIPT_URL     = "https://github.com/robseb/NIOSII_EclipseCompProject"

GIT_FREERTOS_URL   = "https://github.com/FreeRTOS/FreeRTOS-Kernel.git"
GIT_HWLIB_URL      = "https://github.com/robseb/hwlib.git"
GIT_SOCFPGAHAL_URL = "https://github.com/robseb/socfpgaHAL.git"


QURTUS_DEF_FOLDER       = "intelFPGA"
QURTUS_DEF_FOLDER_LITE  = "intelFPGA_lite"


SPLM = ['/','\\'] # Linux, Windows 
SPno = 0
NIOS_CMD_SHEL = ['nios2_command_shell.sh','Nios II Command Shell.bat']


DEMO_NAME_FREERTOSC = 'freertos_c1'
DEMO_NAME_SOCFPGAHALC = 'freertos_socfpgaHAL_c1'

#
#
#
############################################ Global ###########################################
#
#
#  

#
# @brief Global Variable for adding the include paths to the TCL script
#
#
class glob:
    TCL_Header_include_path_list = []
    hwlib_selection =0 # 1: add hwlib, 2: do not add 
    socfpgaHAL_selection =0
    customFolderName = []
    selectedTragedDevice= 0 # 1: CY5/A5, 2: A10

#
#
#
############################################ Github clone function ###########################################
#
#
#

if sys.platform =='linux':
    # @brief to show process bar during github clone
    #
    #

    class CloneProgress(RemoteProgress):
        def update(self, op_code, cur_count, max_count=None, message=''):
            if message:
                sys.stdout.write("\033[F")
                print("    "+message)

# @brief Copy cloned Github repository over a local temp folder to a final 
#        destination to remove write restricted files 
#
def copy_git_windows_friendly(source,temp, fileTemp,dest):

    try:
        if(os.path.isdir(fileTemp)):
            shutil.rmtree(fileTemp, ignore_errors=False) 
    except Exception as ex:
        raise Exception('ERROR: Failed to remove old local folder! Msg: '+str(ex))

    if sys.platform =='linux':
        os.makedirs(fileTemp, mode=0o777, exist_ok=False)
    else:
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
           '# Chosen UI Display Name: "'+DisplayName+'"                      \n'+ \
           'set_sw_property display_name '+DisplayName+'                     \n'+ \
           '                                                                 \n'+ \
           '# The OS should extends the HAL BSP                              \n'+ \
           'set_sw_property extends_bsp_type HAL                             \n'+ \
           '                                                                 \n'+ \
           '# The version Number of this software                            \n'+ \
           'set_sw_property version '+VersionNo+'                            \n'+ \
           '                                                                 \n'+ \
           '# Location in generated BSP that above sources will be copied into \n'+ \
           'set_sw_property bsp_subdirectory '+ OSName+'                     \n' + \
           '                                                                 \n'+ \
           '# Enable preemtion Interupt support for the OS                   \n'+ \
           'set_sw_property isr_preemption_supported true                    \n'+ \
           '                                                                 \n'+ \
           '                                                                 \n'


#
# @brief Check the in the "generate_tcl_file_sources" founded files and write 
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
    print('--> Progress every file in folder structure "'+MainFolder+'"\n')
   
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
                
                # Multi Jump to an other path required 
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
# @brief Add the path of every available file inside a folder structure to the 
#        TCL script file 
#
def generate_tcl_file_add_constBool(SysName,ValueName,Value,Description):
    return 'add_sw_setting boolean system_h_define '+SysName+' '+ValueName+' '+str(Value)+' "'+Description+'"\n'
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

    details ='                                      ---  rsYocto ---              \\n \n' + \
             '     AUTOMATIC GENERATED ECLIPSE FOR NIOS II PROJECT         \\n \n' + \
             '('+GIT_SCRIPT_URL+')\\n \n' + \
             '                                                              \\n \n' + \
             ' ------------------------------------------------------------ \\n \n' + \
             '          by Robin Sebastian (https://github.com/robseb)      \\n \n' + \
             '          Contact: git@robseb.de\\n \n' + \
             '      Vers.: '+version+' Generation: '+str(datetime.now())+'  \\n \n' + \
             '                                                              \\n \n' + \
             ' ------------------------------------------------------------\\n \n' + \
             '   Added Components:                                         \\n \n' + \
             '                              - FreeRTOS -latest             \\n \n'
    if(glob.hwlib_selection==1):
        details=details+'                              - hwlib -18.1             \\n \n'
    if(glob.socfpgaHAL_selection==1):
        details=details+'                              - socfpgaHAL             \\n \n'
    
    if len(glob.customFolderName)>0:
        for FolderName in glob.customFolderName:
             details=details+'                              - '+FolderName+' \\n \n'


    details=details+' ------------------------------------------------------------\\n \n' + \
                    '   Supported Device:                                         \\n \n'
    if(glob.selectedTragedDevice==1):
        details=details+'                             - Intel Cyclone V or Arria V SoC-FPGA \\n \n'
    elif(glob.selectedTragedDevice==2):
        details=details+'                             - Intel Arria 10 SoC-FPGA \\n \n'
    else: 
        details=details+'                             - universal Intel FPGA Family\\n \n'

    xml_str = '<?xml version="1.0" encoding="UTF-8"?>      \n' +\
               '<template_settings>                         \n' +\
	           '    <template                               \n' +\
		       '        	name="'+DemoName+'"             \n' +\
		       '            description="'+DemoDesc+'"      \n' +\
		       '            file_to_open="main.c"           \n' +\
               '            details="'+details+'">          \n'+\
               '    </template>                             \n'+\
               '    <stf>                                   \n'+\
		       '        <os_spec name="FreeRTOS">           \n'
    if(glob.hwlib_selection==1):
	    xml_str=xml_str+'            <sw_component name="Intel hwlib" id="hwlib"/> \n'
    if(glob.socfpgaHAL_selection==1):
	    xml_str=xml_str+'            <sw_component name="robseb socfpgaHAL" id="socfpgaHAL"/> \n'
    if len(glob.customFolderName)>0:
        for FolderName in glob.customFolderName:    
            xml_str=xml_str+'            <sw_component name="'+FolderName+'" id="'+FolderName+'"/> \n'
    
    xml_str=xml_str+'        </os_spec>                          \n'+\
	           '  </stf>                                    \n'+\
               '  <create-this>                             \n'+\
		       '    <app name="'+AppName+'"                 \n'+\
			   '         nios2-app-generate-makefile-args=" --set OBJDUMP_INCLUDE_SOURCE 1 --src-files main.c "\n'+\
			   '         bsp="'+BSPname+'">                 \n'+\
		       '   </app>                                   \n'+\
               '   <bsp name="'+BSPname+'"                  \n'
    # add only FreeRTOS
    if len(glob.customFolderName)==0 and  glob.hwlib_selection==2:
	    xml_str=xml_str+'        type="'+TypeName+'">                \n'
    else:
        xml_str=xml_str+'        type="'+TypeName+'"                \n'
    # add FreeRTOS + hwlib 
    if(glob.hwlib_selection==1) and len(glob.customFolderName)==0:
        xml_str=xml_str+'         nios2-bsp-args="--cmd enable_sw_package hwlib">  \n'
    if(glob.socfpgaHAL_selection==1) and len(glob.customFolderName)==0:
        xml_str=xml_str+'         nios2-bsp-args="--cmd enable_sw_package socfpgaHAL">  \n'
    # add FreeRTOS + user components 
    if len(glob.customFolderName)>0:
        if(glob.socfpgaHAL_selection==1):
            xml_str=xml_str+'         nios2-bsp-args="--cmd enable_sw_package socfpgaHAL">  \n'
        if(glob.hwlib_selection==1):
            xml_str=xml_str+'         nios2-bsp-args="--cmd enable_sw_package hwlib'
        if(glob.hwlib_selection!=1) and (glob.socfpgaHAL_selection!=1):
            xml_str=xml_str+'         nios2-bsp-args="'
        for FolderName in glob.customFolderName:
            xml_str=xml_str+' --cmd enable_sw_package '+FolderName
        xml_str=xml_str+' ">\n'
            
    xml_str=xml_str+'  </bsp>                                    \n'+\
               ' </create-this>                             \n'+\
               '</template_settings>                        \n'
    return xml_str
#
#
#
############################################ Selection Menu  ###########################################
#
#
#

def selection_menu(header1,header2, setitem1, setitem2 ):
    print('\n##############################################################################')
    print('# -> '+header1+' <- #')
    print('# -> '+header2+' <- #')
    print('#   1: '+setitem1)
    print('#   2: '+setitem2)
    print('------------------------------------------------------------------------------')
    print('Q,C = abort execution ')
    while True:
        nb = input('--> Please choose with 1 or 2 = ')
        if(nb == '1'):
            print('---->'+setitem1+'\n')
            return 0
        elif(nb == '2'):
            print('---->'+setitem2+'\n')
            return 1
        elif ((nb == 'C') or (nb == 'c') or (nb == 'Q') or (nb == 'q')):
            print('----> Abort execution of the script')
            sys.exit()
        print('! The input was invalid !')



############################################                                ############################################
############################################             MAIN               ############################################
############################################                                ############################################

if __name__ == '__main__':
    print('\n#############################################################################')
    print('#                                                                            #')
    print('#    ########   ######     ##    ##  #######   ######  ########  #######     #')        
    print('#    ##     ## ##    ##     ##  ##  ##     ## ##    ##    ##    ##     ##    #')          
    print('#    ##     ## ##            ####   ##     ## ##          ##    ##     ##    #')    
    print('#    ########   ######        ##    ##     ## ##          ##    ##     ##    #')   
    print('#    ##   ##         ##       ##    ##     ## ##          ##    ##     ##    #')  
    print('#    ##    ##  ##    ##       ##    ##     ## ##    ##    ##    ##     ##    #')    
    print('#    ##     ##  ######        ##     #######   ######     ##     #######     #') 
    print('#                                                                            #')
    print("#       AUTOMATIC SCRIPT FOR GENERATING AN ECLIPSE FOR NIOS II PROJECT       #")
    print("#                    WITH CUSTOM COMPONENTS,OS AND HAL,...                   #")
    print('#                                                                            #')
    print("#               by Robin Sebastian (https://github.com/robseb)               #")
    print('#                  Contact: git@robseb.de                                    #')
    print("#                            Vers.: "+version+"                                   #")
    print('#                                                                            #')
    print('##############################################################################\n\n')
    ############################################ Runtime environment check ###########################################

    # Runtime environment check
    if sys.version_info[0] < 3:
        print("Use Python 3 for this script!")
        sys.exit()

    ############################################ Find Quartus Installation Path #######################################
    
    print('--> Find the System Platform')

    if sys.platform =='linux':
        Quartus_Folder_def_suf_dir = os.path.join(os.path.join(os.path.expanduser('~'))) + '/'
        SPno = 0
    else: 
        Quartus_Folder_def_suf_dir = 'C:\\' 
        SPno = 1

    QURTUS_NIOSSHELL_DIR    = SPLM[SPno]+"nios2eds"+SPLM[SPno]+NIOS_CMD_SHEL[SPno]

    # 1.Step: Find the Quartus installation path
    print('--> Try to find the default Quartus installation path')

    quartus_standard_ver = False
    # Loop to detect the case that the free Version of EDS (EDS Standard [Folder:intelFPGA]) and 
    #    the free Version of Quartus Prime (Quartus Lite [Folder:intelFPGA_lite]) are installed together 
    while(True):
        if (os.path.exists(Quartus_Folder_def_suf_dir+QURTUS_DEF_FOLDER)) and (not quartus_standard_ver):
            Quartus_Folder=Quartus_Folder_def_suf_dir+QURTUS_DEF_FOLDER
            quartus_standard_ver = True
        elif(os.path.exists(Quartus_Folder_def_suf_dir+QURTUS_DEF_FOLDER_LITE)):
            Quartus_Folder=Quartus_Folder_def_suf_dir+QURTUS_DEF_FOLDER_LITE
            quartus_standard_ver = False
        else:
            print('ERROR: No Intel Quartus Installation Folder was found!')
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
            print('ERROR: No valid Quartus Version was found')
            sys.exit()

        avlVer.sort(reverse = True) 

        highestVer = avlVer[0]
        Quartus_Folder = Quartus_Folder + SPLM[SPno]+ str(highestVer)   

        if (not(os.path.realpath(Quartus_Folder))):
            print('ERROR: No Quartus Installation Folder was found!')
            sys.exit()


        # Check if the NIOS II Command Shell is available 
        if((not(os.path.isfile(Quartus_Folder+QURTUS_NIOSSHELL_DIR)) )):
            if( not quartus_standard_ver):
                print('ERROR: Intel NIOS II Command Shell was not found!')
                sys.exit()
        else:
            break

    print('        Following Quartus Installation Folder was found:')
    print('        '+Quartus_Folder)

    ############################### Check that the script runs inside the Github folder ###############################
    print('\n--> Check that the script runs inside the Github folder')
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

    ############################################  Inputs and user selection ############################################ 
    projectName= "working_folder"
    print('\n--> Working Folder Name: %s \n' % (projectName))
    '''
    # hwlib required ? 
    glob.hwlib_selection = selection_menu('Intel hwlib for using the peripheral HPS components ','of the Cyclone and Arria SoC-FPGA with the NIOS II',\
        'Install the hwlib','Do not pre-install the hwlib') +1

    glob.selectedTragedDevice= 0# 1: CY5/A5, 2: A10
    if(glob.hwlib_selection ==1):
        # Select the target device
        glob.selectedTragedDevice = selection_menu('Select the Intel SoC-FPGA Family',\
            '','Intel Cyclone V- or Arria V SoC-FPGA','Intel Arria 10 SoC-FPGA') +1
    '''
       
    # socfpgaHAL required ? 
    glob.socfpgaHAL_selection = selection_menu('Install the socfpgaHAL for accessing the peripheral hard-IP HPS components ',\
        'of a Cyclone SoC-FPGA with the NIOS II Core?','Install the socfpgaHAL','Do not pre-install the socfpgaHAL') +1

    glob.selectedTragedDevice= 0# 1: CY5/A5, 2: A10
    
    if(glob.socfpgaHAL_selection ==1):
        # Select the target device
        glob.selectedTragedDevice = selection_menu('Select the Intel SoC-FPGA Family','','Intel Cyclone V- or Arria V SoC-FPGA','Intel Arria 10 SoC-FPGA') +1
    
    if glob.selectedTragedDevice ==2:
        print('Error: The selected device is in this version not supported!')
        sys.exit()
  
    print('=====================>>> Starting the generation... <<<==================== \n')
    ################################################ Create Project Folder ###########################################

    if( not (os.path.isdir(projectName))):
        os.mkdir(projectName)
        print('--> Create a new project folder')
    
    ################################################ Clone the latest FreeRTOS Version ###############################

    if(os.path.isdir(projectName+SPLM[SPno]+"FreeRTOS-Kernel")):
        print('--> FreeRTOS Version is already available')

        if sys.platform =='linux':
            print('       Pull it from Github')
            g = git.cmd.Git(os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'FreeRTOS-Kernel')
            g.pull()
        
    else:
        print('--> Cloning the latest FreeRTOS Kernel Version ('+GIT_FREERTOS_URL+')\n')
        print('       please wait...')

        if sys.platform =='linux':
            try:
                git.Repo.clone_from(GIT_FREERTOS_URL,os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'FreeRTOS-Kernel', 
                branch='master', progress=CloneProgress())
            except Exception as ex:
                print('ERROR: The cloning failed! Error Msg.:'+str(ex))
                sys.exit()
        else:
            if( dload.git_clone(GIT_FREERTOS_URL, os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]) == 'Invalid clone_dir'):
                print('ERROR: The downloaded FreeRTOS Folder is not in a valid format!')
                sys.exit()
            if(os.path.isdir(os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'FreeRTOS-Kernel-master')):
                os.rename(os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'FreeRTOS-Kernel-master',os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'FreeRTOS-Kernel')
    	

    ########################################### Check if the FreeRTOS format is okay ################################

    print('--> Check if the FreeRTOS folders looks okay')
    if(not (os.path.isdir(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable")) and (os.path.isdir(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"include"))
    and (os.path.isdir(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable"+SPLM[SPno]+"GCC"))and (os.path.isdir(projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+"portable"+SPLM[SPno]+"GCC"+SPLM[SPno]+"NiosII"))):
        print('ERROR: The downloaded FreeRTOS Folder is not in a valid format!')
        sys.exit()
    else:
        print('    looks okay')

    ########################################### Remove BSP driver for other Platforms ###############################

    # 1. Step: Remove support for other compilers (Only the GCC complier should be supported)
    print('--> Remove support of different compilers as GCC')
    
    # Allow only the folder "GCC" and "MemMang" inside /FreeRTOS-Kernel/portable
    print('--> Allow only the folder "GCC" and "MemMang" inside /FreeRTOS-Kernel/portable')
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
    print('--> Remove support of different Platform as Intel NIOS II')
    # Allow only the NIOS II folder inside /FreeRTOS-Kernel/portable/GCCs
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
    if glob.hwlib_selection == 1:
        if(os.path.isdir(projectName+SPLM[SPno]+"hwlib")):
            print('--> hwlib Version is already available')
            if sys.platform =='linux':
                print('       Pull it from Github')
                g = git.cmd.Git(os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'hwlib')
                g.pull()
        else:
            print('--> Cloning the latest hwlib Version ('+GIT_HWLIB_URL+')\n')
            print('       please wait...')
            if sys.platform =='linux':
                try:
                    git.Repo.clone_from(GIT_HWLIB_URL,os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'hwlib', 
                    branch='master', progress=CloneProgress())
                except Exception as ex:
                    print('ERROR: The cloning failed! Error Msg.:'+str(ex))
                    sys.exit()
            else:
                dload.git_clone(GIT_HWLIB_URL, os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno])

                if(os.path.isdir(os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'hwlib-master')):
                    os.rename(os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'hwlib-master',os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'hwlib')

    ########################################### Check if the hwlib format is okay ################################
    if glob.hwlib_selection == 1:
        print('--> Check if the folders inside hwlib look okay')
        if(not (os.path.isdir(projectName+SPLM[SPno]+"hwlib"))):
            print('ERROR: The downloaded hwlib Folder is not in a valid format!')
            sys.exit()
        else:
            print('    looks okay')


    ################################################ Clone the latest socfpgaHAL Version ###############################
    if glob.socfpgaHAL_selection == 1:
        if(os.path.isdir(projectName+SPLM[SPno]+"socfpgaHAL")):
            print('--> socfpgaHAL Version is already available')
            if sys.platform =='linux':
                print('       Pull it from Github')
                g = git.cmd.Git(os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'socfpgaHAL')
                g.pull()
        else:
            print('--> Cloning the latest socfpgaHAL Version ('+GIT_SOCFPGAHAL_URL+')\n')
            print('       please wait...')
            if sys.platform =='linux':
                try:
                    git.Repo.clone_from(GIT_SOCFPGAHAL_URL,os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'socfpgaHAL', 
                    branch='master', progress=CloneProgress())
                except Exception as ex:
                    print('ERROR: The cloning failed! Error Msg.:'+str(ex))
                    sys.exit()
            else:
                dload.git_clone(GIT_SOCFPGAHAL_URL, os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno])

                if(os.path.isdir(os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'socfpgaHAL-master')):
                    os.rename(os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'socfpgaHAL-master',os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]+'socfpgaHAL')

    ########################################### Check if the socfpgaHAL format is okay ################################
    if glob.hwlib_selection == 1:
        print('--> Check if the folders inside socfpgaHAL look okay')
        if(not (os.path.isdir(projectName+SPLM[SPno]+"socfpgaHAL"))):
            print('ERROR: The downloaded socfpgaHAL Folder is not in a valid format!')
            sys.exit()
        else:
            print('    looks okay')


    ############################# Allow the user to add custom code to the project  ###############################
    print('\n###############################################################################')
    print('#                                                                              #')
    print('#           OPTIONAL: ADD CUSTOM COMPONENTS TO THE PROJECT                     #')
    print('#                                                                              #')
    print('#  At this point it is possible to generate for custom code a NIOS II Eclipse #')
    print('#  component to add the code to the final NIOS II Eclipse HAL project          #')
    print('#                                                                              #')
    print('#  Copy a folder with the code to the working folder                           #')
    print('#  for every folder will be a  NIOS II Eclipse component be generated and      #')
    print('#  it will be added to the final Demo project                                  #')
    print('#                                                                              #')
    print('#  Note: The folder name will be used as component name                        #')
    print('------------------------------------------------------------------------------')
    print('# The working folder:                                                          #')
    print(' '+os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno])
    print('------------------------------------------------------------------------------')
    _wait_ = input('Type anything to continue ... ')

    ######################################## Detect added custom folders ##########################################
    
    print('\n--> Detect added custom folders')
    for comFolders in os.listdir(os.getcwd()+SPLM[SPno]+ projectName+SPLM[SPno]):
        if(not(comFolders == 'hwlib') and (not(comFolders == 'FreeRTOS-Kernel')) \
             and (not(comFolders == 'socfpgaHAL'))):
            print('     Folder: '+comFolders)
            glob.customFolderName.append(comFolders)
    if len(glob.customFolderName) <=0:
            print('     No Folders detect')

    ################################################ Set Quartus Folder Directories ###############################
    print('------------------------------------------------------------------------------')
    Quartus_componet_folder = Quartus_Folder+SPLM[SPno]+'nios2eds'+SPLM[SPno]+'components'
    Quartus_example_folder  = Quartus_Folder+SPLM[SPno]+'nios2eds'+SPLM[SPno]+'examples'+SPLM[SPno]+'software'


    ############################## Copy the additional files to the FreeRTOS folder ###############################
    if(not (os.path.isdir("Additional"+SPLM[SPno]+'FreeRTOS'))):
        print('NOTE: No additional files for FreeRTOS available!')
    else:
        print('--> Copy additional files to the FreeRTOS folder')
        # Copy Source files to the main folder 
        if(os.path.isdir("Additional"+SPLM[SPno]+'FreeRTOS'+SPLM[SPno]+'src')):
            print('    Copy source files')
            try:
                distutils.dir_util.copy_tree(os.getcwd()+SPLM[SPno]+"Additional"+SPLM[SPno]+'FreeRTOS'+SPLM[SPno]+'src',
                        os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+"FreeRTOS-Kernel")
            except Exception as ex:
                print('Msg: '+str(ex))
                print('Error: Failed to copy additional source files to FreeRTOS-Kernel')
                sys.exit()
        
        # Replace the port.c file with additional/port.c file 
        if(os.path.isfile("Additional"+SPLM[SPno]+'FreeRTOS'+SPLM[SPno]+'portable'+SPLM[SPno]+'port.c')
            and os.path.isfile(os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+'portable'+SPLM[SPno]+'GCC'+SPLM[SPno]+'NiosII'+SPLM[SPno]+'port.c')):
            print('--> Replace the port.c file with additional/port.c file')
            try:
                os.remove(os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+'portable'+SPLM[SPno]+'GCC'+SPLM[SPno]+'NiosII'+SPLM[SPno]+'port.c')
                shutil.copy2(os.getcwd()+SPLM[SPno]+"Additional"+SPLM[SPno]+'FreeRTOS'+SPLM[SPno]+'portable'+SPLM[SPno]+'port.c',
                            os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+'portable'+SPLM[SPno]+'GCC'+SPLM[SPno]+'NiosII'+SPLM[SPno]+'port.c')
            except Exception as ex:
                print('Msg: '+str(ex))
                print('Error: Failed to copy additional source files to FreeRTOS-Kernel')
                sys.exit()

        # Copy everything else to the FreeRTOS/portable/NIOS_RTOS_HAL folder
        if(os.path.isdir("Additional"+SPLM[SPno]+'FreeRTOS'+SPLM[SPno]+'NIOS_RTOS_HAL')):
            print('--> Copy everything else to the FreeRTOS/portable/NIOS_RTOS_HAL folder')
            if(os.path.isdir(os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+'portable'+SPLM[SPno]+'NIOS_RTOS_HAL')):
                try:
                    shutil.rmtree(os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+'portable'+SPLM[SPno]+'NIOS_RTOS_HAL', ignore_errors=False) 
                except Exception as ex:
                    print('Msg: '+str(ex))
                    print('Error: Failed to delate the FreeRTOS-Kernel/portable/NIOS_RTOS_HAL folder')
                    sys.exit()
        
            os.mkdir(os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+'portable'+SPLM[SPno]+'NIOS_RTOS_HAL')
              
            try:
                distutils.dir_util.copy_tree(os.getcwd()+SPLM[SPno]+"Additional"+SPLM[SPno]+'FreeRTOS'+SPLM[SPno]+'NIOS_RTOS_HAL',
                        os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+'portable'+SPLM[SPno]+'NIOS_RTOS_HAL')
            except Exception as ex:
                print('Msg: '+str(ex))
                print('Error: Failed to copy additional source files to FreeRTOS-Kernel/portable folder')
                sys.exit()
    
        # Copy Include files to the main folder 
        if(os.path.isdir("Additional"+SPLM[SPno]+'FreeRTOS'+SPLM[SPno]+'inc')):
            print('    Copy include files')
            try:
                distutils.dir_util.copy_tree(os.getcwd()+SPLM[SPno]+"Additional"+SPLM[SPno]+'FreeRTOS'+SPLM[SPno]+'inc',
                        os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+"FreeRTOS-Kernel"+SPLM[SPno]+'include')
            except Exception as ex:
                print('Msg: '+str(ex))
                print('Error: Failed to copy additional include files to FreeRTOS-Kernel')
                sys.exit()

    ######################################### Copy to the Quartus component folder ################################
   
    # 1. Step: Copy the FreeRTOS Kernel to the component folder
    if(os.path.isdir(Quartus_componet_folder+SPLM[SPno]+'FreeRTOS')):
        print('\n--> Remove old component folder: FreeRTOS')
        try:
            shutil.rmtree(Quartus_componet_folder+SPLM[SPno]+'FreeRTOS', ignore_errors=False) 
        except Exception as ex:
            print('ERROR: Failed to remove the old FreeRTOS Quartus Component folder!')
            print('Msg: '+str(ex))
            sys.exit()

    print('--> Generate FreeRTOS Kernel code file structure and')
    print('    Copy the FreeRTOS Kernel to the Quartus Component folder')

    try:
        copy_git_windows_friendly(os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'FreeRTOS-Kernel',os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'FreeRTOS'+SPLM[SPno],
                            os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'source',Quartus_componet_folder+SPLM[SPno]+'FreeRTOS')
    except Exception as ex:
        print('Error during FreeRTOS-Kernel data processing')
        print(str(ex))
        sys.exit()

    if glob.hwlib_selection == 1:
        # 2. Step: Copy the hwlib to the component folder
        if(os.path.isdir(Quartus_componet_folder+SPLM[SPno]+'hwlib')):
            print('--> Remove old component folder: hwlib')
            try:
                shutil.rmtree(Quartus_componet_folder+SPLM[SPno]+'hwlib')
            except Exception as ex:
                print('ERROR: Failed to remove the old hwlib Quartus Component folder!')
                print('Msg: '+str(ex))
                sys.exit()

        print('--> Generate hwlib code file structure and')
        print('    Copy the hwlib to the Quartus Component folder')

        try:
            copy_git_windows_friendly(os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'hwlib',os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'hwlibNIOS'+SPLM[SPno],
                                os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'top'+SPLM[SPno],Quartus_componet_folder+SPLM[SPno]+'hwlib')
        except Exception as ex:
            print('Error during hwlib data processing')
            print(str(ex))
            sys.exit()

    if glob.socfpgaHAL_selection == 1:
        # 2. Step: Copy the socfpgaHAL to the component folder
        if(os.path.isdir(Quartus_componet_folder+SPLM[SPno]+'socfpgaHAL')):
            print('--> Remove old component folder: socfpgaHAL')
            try:
                shutil.rmtree(Quartus_componet_folder+SPLM[SPno]+'socfpgaHAL')
            except Exception as ex:
                print('ERROR: Failed to remove the old socfpgaHAL Quartus Component folder!')
                print('Msg: '+str(ex))
                sys.exit()

        print('--> Generate socfpgaHAL code file structure and')
        print('    Copy the socfpgaHAL to the Quartus Component folder')

        try:
            copy_git_windows_friendly(os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'socfpgaHAL',os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'socfpgaHALNIOS'+SPLM[SPno],
                                os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'top'+SPLM[SPno],Quartus_componet_folder+SPLM[SPno]+'socfpgaHAL')

        except Exception as ex:
            print('Error during hwlib data processing')
            print(str(ex))
            sys.exit()

    # 3. Step: Copy the custom user folders
    if len(glob.customFolderName)>0:
        print('\n--> Generate  component TCL script for custom user files')
        for FolderName in glob.customFolderName:
            if(os.path.isdir(Quartus_componet_folder+SPLM[SPno]+FolderName)):
                print('--> Remove old custom user component folder: '+FolderName)
                try:
                    shutil.rmtree(Quartus_componet_folder+SPLM[SPno]+FolderName)
                except Exception as ex:
                    print('ERROR: Failed to remove old custom user component folder: '+FolderName)
                    print('Msg: '+str(ex))
                    sys.exit()
            print('--> Generate the component "'+FolderName+'" code file structure and')
            print('    Copy it to the Quartus Component folder')
            try:
                copy_git_windows_friendly(os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+FolderName,os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+FolderName+'NIOS'+SPLM[SPno],
                                    os.getcwd()+SPLM[SPno]+projectName+SPLM[SPno]+'top'+SPLM[SPno],Quartus_componet_folder+SPLM[SPno]+FolderName)
            except Exception as ex:
                print('ERROR: during '+FolderName+' data processing')
                print(str(ex))
                sys.exit()

    
    ################################################# Generate the TCL scripts #################################################
    
    if glob.hwlib_selection == 1:
        # ==================================== HWLIB TCL SCRIPT ====================================
        # 1.Step: Create TCL component file for 'hwlib'
        print('\n--> Generate TCL component TCL script for hwlib')
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

        # 1.c: Link hwlib together with HAN and FreeRTOS and copy the code
        tcl_hwlib_str=tcl_hwlib_str+'\n\n' +\
        '# Support only FreeRTOS and the default Intel NIOS II HAL\n' + \
        'add_sw_property supported_bsp_type FreeRTOS \n' +\
        'add_sw_property supported_bsp_type HAL \n'

        # 1.d: Choose the selected target device 
        tcl_hwlib_str=tcl_hwlib_str+'\n\n' +\
        '# \n' + \
        '# General settings\n' + \
        '#\n'

        if(glob.selectedTragedDevice==1):
            tcl_hwlib_str=tcl_hwlib_str+generate_tcl_file_add_constBool('soc_cy_av','soc_cy_av',True,'Const for hwlib to select the target SoC-FPGA device')
        elif(glob.selectedTragedDevice==2):
            tcl_hwlib_str=tcl_hwlib_str+generate_tcl_file_add_constBool('soc_a10','soc_a10',True,'Const for hwlib to select the target SoC-FPGA device')
        
        
        # Remove the old TCL script file
        if(os.path.isfile(Quartus_componet_folder+SPLM[SPno]+'hwlib'+SPLM[SPno]+"hwlib_sw.tcl")):
            os.remove(Quartus_componet_folder+SPLM[SPno]+'hwlib'+SPLM[SPno]+"hwlib_sw.tcl")

        with open(Quartus_componet_folder+SPLM[SPno]+'hwlib'+SPLM[SPno]+"hwlib_sw.tcl","a") as f:
            f.write(tcl_hwlib_str)

        print('   Generatation of TCL component TCL script for hwlib done')


    if glob.socfpgaHAL_selection == 1:
        # ==================================== SOCFPGAHAL TCL SCRIPT ====================================
        # 1.Step: Create TCL component file for 'socfpgaHAL'
        print('\n--> Generate TCL component TCL script for socfpgaHAL')
        tcl_socfpgahal_str = ''

        # 1.a: Create file header for Component files 
        tcl_socfpgahal_str+= generate_tcl_file_header_package('socfpgaHAL_sw.tcl','socfpgaHAL',str(highestVer),'socfpgaHAL')

        # 1.b: Add files to import to the TCL script
        try:
            tcl_socfpgahal_str+= generate_tcl_file_sources(Quartus_componet_folder+SPLM[SPno]+'socfpgaHAL','socfpgaHAL')
        except Exception as ex:
            print('ERROR: Failed to generate the socfpgaHAL TCL script file!')
            print('Msg: '+str(ex))
            sys.exit()

        # 1.c: Link hwlib together with HAN and FreeRTOS and copy the code
        tcl_socfpgahal_str+='\n\n' +\
        '# Support only FreeRTOS and the robseb socfpgaHAL\n' + \
        'add_sw_property supported_bsp_type FreeRTOS \n' +\
        'add_sw_property supported_bsp_type socfpgaHAL \n'

        # 1.d: Choose the selected target device 
        tcl_socfpgahal_str=tcl_socfpgahal_str+'\n\n' +\
        '# \n' + \
        '# General settings\n' + \
        '#\n'

        if(glob.selectedTragedDevice==1):
            tcl_socfpgahal_str+=generate_tcl_file_add_constBool('soc_cy_av','soc_cy_av',True,'Const for socfpgaHAL to select the target SoC-FPGA device')
        elif(glob.selectedTragedDevice==2):
            tcl_socfpgahal_str+=generate_tcl_file_add_constBool('soc_a10','soc_a10',True,'Const for socfpgaHAL to select the target SoC-FPGA device')

        tcl_socfpgahal_str+=generate_tcl_file_add_constBool('SOCFPGAHAL_MODE_NIOS','SOCFPGAHAL_MODE_NIOS',True,'Const to use the Version for the NIOS II')

        # Remove the old TCL script file
        if(os.path.isfile(Quartus_componet_folder+SPLM[SPno]+'socfpgaHAL'+SPLM[SPno]+"socfpgaHAL_sw.tcl")):
            os.remove(Quartus_componet_folder+SPLM[SPno]+'socfpgaHAL'+SPLM[SPno]+"hwlib_sw.tcl")

        with open(Quartus_componet_folder+SPLM[SPno]+'socfpgaHAL'+SPLM[SPno]+"socfpgaHAL_sw.tcl","a") as f:
            f.write(tcl_socfpgahal_str)

        print('   Generatation of TCL component TCL script for socfpgaHAL done')


    # ==================================== FREERTOS TCL SCRIPT ===================================
    print('\n--> Generate TCL component TCL script for the FreeRTOS Kernel')
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

    # 2.c: Overdrive HAL files
    tcl_freeRTOS_str=tcl_freeRTOS_str+'\n\n' +\
    '# Overridden HAL files\n' + \
    'add_sw_property excluded_hal_source HAL/src/alt_irq_register.c \n' +\
    'add_sw_property excluded_hal_source HAL/inc/priv/alt_legacy_irq.h \n'+\
    'add_sw_property excluded_hal_source HAL/inc/priv/altera_avalon_timer_regs.h'+\
    'add_sw_property excluded_hal_source HAL/src/alt_env_lock.c\n' +\
    'add_sw_property excluded_hal_source HAL/src/alt_malloc_lock.c\n' +\
    'add_sw_property excluded_hal_source HAL/src/alt_exception_entry.S\n' +\
    'add_sw_property excluded_hal_source HAL/src/alt_exception_trap.S\n' +\
    'add_sw_property excluded_hal_source HAL/src/alt_irq_entry.S\n' +\
    'add_sw_property excluded_hal_source HAL/src/alt_software_exception.S\n' +\
    'add_sw_property excluded_hal_source HAL/inc/os/alt_hooks.h\n' +\
    'add_sw_property excluded_hal_source HAL/src/alt_exit.c\n' +\
    'add_sw_property excluded_hal_source HAL/src/alt_iic.c\n' +\
    'add_sw_property excluded_hal_source HAL/src/alt_main.c\n' +\
    'add_sw_property excluded_hal_source HAL/src/alt_tick.c\n' +\
    'add_sw_property excluded_hal_source HAL/src/alt_irq_handler.c\n' +\
    'add_sw_property excluded_hal_source HAL/inc/os/alt_sem.\n'

    # Remove the old TCL script file
    if(os.path.isfile(Quartus_componet_folder+SPLM[SPno]+'FreeRTOS'+SPLM[SPno]+"FreeRTOS_sw.tcl")):
        os.remove(Quartus_componet_folder+SPLM[SPno]+'FreeRTOS'+SPLM[SPno]+"FreeRTOS_sw.tcl")

    with open(Quartus_componet_folder+SPLM[SPno]+'FreeRTOS'+SPLM[SPno]+"FreeRTOS_sw.tcl","a") as f:
        f.write(tcl_freeRTOS_str)

    print('   Generatation of the TCL OS TCL script for FreeRTOS done')

    # ================================ TCL SCRIPTS FOR CUSTOM USER COMPONENTS ======================================
    if len(glob.customFolderName)>0:
        print('\n--> Generate TCL component TCL script for custom user files')
        for FolderName in glob.customFolderName:
            # 1.Step: Create TCL component file for the custom component 
            print('\n--> Generate TCL component TCL script for '+FolderName)
            tcl_hwlib_str = ''

            # 1.a: Create file header for Component files 
            tcl_hwlib_str= tcl_hwlib_str+ generate_tcl_file_header_package(FolderName+'_sw.tcl',FolderName,str(highestVer),FolderName)

            # 1.b: Add files to import to the TCL script
            try:
                tcl_hwlib_str= tcl_hwlib_str+ generate_tcl_file_sources(Quartus_componet_folder+SPLM[SPno]+FolderName,FolderName)
            except Exception as ex:
                print('ERROR: Failed to generate the '+FolderName+'TCL script file!')
                print('Msg: '+str(ex))
                sys.exit()

            # 1.c: Link hwlib together with HAN and FreeRTOS and copy the code
            tcl_hwlib_str=tcl_hwlib_str+'\n\n' +\
            '# Support only FreeRTOS and the default Intel NIOS II HAL\n' + \
            'add_sw_property supported_bsp_type FreeRTOS \n' +\
            'add_sw_property supported_bsp_type HAL \n'

            # 1.d: Choose the selected target device 
            tcl_hwlib_str=tcl_hwlib_str+'\n\n' +\
            '# \n' + \
            '# General settings\n' + \
            '#\n'

            # Remove the old TCL script file
            if(os.path.isfile(Quartus_componet_folder+SPLM[SPno]+FolderName+SPLM[SPno]+FolderName+"_sw.tcl")):
                os.remove(Quartus_componet_folder+SPLM[SPno]+FolderName+SPLM[SPno]+FolderName+"_sw.tcl")

            with open(Quartus_componet_folder+SPLM[SPno]+FolderName+SPLM[SPno]+FolderName+"_sw.tcl","a") as f:
                f.write(tcl_hwlib_str)

            print('   Generatation of the TCL component TCL script for '+FolderName+' done')

    
    ############################# Allow the user to add custom code to the project  ###############################
    if len(glob.customFolderName)>0:
        print('\n################################################################################')
        print('#                                                                              #')
        print('#  OPTIONAL: EDIT THE GENERATED TCL SCRIPT FOR CUSTOM COMPONENTS               #')
        print('#                                                                              #')
        print('#  At this point it is possible to edit the autogenerated TCL Scripts for the  #')
        print('#  custom components                                                           #')
        print('#                                                                              #')
        print('-------------------------------------------------------------------------------')
        print('#  Open and edit the following file/s:                                         #')

        for FolderName in glob.customFolderName:
            print('         for the Component "'+FolderName+'":')
            print(Quartus_componet_folder+SPLM[SPno]+FolderName+SPLM[SPno]+FolderName+"_sw.tcl")

        print('------------------------------------------------------------------------------')
        __wait__ = input('Type anything to continue ... ')


    ################################################## Generate Demo project Files #################################################

    print('\n --> Copy the default FreeRTOS Demo files to the Quartus Example folder')


    if(os.path.isdir(Quartus_example_folder+SPLM[SPno]+DEMO_NAME_FREERTOSC)):
        print('--> Remove old component folder: '+DEMO_NAME_FREERTOSC)
        try:
            shutil.rmtree(Quartus_example_folder+SPLM[SPno]+DEMO_NAME_FREERTOSC)
        except Exception as ex:
            print('ERROR: Failed to remove the old'+DEMO_NAME_FREERTOSC+' Quartus Example folder!')
            print('Msg: '+str(ex))
            sys.exit()

    try:
        distutils.dir_util.copy_tree(os.getcwd()+SPLM[SPno]+'Demos'+SPLM[SPno]+DEMO_NAME_FREERTOSC,\
            Quartus_example_folder+SPLM[SPno]+DEMO_NAME_FREERTOSC)
    except Exception as ex:
        print('Error during Example Project folder data processing')
        print(str(ex))
        sys.exit()


    ################################################ Generate XML Demo project File ################################################

    print('--> Generate XML Demo project template File for the default FreeRTOS Demo')

    xml_file = generate_xml_template_file('FreeRTOS - robseb',DEMO_NAME_FREERTOSC,\
        'freertos_robseb','freertos','FreeRTOS Demo with hwlib')


    # Remove the old TCL script file
    if(os.path.isfile(Quartus_example_folder+SPLM[SPno]+DEMO_NAME_FREERTOSC+SPLM[SPno]+"template.xml")):
        os.remove(Quartus_example_folder+SPLM[SPno]+DEMO_NAME_FREERTOSC+SPLM[SPno]+"template.xml")

    with open(Quartus_example_folder+SPLM[SPno]+DEMO_NAME_FREERTOSC+SPLM[SPno]+"template.xml","a") as f:
        f.write(xml_file)


    # Generate a socfpgaHAL demo project
    if glob.socfpgaHAL_selection == 1:

        print('\n --> Copy the socfpgaHAL Demo files to the Quartus Example folder')

        if(os.path.isdir(Quartus_example_folder+SPLM[SPno]+DEMO_NAME_SOCFPGAHALC)):
            print('--> Remove old component folder: '+DEMO_NAME_SOCFPGAHALC)
            try:
                shutil.rmtree(Quartus_example_folder+SPLM[SPno]+DEMO_NAME_SOCFPGAHALC)
            except Exception as ex:
                print('ERROR: Failed to remove the old'+DEMO_NAME_SOCFPGAHALC+' Quartus Example folder!')
                print('Msg: '+str(ex))
                sys.exit()

        try:
            distutils.dir_util.copy_tree(os.getcwd()+SPLM[SPno]+'Demos'+SPLM[SPno]+DEMO_NAME_SOCFPGAHALC,\
                Quartus_example_folder+SPLM[SPno]+DEMO_NAME_SOCFPGAHALC)
        except Exception as ex:
            print('Error during Example Project folder data processing')
            print(str(ex))
            sys.exit()

        print('--> Generate XML Demo project template File for the default socfpgaHAL Demo')
        xml_file = generate_xml_template_file('FreeRTOS+socfpgaHAL-robseb',DEMO_NAME_SOCFPGAHALC,\
            'socfpgahal_freertos_robseb','freertos',\
                'socfpgaHAL demo with FreeRTOS\n to demostrate the FPGA-to-HPS bridge with a NIOS II processor')

        # Remove the old TCL script file
        if(os.path.isfile(Quartus_example_folder+SPLM[SPno]+DEMO_NAME_SOCFPGAHALC+SPLM[SPno]+"template.xml")):
            os.remove(Quartus_example_folder+SPLM[SPno]+DEMO_NAME_SOCFPGAHALC+SPLM[SPno]+"template.xml")

        with open(Quartus_example_folder+SPLM[SPno]+DEMO_NAME_SOCFPGAHALC+SPLM[SPno]+"template.xml","a") as f:
            f.write(xml_file)

    ############################################ NIOS II-Commnad Shell: Execute TCL Scripts ####################################
    print('--> Open the Intel NIOS II Command Shell\n')

    try:

        with Popen(Quartus_Folder+QURTUS_NIOSSHELL_DIR, stdout = subprocess.PIPE, stdin=subprocess.PIPE) as niosCmdSH:
           
            print('   Check that the NIOS II Command Shell works properly')
            startUpMsg =''
            line = 'xx'
            while not(line =='' or line=='\n'):
                line = niosCmdSH.stdout.readline().decode("utf-8") 
                startUpMsg = startUpMsg+line
            
            niosCmdSH.communicate() 
            niosCmdSH.stdout.close()
            # Check that the NIOS II Command Shell was open successfully 
            if not "Altera Nios2 Command Shell" in startUpMsg:
                print('ERROR: Failed to start the NIOS II Command Shell successfully!')
                sys.exit()
            print('    looks ok')

        with Popen(Quartus_Folder+QURTUS_NIOSSHELL_DIR,stdin=subprocess.PIPE) as niosCmdSH:
            time.sleep(1)
            print('--> Navigate to the Quartus Project Folder')
    
            if sys.platform =='linux':
                b = bytes(' cd '+Quartus_componet_folder+"\n", 'utf-8')
            else:
                if(highestVer>=19.1):
                    if(quartus_standard_ver):
                        b = bytes(' cd /mnt/c/'+QURTUS_DEF_FOLDER+'/'+str(highestVer)+'/nios2eds/components'"\n", 'utf-8')
                    else:
                        b = bytes(' cd /mnt/c/'+QURTUS_DEF_FOLDER_LITE+'/'+str(highestVer)+'/nios2eds/components'"\n", 'utf-8')
                else:

                    if(quartus_standard_ver):
                        b = bytes(' cd C:/'+QURTUS_DEF_FOLDER+'/'+str(highestVer)+'/nios2eds/components'"\n", 'utf-8')
                    else:
                        b = bytes(' cd C:/'+QURTUS_DEF_FOLDER_LITE+'/'+str(highestVer)+'/nios2eds/components'"\n", 'utf-8')
            niosCmdSH.stdin.write(b) 
            time.sleep(0.5)
            
            print('--> Generate now the Eclipse for NIOS components by executing the TCL scripts')

            if(highestVer>=19.1 and not(sys.platform =='linux')):
                print("   Windows 10 Version for 19.1+")
                b = bytes('ip-make-ipx.exe --source-directory=. --output=components.ipx\n', 'utf-8')
            else:
                b = bytes('ip-make-ipx --source-directory=. --output=components.ipx\n', 'utf-8')
            
            niosCmdSH.stdin.write(b)
            niosCmdSH.communicate()
            
    except Exception as ex:
       print('ERROR: Failed to start the Intel NIOS II Command Shell! '+ str(ex))
       sys.exit()

############################################################ Goodby screen  ###################################################
    print('\n################################################################################')
    print('#                                                                              #')
    print('#                        GENERATION WAS SUCCESSFUL                             #')
    print('# -----------------------------------------------------------------------------#')
    print('                                 NEXT STEPS                                    #')
    print('#                                                                              #')
    print('#                     --- Open ECLIPSE for NIOS II ---                         #')
    print('                   ('+Quartus_Folder+SPLM[SPno]+'nios2eds'+SPLM[SPno]+'bin'+SPLM[SPno]+'eclipse_nios2)  ')
    print('#                                                                              #')
    print('#               --- Open the generated Example Project ---                     #')
    print('#      +  Select inside Eclipse:  File > New > NIOS II Application and BSP ... #')
    print('#      + Select the Template: "FreeRTOS - robseb"                              #')
    print('#                                                                              #')
    print('#                 --- Use the generated NIOS II BSP  ---                       #')
    print('#      +  Select inside Eclipse:  File > New > NIOS II Board Support Package   #')
    print('#      +  Select as BSP type:  "FreeRTOS"                                      #')
    print('#                                                                              #')
    print('# -----------------------------------------------------------------------------#')
    print('#                                                                              #')
    print('#                           SUPPORT THE AUTHOR                                 #')
    print('#                                                                              #')
    print('#                            ROBIN SEBASTIAN                                   #')
    print('#                     (https://github.com/robseb/)                             #')
    print('#                        Contact: git@robseb.de                                #')
    print('#                                                                              #')
    print('#    NIOSII_EclipseCompProject and rsYocto are projects, that I have fully     #')
    print('#        developed on my own. No companies are involved in these projects.     #')
    print('#        Today I am a Master Student of electronic engineering                 #')
    print('#            Please support me for further development                         #')
    print('#                                                                              #')
    print('################################################################################')