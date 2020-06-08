
![GitHub](https://img.shields.io/static/v1?label=Core&message=Intel+NIOS+II&color=blue)
![GitHub](https://img.shields.io/static/v1?label=hwlib+SoC-FPGA&message=Cyclone+V,+Arria+V,+Arria+10&color=yellowgreen)
![GitHub](https://img.shields.io/github/license/robseb/NIOSII_EclipseCompProject)
# Python Script to automatically generate a Intel NIOS II Eclipse Project with a custom software components (e.g. FreeRTOS)

![Alt text](doc/Concept.png?raw=true "Concept illustration")

<br>

**This Python script can automate the project preparation process by generating in Eclipse Demo project with selected components. For every by the user chosen component is an TCL-script generated and it will be added to the demo project.**

In the same way it is enabled to drag & drop folder with custom code to add them to the project. The often time intensive manual pre-configuration process is not necessary any more. 
The script can for instant clone the latest Kernel of the real-time operating system “*FreeRTOS*” from *GitHub* and removes the driver for other platforms and generates TCL-scripts with all global values, sources and includes. 

This script is designed to work together with the complete Intel development suite and supports every Intel FPGA device family with the support of the NIOS II soft core processor. 

In the future I will add more and more components that can be selected and added to the project.

___

![Alt text](doc/EclipseDebugFreeRTOS.png?raw=true "Sceeenshoot Debugging FreeRTOS")
**Screenshot of a Eclipse Debugging sesion of a automaticly generated project with FreeRTOS**


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

* Supported SoC-FPGA of the Intel *hwlib* for accessing *HPS* hard-IP with the *NIOS II* core
    * **Intel Cyclone V SoC-FPGA**-families 
    * **Intel Arria V SoC-FPGA**-families
    * **Intel Arria 10 SX SoC-FPGA**-family  

* Tested Platforms
    * Intel Quartus Prime Lite 19.1 Ubuntu & Windows 10 
    * Intel Quartus Prime Lite 18.1 Ubuntu & Windows 10 
    * Quartus Prime Standard 18.1 Windows 10


# Getting started

## I. Installment of Intel Quartus Prime 19.1 with NIOS II support
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
            * Be sure that "**Add Python 3.X to PATH**" is selected during the installment
                ![Alt text](doc/Screenshoot_PythonInstallment.png?raw=true "Screenshot of the Python installer")
        * **Restart** your Computer
        * **Install the Windows Subsystem for Linux (WSL)**
            * Be sure that your host computer runs Windows 10 **Build 19041** or higher
            * Follow [*this step-by-step guide*](https://docs.microsoft.com/en-us/windows/wsl/install-win10) to install WSL 2
                * Enable and Install WSL with the *Windows Power Shell*
                * Update to **WSL 2**
                * Install a **Ubuntu Linux Distribution**
                * Set up the distribution with a user name and password
            * Install additional components required by the *NIOS II Command Shell*
                *  Open the Windows Command Prompt and execute following command to start the wsl
                    ````cmd
                    wsl
                    ````
                * Install the required packages with
                    ````cmd
                    sudo apt-get update
                    sudo apt-get install wsl make dos2unix
                    ````
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

<br>

## II. Run the script to generate a new custom Eclipse Project
To use this script to generate a custom Eclipse project for the NIOS II sof-core processor realise follow instructions:
* II.1.: **Clone this Github repository**
* II.2.: **Open the Windows Command prompt or the Linux Terminal and navigate to the repository folder**
* II.3.: **Install a *Python Pip* module to clone Github repositories by running following command**
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
        * **Run the script as administrator to avoid permission issues by writing to C:**
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
Also, it is enabled to drag & drop folders with custom Code to the *"working_folder"* inside this repository folder. The script will automatically generate for every code folder a NIOS II Eclipse package. This package is pre-installed to the generate NIOS II Example Project. 
</details>
<br>

## IV. Create a new Eclipse project with the generate example project
<br>

Follow following instructions to create a new Eclipse for NIOS II project with the previously generated example project. 

<details>
<summary><strong>Start Eclipse for NIOS II</strong></summary>
<a name="pos2"></a>

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
</details>

* IV.3.: **Create a new Eclipse project** by selecting: *File/New/Nios II Application and BSP from Template*

     ![Alt text](doc/ScreenshootEclipseConf.png?raw=true "Screenshot of the Eclipse project configuration")
 * Assign the output "*sopcinfo*" file of the Quartus Project with the Eclipse Project by specifying the *SOPC Information File name*
 * Give the Project a name
 * The generateD project template is called "**FreeRTOS -robseb**". Select it.  
  
    ![Alt text](doc/ScreenshootEclipseProjectGenerate.png?raw=true "Screenshot of the Eclipse project configuration")
* Press **Finish** to allow Eclispe to create a new project

* Open the demo application c-file "**main.c**" from the application part of the Eclipse project

**Folder structure of the generated project**  
    ![Alt text](doc/ProjectContent.png?raw=true "Eclipse Project Folder structure")

**Screenshot of Eclipse with the open auto generated FreeRTOS project**
    ![Alt text](doc/EclipseSceenshoot.png?raw=true "Screenshot of Eclipse")
<br>

* **Select your FPGA board for the Demo**
    * The pre-installed demo contains a simple stop watch written as FreeRTOS task
    * Choice your FPGA development board for this demo due to specifying "*SELCTED_BOARD*" in "*main.c*"
        ````c
        #define TERASIC_DE0_NANO    1  // Terasic DE0  NANO Board with a Intel Cyclone IV FPGA
        #define TERASIC_DE10_STD    2  // Terasic DE10 STANDARD Board with a Intel Cyclone V SoC-FPGA
        #define TERASIC_DE10_NANO   3  // Terasic DE10 NANO Board with a Intel Cyclone V SoC-FPGA
        #define TERASIC_HAN_PILOT   4  // Terasic HAN PILOT Board with a Intel Arria 10 SoC-FPGA
        #define CUSTOM_BOARD	    0  // Custom board with a custom board configuration
        #define UNKOWN_BOARD	   -1
        /////
        ///////////////////
        // TODO: Select your development board
        #define SELCTED_BOARD TERASIC_DE10_STD
        ///////////////////
        /////
        ````
* **Compile the project** by pressing **`Ctrl+b`** 


## VI. Debug the Eclipse project
<br>
<details>
<summary><strong>Step-by-Step guide</strong></summary>
<a name="step4"></a>
<br>

After the project build was successful the project can be debugged on the development board. 
For this task it is necessary to configure the FPGA with a proper FPGA configuration with a NIOS II soft-core processor.
In the following steps are shown how to start a debugging session on a FPGA development board with a proper FPGA configuration and the Intel USB FPGA Blaster (available on *Teraisc* FPGA boards).   

* Select the debug icon (*bug*) and choose "*Debug Configurations...*" on the Eclipse toolbar

    ![Alt text](doc/EclipseDebugButton.png?raw=true "Eclipse Debug button")
* The following window appears 
    ![Alt text](doc/EclipseDebugConfWin1.png?raw=true "Eclipse Debug configuration window")

* Double-click to the list iteam "**Nios II Hardware**" to create a new debugging configuration
* Inside the debugging configuration select the **Project name** of your previously created project
    ![Alt text](doc/EclipseDebugConfWin2.png?raw=true "Eclipse Debug configuration window - project selection")
* Check on the tap "**Debugger**" that Eclipse could find the FPGA Blaster of your board
      ![Alt text](doc/EclipseDebugConfWin3.png?raw=true "Eclipse Debug configuration window - Debugger")
*  Start the debugging session by pressing the "**Apply**"- and "**Debug**"-Button
* Now should start the debugging process as shown in screenshot above

</details>

## VII. Example output of the Python script
<br>
<details>
<summary><strong>The output after a executon</strong></summary>
<a name="step5"></a>

````shell
 C:\Users\robseb\Documents\GitHub\NIOSII_EclipseCompProject>python makeNIOS_CompProject.py

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
#                            Vers.: 1.02                                     #
#                                                                            #
##############################################################################


--> Find the System Platform
--> Try to find the default Quartus installation path
        Following Quartus Installation Folder was found:
        C:\intelFPGA_lite\19.1

--> Check that the script runs inside the Github folder

--> Working Folder Name: working_folder


##############################################################################
# -> Intel hwlib for using the peripheral HPS components  <- #
# -> of the Cyclone and Arria SoC-FPGA with the NIOS II <- #
#   1: Install the hwlib
#   2: Do not pre-install the hwlib
------------------------------------------------------------------------------
Q,C = abort execution
--> Please chose with 1 or 2 = 1
---->Install the hwlib


##############################################################################
# -> Select the Intel SoC-FPGA Family <- #
# ->  <- #
#   1: Intel Cyclone V- or Arria V SoC-FPGA
#   2: Intel Arria 10 SoC-FPGA
------------------------------------------------------------------------------
Q,C = abort execution
--> Please chose with 1 or 2 = 1
---->Intel Cyclone V- or Arria V SoC-FPGA

=====================>>> Starting the generation... <<<====================

--> FreeRTOS Version is already available
--> Check if the FreeRTOS folders looks okay
    looks okay
--> Remove support of diffrent compliers as GCC
--> Allow only the folder "GCC" and "MemMang" inside /FreeRTOS-Kernel/portable
--> Remove support of diffrent Platform as Intel NIOS II
--> Remove vintage Memory Management
--> Cloning the latest hwlib Version (https://github.com/robseb/hwlib.git)

       please wait...
--> Check if the hwlib folders looks okay
    looks okay

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
 C:\Users\robseb\Documents\GitHub\NIOSII_EclipseCompProject\working_folder\
------------------------------------------------------------------------------
Type anything to continue ...

--> Detect added custom folders
     Folder: EthernetIF
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
--> Generate hwlib code file structure and
    Copy the hwlib to the Quartus Component folder
      include
      LICENSE
      src

--> Generate  component TCL script for custom user files
--> Generate the component "EthernetIF" code file structure and
    Copy it to the Quartus Component folder
      alt_dma.c
      alt_dma.h
      alt_fpgamgr.h
      alt_fpgamgrdata.h
      alt_fpga_manager.c
      alt_fpga_manager.h
      alt_printf.h
      CHECKSUMFILE
      CMakeLists.txt
      FPGA-status.vcxproj
      FPGA-writeBridge
      hps.h
      hwlib.h
      main.cpp
      readme
      socal.h

--> Generate TCL component TCL script for hwlib
--> Progress every file in folder structure "hwlib"

    Folder: include
    Folder: source
    Folder: src
    --> \src
    Folder: hwmgr
    Folder: safeclib
    Folder: utils
    --> \src\utils
    File: alt_p2uart.c
    File: alt_printf.c
    <-- \src
    Folder: hwmgr
    Folder: safeclib
    --> \src\safeclib
    File: abort_handler_s.c
    File: ignore_handler_s.c
    File: memcmp16_s.c
    File: memcmp32_s.c
    File: memcmp_s.c
    File: memcpy16_s.c
    File: memcpy32_s.c
    File: memcpy_s.c
    File: memmove16_s.c
    File: memmove32_s.c
    File: memmove_s.c
    File: memset16_s.c
    File: memset32_s.c
    File: memset_s.c
    File: memzero16_s.c
    File: memzero32_s.c
    File: memzero_s.c
    File: mem_primitives_lib.c
    File: mem_primitives_lib.h
    File: safeclib_private.h
    File: safe_mem_constraint.c
    File: safe_mem_constraint.h
    File: safe_str_constraint.c
    File: safe_str_constraint.h
    File: snprintf_support.c
    File: stpcpy_s.c
    File: stpncpy_s.c
    File: strcasecmp_s.c
    File: strcasestr_s.c
    File: strcat_s.c
    File: strcmpfld_s.c
    File: strcmp_s.c
    File: strcpyfldin_s.c
    File: strcpyfldout_s.c
    File: strcpyfld_s.c
    File: strcpy_s.c
    File: strcspn_s.c
    File: strfirstchar_s.c
    File: strfirstdiff_s.c
    File: strfirstsame_s.c
    File: strisalphanumeric_s.c
    File: strisascii_s.c
    File: strisdigit_s.c
    File: strishex_s.c
    File: strislowercase_s.c
    File: strismixedcase_s.c
    File: strispassword_s.c
    File: strisuppercase_s.c
    File: strlastchar_s.c
    File: strlastdiff_s.c
    File: strlastsame_s.c
    File: strljustify_s.c
    File: strncat_s.c
    File: strncpy_s.c
    File: strnlen_s.c
    File: strnterminate_s.c
    File: strpbrk_s.c
    File: strprefix_s.c
    File: strremovews_s.c
    File: strspn_s.c
    File: strstr_s.c
    File: strtok_s.c
    File: strtolowercase_s.c
    File: strtouppercase_s.c
    File: strzero_s.c
    File: wcpcpy_s.c
    File: wcscat_s.c
    File: wcscpy_s.c
    File: wcsncat_s.c
    File: wcsncpy_s.c
    File: wcsnlen_s.c
    File: wmemcmp_s.c
    File: wmemcpy_s.c
    File: wmemmove_s.c
    File: wmemset_s.c
    <-- \src
    Folder: hwmgr
    --> \src\hwmgr
    File: alt_16550_uart.c
    File: alt_can.c
    File: alt_generalpurpose_io.c
    File: alt_globaltmr.c
    File: alt_i2c.c
    File: alt_nand.c
    File: alt_qspi.c
    File: alt_spi.c
    File: alt_timers.c
    File: alt_watchdog.c
    Folder: soc_a10
    Folder: soc_cv_av
    --> \src\hwmgr\soc_cv_av
    File: alt_bridge_f2s_armcc.s
    File: alt_bridge_f2s_gnu.s
    File: alt_clock_manager.c
    File: alt_clock_manager_init.c
    <-- \src\hwmgr
    Folder: soc_a10
    --> \src\hwmgr\soc_a10
    File: alt_clock_manager.c
    File: alt_ecc.c
    File: alt_reset_manager.c
    File: alt_system_manager.c
    <-- \src\hwmgr
    <-- \src\hwmgr
    <<<<---- \include
    File: alt_16550_uart.h
    File: alt_can.h
    File: alt_can_private.h
    File: alt_generalpurpose_io.h
    File: alt_globaltmr.h
    File: alt_i2c.h
    File: alt_nand.h
    File: alt_printf.h
    File: alt_qspi.h
    File: alt_spi.h
    File: alt_timers.h
    File: alt_watchdog.h
    File: hwlib.h
    Folder: safeclib
    Folder: soc_a10
    Folder: soc_cv_av
    --> \include\soc_cv_av
    File: alt_clock_group.h
    File: alt_clock_manager.h
    File: alt_config.h
    File: alt_int_device.h
    File: alt_reset_manager.h
    File: alt_system_manager.h
    Folder: socal
    --> \include\soc_cv_av\socal
    File: alt_acpidmap.h
    File: alt_can.h
    File: alt_clkmgr.h
    File: alt_dap.h
    File: alt_dmanonsecure.h
    File: alt_dmasecure.h
    File: alt_emac.h
    File: alt_f2h.h
    File: alt_fpgamgrdata.h
    File: alt_gpio.h
    File: alt_h2f.h
    File: alt_i2c.h
    File: alt_l3.h
    File: alt_l4wd.h
    File: alt_lwfpgaslvs.h
    File: alt_lwh2f.h
    File: alt_mpu_registers.h
    File: alt_nand.h
    File: alt_nanddata.h
    File: alt_ocram.h
    File: alt_qspi.h
    File: alt_qspidata.h
    File: alt_rom.h
    File: alt_rstmgr.h
    File: alt_scanmgr.h
    File: alt_sdr.h
    File: alt_spim.h
    File: alt_spis.h
    File: alt_stm.h
    File: alt_sysmgr.h
    File: alt_tmr.h
    File: alt_uart.h
    File: alt_usb.h
    File: hps.h
    File: pll_config.h
    File: socal.h
    <-- \include\soc_cv_av
    <-- \include\soc_cv_av
    <<<<---- \include
    Folder: safeclib
    Folder: soc_a10
    --> \include\soc_a10
    File: alt_clock_manager.h
    File: alt_config.h
    File: alt_int_device.h
    File: alt_reset_manager.h
    Folder: socal
    --> \include\soc_a10\socal
    File: alt_clkmgr.h
    File: alt_ecc_dmac.h
    File: alt_ecc_emac0_rx_ecc.h
    File: alt_ecc_emac0_tx_ecc.h
    File: alt_ecc_emac1_rx_ecc.h
    File: alt_ecc_emac1_tx_ecc.h
    File: alt_ecc_emac2_rx_ecc.h
    File: alt_ecc_emac2_tx_ecc.h
    File: alt_ecc_hmc_ocp.h
    File: alt_ecc_nand.h
    File: alt_ecc_nandr.h
    File: alt_ecc_nandw.h
    File: alt_ecc_ocram_ecc.h
    File: alt_ecc_otg0_ecc.h
    File: alt_ecc_otg1_ecc.h
    File: alt_ecc_qspi.h
    File: alt_ecc_sdmmc.h
    File: alt_emac.h
    File: alt_fpgamgr.h
    File: alt_fpgamgrdata.h
    File: alt_gpio.h
    File: alt_i2c.h
    File: alt_io48_hmc_mmr.h
    File: alt_nand.h
    File: alt_noc_fw_ddr_l3_scr.h
    File: alt_noc_fw_ddr_mpu_f2sdr_ddr_scr.h
    File: alt_noc_fw_h2f_scr.h
    File: alt_noc_fw_l4_per_scr.h
    File: alt_noc_fw_l4_sys_scr.h
    File: alt_noc_fw_ocram_scr.h
    File: alt_noc_l4_priv_flt.h
    File: alt_noc_mpu_acp_rate_ad_main_rate.h
    File: alt_noc_mpu_cs.h
    File: alt_noc_mpu_ddr.h
    File: alt_noc_mpu_dma_m0_qos.h
    File: alt_noc_mpu_emac0.h
    File: alt_noc_mpu_emac1.h
    File: alt_noc_mpu_emac2.h
    File: alt_noc_mpu_f2h_axi128_qos.h
    File: alt_noc_mpu_f2h_axi32_qos.h
    File: alt_noc_mpu_f2h_axi64_qos.h
    File: alt_noc_mpu_f2h_rate_ad_main_rate.h
    File: alt_noc_mpu_f2sdr0_axi128_qos.h
    File: alt_noc_mpu_f2sdr0_axi32_qos.h
    File: alt_noc_mpu_f2sdr0_axi64_qos.h
    File: alt_noc_mpu_f2sdr1_axi32_qos.h
    File: alt_noc_mpu_f2sdr1_axi64_qos.h
    File: alt_noc_mpu_f2sdr2_axi128_qos.h
    File: alt_noc_mpu_f2sdr2_axi32_qos.h
    File: alt_noc_mpu_f2sdr2_axi64_qos.h
    File: alt_noc_mpu_l3toh2fresp_main_rate.h
    File: alt_noc_mpu_l4.h
    File: alt_noc_mpu_m0_main_qos.h
    File: alt_noc_mpu_m0_rate_adresp_main_rate.h
    File: alt_noc_mpu_m1toddrresp_main_rate.h
    File: alt_noc_mpu_m1_main_qos.h
    File: alt_noc_mpu_nand_m_main_qos.h
    File: alt_noc_mpu_prb.h
    File: alt_noc_mpu_sdmmc_m_main_qos.h
    File: alt_noc_mpu_usb0_m_main_qos.h
    File: alt_noc_mpu_usb1_m_main_qos.h
    File: alt_pinmux.h
    File: alt_qspi.h
    File: alt_rstmgr.h
    File: alt_sdmmc.h
    File: alt_spim.h
    File: alt_spis.h
    File: alt_sysmgr.h
    File: alt_tmr.h
    File: alt_uart.h
    File: alt_usb.h
    File: hps.h
    File: socal.h
    <-- \include\soc_a10
    <-- \include\soc_a10
    <<<<---- \include
    Folder: safeclib
    --> \include\safeclib
    File: safe_lib.h
    File: safe_lib_errno.h
    File: safe_mem_lib.h
    File: safe_str_lib.h
    File: safe_types.h
    File: snprintf_s.h
    <-- \include
    <-- \include
    <<<<---- \include
    ==== File processing done ====

--> Generate include folders for "hwlib"
   Add include path: src/safeclib
   Add include path: include
   Add include path: include/soc_cv_av
   Add include path: include/soc_cv_av/socal
   Add include path: include/soc_a10
   Add include path: include/soc_a10/socal
   Add include path: include/safeclib
   Generatation of TCL component TCL script for hwlib done

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

--> Generate TCL component TCL script for custom user files

--> Generate TCL component TCL script for EthernetIF
--> Progress every file in folder structure "EthernetIF"

    Folder: FPGA-writeBridge
    Folder: readme
    Folder: source
    --> \source
    File: alt_dma.c
    File: alt_dma.h
    File: alt_fpgamgr.h
    File: alt_fpgamgrdata.h
    File: alt_fpga_manager.c
    File: alt_fpga_manager.h
    File: alt_printf.h
    File: CHECKSUMFILE
    File: CMakeLists.txt
    File: FPGA-status.vcxproj
    File: hps.h
    File: hwlib.h
    File: main.cpp
    File: socal.h
    <--
    Folder: FPGA-writeBridge
    Folder: readme
    --> \readme
    Folder: images
    File: readme.html
    File: stylesheet.css
    --> \readme\images
    File: ArchOptions.gif
    File: ChangeRemote.gif
    File: debuggerexport.png
    File: firstconnection.png
    File: linker.png
    File: ManageConnections.gif
    File: OutputTypes.gif
    File: postbuild.png
    <-- \readme
    <-- \readme
    <<<<---- \FPGA-writeBridge
    File: CHECKSUMFILE
    File: CMakeLists.txt
    File: FPGA-WriteBridge.vcxproj
    File: hps.h
    File: main.cpp
    Folder: readme
    --> \FPGA-writeBridge\readme
    Folder: images
    File: readme.html
    File: stylesheet.css
    --> \FPGA-writeBridge\readme\images
    File: ArchOptions.gif
    File: ChangeRemote.gif
    File: debuggerexport.png
    File: firstconnection.png
    File: linker.png
    File: ManageConnections.gif
    File: OutputTypes.gif
    File: postbuild.png
    <-- \FPGA-writeBridge\readme
    <-- \FPGA-writeBridge\readme
    <<<<---- \FPGA-writeBridge
    ==== File processing done ====

--> Generate include folders for "EthernetIF"
   Add include path: source
   Add include path: FPGA-writeBridge
   Generatation of TCL component TCL script for EthernetIF done

################################################################################
#                                                                              #
#  OPTIONAL: EDIT THE GENERATE TCL SCRIPT FOR CUSTOM COMPONENTS                #
#                                                                              #
#  Add this point it is possible to edit the autogenerated TCL Scripts for the #
#  custom components                                                           #
#                                                                              #
-------------------------------------------------------------------------------
#  Open and edit following file/s:                                             #
         for the Component "EthernetIF":
C:\intelFPGA_lite\19.1\nios2eds\components\EthernetIF\EthernetIF_sw.tcl
------------------------------------------------------------------------------
Type anything to continue ...

 --> Copy Demo files to the Quartus Example folder
--> Remove old component folder: freertos_c1
--> Generate XML Demo project template File
--> Open the Intel NIOS II Command Shell

   Check that the NIOS II Command Shell works porterly
    looks ok
------------------------------------------------
Altera Nios2 Command Shell

Version 19.1, Build 670
------------------------------------------------
--> Navigate to the Quartus Project Folder
--> Generate now Eclipse for NIOS components by executing the TCL scripts
   Windows 10 Version for 19.1
2020.06.07.12:16:24 Info: Doing: <b>ip-make-ipx --source-directory=. --output=components.ipx</b>
2020.06.07.12:16:24 Info: Using factories: JarFactory, TclModuleFactory, BeanElementFactory, PresetFactory, QsysFactory, IPXactBlackBoxFactory, EmbeddedSwTclDriverFactory
2020.06.07.12:16:24 Info: (0) searching <b>C:/intelFPGA_lite/19.1/nios2eds/components/**/*</b> (command line switch)
2020.06.07.12:16:24 Info: Loading altera_hal/altera_hal_sw.tcl
2020.06.07.12:16:24 Info: Loading altera_hostfs/altera_hostfs_sw.tcl
2020.06.07.12:16:25 Info: Loading altera_iniche/altera_iniche_sw.tcl
2020.06.07.12:16:25 Info: Loading altera_nios2/altera_nios2_hal_sw.tcl
2020.06.07.12:16:25 Info: Loading altera_nios2/altera_nios2_qsys_hal_sw.tcl
2020.06.07.12:16:25 Info: Loading altera_nios2/altera_nios2_qsys_hw.tcl
2020.06.07.12:16:25 Info: Loading altera_nios2/altera_nios2_qsys_ucosiii_sw.tcl
2020.06.07.12:16:25 Info: Loading altera_nios2/altera_nios2_qsys_ucosii_sw.tcl
2020.06.07.12:16:25 Info: Loading altera_nios2/altera_nios2_ucosiii_sw.tcl
2020.06.07.12:16:25 Info: Loading altera_nios2/altera_nios2_ucosii_sw.tcl
2020.06.07.12:16:25 Info: Loading altera_nios2/nios2-wizard.jar
2020.06.07.12:16:25 Info: Loading altera_nios2/nios2-wizard.jar
2020.06.07.12:16:25 Info: Loading altera_nios2_gen2/altera_nios2_hal_sw.tcl
2020.06.07.12:16:25 Info: Loading altera_nios2_gen2/altera_nios2_hw.tcl
2020.06.07.12:16:26 Info: Loading altera_nios2_gen2/altera_nios2_ucosiii_sw.tcl
2020.06.07.12:16:26 Info: Loading altera_nios2_gen2/altera_nios2_ucosii_sw.tcl
2020.06.07.12:16:26 Info: Loading altera_nios2_gen2/altera_nios2_unit_hw.tcl
2020.06.07.12:16:26 Info: Loading altera_quad_seven_seg/altera_quad_seven_seg_sw.tcl
2020.06.07.12:16:26 Info: Loading altera_ro_zipfs/altera_ro_zipfs_sw.tcl
2020.06.07.12:16:26 Info: Loading EthernetIF/EthernetIF_sw.tcl
2020.06.07.12:16:26 Info: Loading FreeRTOS/FreeRTOS_sw.tcl
2020.06.07.12:16:26 Info: Loading hwlib/hwlib_sw.tcl
2020.06.07.12:16:26 Info: Loading micrium_uc_osii/micrium_ucosii_sw.tcl
2020.06.07.12:16:26 Info: Loading top/top_sw.tcl
2020.06.07.12:16:26 Info: <b>C:/intelFPGA_lite/19.1/nios2eds/components/**/*</b> matched 176 files in 1,86 seconds
2020.06.07.12:16:26 Info: Found 22 components

################################################################################
#                                                                              #
#                        GENERATION WAS SUCCESSFUL                             #
# -----------------------------------------------------------------------------#
                                 NEXT STEPS                                    #
#                                                                              #
#                     --- Open ECLIPSE for NIOS II ---                         #
                   (C:\intelFPGA_lite\19.1\nios2eds\bin\eclipse_nios2)
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

C:\Users\robseb\Documents\GitHub\NIOSII_EclipseCompProject>
````
</details>

<br>
<br>

___


# Author

**Robin Sebastian**

*NIOSII_EclipseCompProject* and *rsYocto* are projects, that I have fully developed on my own. No companies are involved in this projects.
Today I'm a Master Student of electronic engineering with the major embedded systems. I‘m looking for an interesting job offer to share and deepen my shown skills starting summer 2020.

[![Gitter](https://badges.gitter.im/rsyocto/community.svg)](https://gitter.im/rsyocto/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Email me!](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](mailto:git@robseb.de)

[![GitHub stars](https://img.shields.io/github/stars/robseb/NIOSII_EclipseCompProject?style=social)](https://GitHub.com/robseb/NIOSII_EclipseCompProject/stargazers/)
[![GitHub watchers](https://img.shields.io/github/watchers/robseb/NIOSII_EclipseCompProject?style=social)](https://github.com/robseb/NIOSII_EclipseCompProject/watchers)
[![GitHub followers](https://img.shields.io/github/followers/robseb?style=social)](https://github.com/robseb)

