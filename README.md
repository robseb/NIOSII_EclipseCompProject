# Concept

![Alt text](doc/Concept.png?raw=true "Concept illustration")

<br>

**Python Script to automatically generate a Intel NIOS II Eclipse Demo Project with a custom configuration**

The Python script automatically generate by the user-specified an optimized Eclipse Demo project for the Intel NIOS II Embedded Design Suite IDE.
It should help to automate the often complicate and always equal project setup process with custom libraries and real-time operating systems, such as FreeRTOS. 

# Selectable Components
The list of selected comports, that can be automatically cloned from Github will updated. <br>
Now, are following components available: 

| Components | Description
|:--|:--|
| [**FreeRTOS-Kernel**](https://github.com/FreeRTOS/FreeRTOS-Kernel) *for NIOS II*    | The latest FreeRTOS Version cloned from Github  |
| [**Intel hwlib**](https://github.com/robseb/hwlib) optimazed for NIOS II    | Library for accessing HPS components of SoC-FPGAs with NIOS II |
|  `Custom Code folders` | Inserted folders with user libraries 

# Supported Platforms 

* **Desktop OS**
    * **Windows 10**
    * **Ubuntu Linux**
* **IDE**
    * Intel Quartus Prime including NIOS II EDS

* **Every Intel FPGA with NIOS II support**  
    * For running FreeRTOS is a **Timer** module required 

* Supported SoC-FPGA of the Intel *hwlib* for accessing HPS hard-IP with the NIOS II core
    * **Intel Cyclone V SoC-FPGA**-families 
    * **Intel Arria V SoC-FPGA**-families
    * **Intel Arria 10 SX SoC-FPGA**-family  

# Getting started
## I. Installment of Intel Quartus Prime II with NIOS II support 
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
            * **Alternativ Mirror:** The files are inside the [**Releases**](https://github.com/robseb/NIOSII_EclipseCompProject/releases) of this Github repository available, as well. 
        * **Extract** (unzip) the downloaded file
        * **Rename** the folder "*eclipse*" inside the extracted folder to "*eclipse_nios2*"
        * **Copy** the folder "*eclipse_nios2*" inside the extract folder to:
            * **Windows 10:** "C:\intelFPGA_lite\19.1\nios2eds\bin"
            * **Ubuntu:**  "intelFPGA_lite\19.1\nios2eds\bin"
        * **Extract** (unzip) the file to a temporary location on the desktop 
            * **Windows 10:** C:\intelFPGA_lite\19.1\nios2eds\bin\eclipse_nios2_plugins.zip
             * **Ubuntu:** intelFPGA_lite\19.1\nios2eds\bin\eclipse_nios2_plugins.tar.gz
        * **Copy** the content of this extracted folder to the before downloaded folder 
            * **Windows 10 :** C:\intelFPGA_lite\19.1\nios2eds\eclispe_nios2
            * **Ubuntu:** intelFPGA_lite\19.1\nios2eds\bin\\eclispe_nios2
            * **Replace** the file in the folder with the new one by merging them together 
            * The folder should now look like:
                ![Alt text](doc/Screenshoot_ContentFolder.png?raw=true "Screenshot of the folder content")

## II. Run the script to generate a new custom Eclipse Project
To use this script to generate a custom Eclipse project for the NIOS II sof-core processor realise follow instructions:
* II.1.: **Clone this Github repository** 
* II.2.: **Open the Windows Command prompt or the Linux Terminal and navigate to the repository folder**
* II.3.: **Install the *Python Pip* module "*dload*" by running following command
    ````shell
    pip3 install dload
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
Follow the displayed instructions of the script to add the available module to your configuration. 
Also, it is enabled to drag & drop folders with custom Code to the "*working_folder*" inside this repository folder. The script will automatically generate for every code folder a NIOS II Eclipse package. This package is pre-installed to the generate NIOS II Example Project. 

## IV. Create a new Eclipse project with the generate example project
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
## VI. Debug the Eclipse project

## VII. Example output of the Python script

<h3> Work under process! </h3>

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
