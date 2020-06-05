# Python Script to automatically generate a Intel NIOS II Eclipse Demo Project with a custom configuration

![Alt text](doc/Concept.png?raw=true "Concept illustration")

<br>

The Python script automatically generate by the user-specified an optimized Eclipse Demo project for the Intel NIOS II Embedded Design Suite IDE.
It should help to automate the often complicate and always equal project setup process with custom libraries and real-time operating systems, such as FreeRTOS. 

# Selectable Components
The list of selected comports, that can be automatically cloned from Github will updated. <br>
Now, are following components available: 

| Components | Description
|:--|:--|
| [**FreeRTOS-Kernel**](https://github.com/FreeRTOS/FreeRTOS-Kernel) *for NIOS II*    | The latest FreeRTOS Version cloned from Github  |
| [**Intel hwlib**](https://github.com/robseb/hwlib) optimized for NIOS II    | Library for accessing HPS components of SoC-FPGAs with NIOS II |
|  `Custom Code folders` | Inserted folders with user libraries 

# Supported Platforms 

* **Desktop OS**
    * **Windows 10**
    * **Ubuntu Linux**
* **IDE**
    * **Intel Quartus Prime Lite**<!--  -->
    * **Intel Quartus Prime Standard**

* **Every Intel FPGA with NIOS II support**  
    * For running FreeRTOS is a **Timer** module required 

* Supported SoC-FPGA of the Intel *hwlib* for accessing HPS hard-IP with the NIOS II core
    * **Intel Cyclone V SoC-FPGA**-families 
    * **Intel Arria V SoC-FPGA**-families
    * **Intel Arria 10 SX SoC-FPGA**-family  

# Getting started

## I. Installment of Intel Quartus Prime II with NIOS II support
<br>
<details>
<summary><strong>Step-by-step guide</strong></summary>
<a name="Pos1"></a>
<br>

The following step-by-step guide show how to install the necessary Intel Quartus Prime IDE with the Intel NIOS II Embedded Design Suite IDE for Windows and Linux (used Version for this guide: v19.1.0.670)

* I.1.: **Installment of additional required components**
    * **Windows 10**
        * Install [**Java**](https://www.java.com/en/download/win10.jsp) for Windows 
        * Install the [**latest Python Version**](https://www.python.org/downloads/windows/) for Windows (that is required to use the script)
            * Use the **Windows x86-64 executable installer**
            * Be sure that "Add Python 3.X to PATH" is selected during the installment
                ![Alt text](doc/Screenshoot_PythonInstallment.png?raw=true "Screenshot of the Python installer")
        * **Restart** your Computer
    * **Ubuntu**
        * Install *Python pip* by executing following Linux command
        ````shell
        sudo apt update
        sudo apt install python3-pip
        ````

* I.2.: [**Download the latest Intel Quartus Prime Edition**](https://fpgasoftware.intel.com/?edition=lite) for your OS and with support for your Intel FPGA family (Quartus Prime (includes Nios II EDS) Version)
* I.3.: **Download the Device support for your used FPGA device family**
* I.4.: **Installment of Intel Quartus Prime**
    * **Ubuntu**
        * Open the Linux **Terminal** and navigate to the download Quartus file
        * Run following commands inside the Terminal: 
            ````shell
            chmod +x QuartusLiteSetup-19.X.X.XXX-linux.run
            ./QuartusLiteSetup-19.X.X.XXX-linux.run
            ````
    * **Windows 10 & Ubuntu**
        * Follow the instructions of the installer
        * Use the default installation path
        ![Alt text](doc/Screenshoot_installingQuartus.png?raw=true "Screenshot of the installing progress")

* 1.5.: **Add support for your used FPGA family**
    * **Windows 10** 
        *  Start from the Windows start menu the application **"Device Installer (Quartus Prime 19.1)"**  
    * **Ubuntu** 
        * Open the installed Quartus Prime be executing following command inside the Linux Terminal:
    	  ````shell
          intelFPGA_lite/19.1/quartus/bin ./quartus --64bit
          ````
        * After the first start of Intel Quartus Prime following Message Box should appear:
            ![Alt text](doc/QuartusMessageBox.png?raw=true "Screenshot of the message box")
        * Select **Yes** to add support for your chosen Intel FPGA device family
        * **Alternativ:** Inside Quartus Prime select: *Tools/Install Devices...* 
    * **Windows 10 & Ubuntu**
        * Follow the installer
            * Select the folder where the downloaded Device support file (*.qdz*) is located
            * The chosen FPGA device family should be detected 
            * For example for the Intel Cyclone V family:
                ![Alt text](doc/Screenshoot_DeviceSupport.png?raw=true "Screenshot of Device Support Installment")
* 1.6.: **Installment of the *Intel NIOS II Software Build Tools* (SBT) for Eclipse**
    * **Windows 10 & Ubuntu**
        * **Download** CDT 8.8.1 which is Eclipse C/C++ IDE for Mars.2
            * [**CDT 8.8.1 for Windows**](https://www.eclipse.org/downloads/download.php?file=/technology/epp/downloads/release/mars/2/eclipse-cpp-mars-2-win32-x86_64.zip)
            * [**CDT 8.8.1 for Linux**](https://www.eclipse.org/downloads/download.php?file=/technology/epp/downloads/release/mars/2/eclipse-cpp-mars-2-linux-gtk-x86_64.tar.gz)
            * **Alternativ Mirror:** The files are inside the [**Releases**](https://github.com/robseb/NIOSII_EclipseCompProject/releases) of this Github repository available, as well. With this version you can copy the extract folder to
                * **Windows 10:** "C:\intelFPGA_lite\19.1\nios2eds\bin"
                * **Ubuntu:**  "intelFPGA_lite\19.1\nios2eds\bin"
        * **Extract** (unzip) the downloaded file
        * **Rename** the folder "*eclipse*" inside the extracted folder to "*eclipse_nios2*"
        * **Copy** the folder "*eclipse_nios2*" inside the extract folder to:
            * **Windows 10:** "C:\intelFPGA_lite\19.1\nios2eds\bin"
            * **Ubuntu:**  "intelFPGA_lite\19.1\nios2eds\bin"
        * **Extract** (unzip) the file to a temporary location on the desktop 
            * **Windows 10:** C:\intelFPGA_lite\19.1\nios2eds\bin\eclipse_nios2_plugins.zip
             * **Ubuntu:** intelFPGA_lite\19.1\nios2eds\bin\eclipse_nios2_plugins.tar.gz
        * **Copy** the content of this extracted folder to the before downloaded folder 
            * **Windows 10:** C:\intelFPGA_lite\19.1\nios2eds\eclispe_nios2
            * **Ubuntu:** intelFPGA_lite\19.1\nios2eds\bin\\eclispe_nios2
            * **Replace** the file in the folder with the new one by merging them together 
            * The folder should now look like:
                ![Alt text](doc/Screenshoot_ContentFolder.png?raw=true "Screenshot of the folder content")
</details>

## II. Run the script to generate a new custom Eclipse Project
To use this script to generate a custom Eclipse project for the NIOS II sof-core processor realise follow instructions:
* II.1.: **Clone this Github repository** 
* II.2.: **Open the Windows Command prompt or the Linux Terminal and navigate to the repository folder**
* II.3.: **Install a *Python Pip* module to clone Github repositories by running following command
    * **Windows 10**
        ````shell
        pip3 install dload
        ````
    * **Ubuntu**
        ````shell
        pip3 install GitPython
        ````
* II.3.: **Execute the Python script by running following command**
    * **Windows 10**
    ````shell
    python makeNIOS_CompProject.py        
    ```` 
    * **Ubuntu**
    ````shell
    python3 makeNIOS_CompProject.py        
    ```` 
## III. Configure the Eclipse Example Project for your requirements 
<br>
<details>
<summary><strong>Details</strong></summary>
<a name="pos2"></a>
<br>
Follow the displayed instructions of the script to add the available module to your configuration. 
Also, it is enabled to drag & drop folders with custom Code to the "*working_folder*" inside this repository folder. The script will automatically generate for every code folder a NIOS II Eclipse package. This package is pre-installed to the generate NIOS II Example Project. 
</details>

## IV. Create a new Eclipse project with the generate example project
<br>

Follow following instructions to create a new Eclipse for NIOS II project with the previously generated example project. 
* IV.1.:  **Start *Eclispe for NIOS II*** 
    * Select inside *Quartus Prime* *Tools/NIOS II Software Build Tools for Eclipse*
    * **Alternative:** Open Eclipse manually  
        * Start the *NIOS II Command Shell*
            * **Windows 10:** Start: *C:\intelFPGA\18.1\nios2eds*
            * **Ubuntu:** Execute following commands
            ````shell  
            cd intelFPGA_lite/19.1/nios2eds/
            ./nios2_command_shell.sh
            ````
        * Start Eclipse inside the *NIOS II Command Shell* by typing following command
            ````shell
            eclipse-nios2
            ````
* IV.2.: **Select a Eclispe Workspace**
* IV.3.: **Create a new Eclispe project** by selecting: *File/New/Nios II Application and BSP from Template*
 ![Alt text](doc/ScreenshootEclipseConf.png?raw=true "Screenshot of the Eclipse project configuration")
 * Assign the output "*sopcinfo*" file of the Quartus Project with the Eclipse Project by specifying the *SOPC Information File name*
 * Give the Project a name
 * The by the script generate Project template is called "**FreeRTOS -robseb**". Select it.  
  ![Alt text](doc/ScreenshootEclipseProjectGenerate.png?raw=true "Screenshot of the Eclipse project configuration")
* Press **Finish** to allow Eclispe to create a new project
<br>
<br>
<br>
<br>

## V. Compile the Eclispe project 
<br>

<details>
<summary><strong>Step-by-Step guide</strong></summary>
<a name="step3"></a>
<br>
 Coming!
</details>

## VI. Debug the Eclipse project

<details>
<summary><strong>Step-by-Step guide</strong></summary>
<a name="step3"></a>
<br>
 Coming!
</details>

## VII. Example output of the Python script
<br>

````shell
    C:\Users\Robin\Documents\GitHub\NIOSII_EclipseCompProject>python makeNIOS_CompProject.py

    #############################################################################
    #                                                                            #
    #    ########   ######     ##    ##  #######   ######  ########  #######     #
    #    ##     ## ##    ##     ##  ##  ##     ## ##    ##    ##    ##     ##    #
    #    ##     ## ##            ####   ##     ## ##          ##    ##     ##    #
    #    ########   ######        ##    ##     ## ##          ##    ##     ##    #
    #    ##   ##         ##       ##    ##     ## ##          ##    ##     ##    #
    #    ##    ##  ##    ##       ##    ##     ## ##    ##    ##    ##     ##    #
    #    ##     ##  ######        ##     #######   ######     ##     #######     #
    #                                                                            #
    #       AUTOMATIC SCRIPT FOR GENERATING A ECLIPSE FOR NIOS II PROJECT        #
    #                    WITH CUSTOM COMPONENTS,OS AND HAL,...                   #
    #                                                                            #
    #               by Robin Sebastian (https://github.com/robseb)               #
    #                            Vers.: 1.007                                   #
    #                                                                            #
    ##############################################################################


    --> Find the System Platform
    --> Try to find the default Quartus installation path
            Following Quartus Installation Folder was found:
            C:\intelFPGA_lite\18.1

    --> Check that the script runs inside the Github folder

    --> Working Folder Name: working_folder


    ##############################################################################
    # -> Intel hwlib for using the peripheral HPS components  <- #
    # -> of the Cyclone and Arria SoC-FPGA with the NIOS II <- #
    #   1: Install the hwlib
    #   2: Do not pre-install the hwlib
    ------------------------------------------------------------------------------
    Q,C = abort execution
    --> Please chose with 1 or 2 = 2
    ---->Do not pre-install the hwlib

    =====================>>> Starting the generation... <<<====================

    --> FreeRTOS Version is already available
    --> Check if the FreeRTOS folders looks okay
        looks okay
    --> Remove support of diffrent compliers as GCC
    --> Allow only the folder "GCC" and "MemMang" inside /FreeRTOS-Kernel/portable
    --> Remove support of diffrent Platform as Intel NIOS II
    --> Remove vintage Memory Management

    ###############################################################################
    #                                                                              #
    #           OPTIONAL: ADD CUSTOM COMPONENTS TO THE PROJECT                     #
    #                                                                              #
    #  Add this point it is possible to generate for custom code a NIOS II Eclipse #
    #  component to add the code to the final NIOS II Eclipse HAL project          #
    #                                                                              #
    #  Copy a folder with the code to the working folder                           #
    #  for every folder will be a  NIOS II Eclipse component be generareted and    #
    #  it will be added to the final Demo project                                  #
    #                                                                              #
    #  Note: The folder name will be used as component name                        #
    ------------------------------------------------------------------------------
    # The working folder:                                                          #
    C:\Users\Robin\Documents\GitHub\NIOSII_EclipseCompProject\working_folder\
    ------------------------------------------------------------------------------
    Type anything to continue ...

    --> Detect added custom folders
        No Folders detect
    ------------------------------------------------------------------------------
    --> Coy additional files to the FreeRTOS folder
    --> Relace the port.c file with additional/port.c file
    --> Copy everything else to the FreeRTOS/portable/NIOS_RTOS_HAL folder
        Copy include files

    --> Remove old component folder: FreeRTOS
    --> Generate FreeRTOS Kernel code file structure and
        Copy the FreeRTOS Kernel to the Quartus Component folder
        CONTRIBUTING.md
        croutine.c
        event_groups.c
        GitHub-FreeRTOS-Kernel-Home.url
        History.txt
        include
        LICENSE.md
        list.c
        portable
        queue.c
        Quick_Start_Guide.url
        README.md
        SECURITY.md
        stream_buffer.c
        tasks.c
        timers.c

    --> Generate TCL component TCL script for the FreeRTOS Kernel
    --> Progress every file in folder structure "FreeRTOS"

        Folder: include
        Folder: portable
        Folder: source
        --> \source
        File: CONTRIBUTING.md
        File: croutine.c
        File: event_groups.c
        File: GitHub-FreeRTOS-Kernel-Home.url
        File: History.txt
        File: LICENSE.md
        File: list.c
        File: queue.c
        File: Quick_Start_Guide.url
        File: README.md
        File: SECURITY.md
        File: stream_buffer.c
        File: tasks.c
        File: timers.c
        <--
        Folder: include
        Folder: portable
        --> \portable
        Folder: GCC
        Folder: MemMang
        Folder: NIOS_RTOS_HAL
        File: readme.txt
        --> \portable\NIOS_RTOS_HAL
        File: alt_env_lock.c
        File: alt_exit.c
        File: alt_hooks.h
        File: alt_iic.c
        File: alt_irq_handler.c
        File: alt_legacy_irq.h
        File: alt_main.c
        File: alt_malloc_lock.c
        File: alt_sem.h
        File: alt_sem_freertos.h
        File: alt_tick.c
        <-- \portable
        Folder: GCC
        Folder: MemMang
        --> \portable\MemMang
        File: heap_3.c
        File: heap_4.c
        File: heap_5.c
        File: ReadMe.url
        <-- \portable
        Folder: GCC
        --> \portable\GCC
        Folder: NiosII
        --> \portable\GCC\NiosII
        File: port.c
        File: portmacro.h
        File: port_asm.S
        <-- \portable\GCC
        <-- \portable\GCC
        <<<<---- \include
        File: atomic.h
        File: croutine.h
        File: deprecated_definitions.h
        File: event_groups.h
        File: FreeRTOS.h
        File: FreeRTOSConfig.h
        File: list.h
        File: message_buffer.h
        File: mpu_prototypes.h
        File: mpu_wrappers.h
        File: portable.h
        File: projdefs.h
        File: queue.h
        File: semphr.h
        File: StackMacros.h
        File: stack_macros.h
        File: stdint.readme
        File: stream_buffer.h
        File: task.h
        File: timers.h
        <-- \include
        <<<<---- \include
        ==== File processing done ====

    --> Generate include folders for "FreeRTOS"
    Add include path: portable/NIOS_RTOS_HAL
    Add include path: portable/GCC/NiosII
    Add include path: include
    Generatation of TCL OS TCL script for FreeRTOS done

    --> Copy Demo files to the Quartus Example folder
    --> Remove old component folder: freertos_c1
    --> Generate XML Demo project template File
    --> Open the Intel NIOS II Command Shell

    --> Navigate to the Quartus Project Folder
    --> Generate now Eclipse for NIOS components by executing the TCL scripts
    ------------------------------------------------
    Altera Nios2 Command Shell [GCC 4]

    Version 18.1, Build 625
    ------------------------------------------------
    2020.06.03.18:07:12 Info: Doing: <b>ip-make-ipx --source-directory=. --output=components.ipx</b>
    2020.06.03.18:07:13 Info: Using factories: CuspFactory, ImportFactory, DSPBuilderFactory, JarFactory, TclModuleFactory, BeanElementFactory, PresetFactory, QsysFactory, IPXactBlackBoxFactory, EmbeddedSwTclDriverFactory
    2020.06.03.18:07:13 Info: (0) searching <b>C:/intelFPGA_lite/18.1/nios2eds/components/**/*</b> (command line switch)
    2020.06.03.18:07:13 Info: Loading altera_hal/altera_hal_sw.tcl
    2020.06.03.18:07:13 Info: Loading altera_hostfs/altera_hostfs_sw.tcl
    2020.06.03.18:07:13 Info: Loading altera_iniche/altera_iniche_sw.tcl
    2020.06.03.18:07:13 Info: Loading altera_nios2/altera_nios2_hal_sw.tcl
    2020.06.03.18:07:13 Info: Loading altera_nios2/altera_nios2_qsys_hal_sw.tcl
    2020.06.03.18:07:13 Info: Loading altera_nios2/altera_nios2_qsys_hw.tcl
    2020.06.03.18:07:14 Info: Loading altera_nios2/altera_nios2_qsys_ucosiii_sw.tcl
    2020.06.03.18:07:14 Info: Loading altera_nios2/altera_nios2_qsys_ucosii_sw.tcl
    2020.06.03.18:07:14 Info: Loading altera_nios2/altera_nios2_ucosiii_sw.tcl
    2020.06.03.18:07:14 Info: Loading altera_nios2/altera_nios2_ucosii_sw.tcl
    2020.06.03.18:07:14 Info: Loading altera_nios2/nios2-wizard.jar
    2020.06.03.18:07:14 Info: Loading altera_nios2/nios2-wizard.jar
    2020.06.03.18:07:14 Info: Loading altera_nios2_gen2/altera_nios2_hal_sw.tcl
    2020.06.03.18:07:14 Info: Loading altera_nios2_gen2/altera_nios2_hw.tcl
    2020.06.03.18:07:14 Info: Loading altera_nios2_gen2/altera_nios2_ucosiii_sw.tcl
    2020.06.03.18:07:14 Info: Loading altera_nios2_gen2/altera_nios2_ucosii_sw.tcl
    2020.06.03.18:07:14 Info: Loading altera_nios2_gen2/altera_nios2_unit_hw.tcl
    2020.06.03.18:07:14 Info: Loading altera_quad_seven_seg/altera_quad_seven_seg_sw.tcl
    2020.06.03.18:07:14 Info: Loading altera_ro_zipfs/altera_ro_zipfs_sw.tcl
    2020.06.03.18:07:14 Info: Loading FreeRTOS/FreeRTOS_sw.tcl
    2020.06.03.18:07:14 Info: Loading hwlib/hwlib_sw.tcl
    2020.06.03.18:07:14 Info: Loading micrium_uc_osii/micrium_ucosii_sw.tcl
    2020.06.03.18:07:14 Info: <b>C:/intelFPGA_lite/18.1/nios2eds/components/**/*</b> matched 170 files in 1.36 seconds
    2020.06.03.18:07:14 Info: Found 20 components

    ################################################################################
    #                                                                              #
    #                        GENERATION WAS SUCCESSFUL                             #
    # -----------------------------------------------------------------------------#
                                    NEXT STEPS                                    #
    #                                                                              #
    #                     --- Open ECLIPSE for NIOS II ---                         #
                    (C:\intelFPGA_lite\18.1\nios2eds\bin\eclipse_nios2)
    #                                                                              #
    #               --- Open the generated Example Project ---                     #
    #      +  Select inside Eclipse:  File > New > NIOS II Application and BSP ... #
    #      + Select the Temaplate: "FreeRTOS - robseb"                             #
    #                                                                              #
    #                 --- Use the generated NIOS II BSP  ---                       #
    #      +  Select inside Eclipse:  File > New > NIOS II Board Support Package   #
    #      +  Select as BSP type:  "FreeRTOS"                                      #
    #                                                                              #
    # -----------------------------------------------------------------------------#
    #                                                                              #
    #                           SUPPORT THE AUTHOR                                 #
    #                                                                              #
    #                            ROBIN SEBASTIAN                                   #
    #                     (https://github.com/robseb/)                             #
    #                                                                              #
    #    NIOSII_EclipseCompProject and rsYocto are projects, that I have fully     #
    #        developed on my own. No companies are involved in this projects.      #
    #        Today I aim a Master Student of electronic engineering                #
    #            Please support me for further development                         #
    #                                                                              #
    ################################################################################
    C:\Users\Robin\Documents\GitHub\NIOSII_EclipseCompProject>
````

<br>
<br>
<br>
<br>

# Author

***Robin Sebastian**

*NIOSII_EclipseCompProject* and *rsYocto* are projects, that I have fully developed on my own. No companies are involved in this projects.
Today I'm a Master Student of electronic engineering with the major embedded systems. 

[![Gitter](https://badges.gitter.im/rsyocto/community.svg)](https://gitter.im/rsyocto/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Email me!](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](mailto:git@robseb.de)
