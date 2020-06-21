# Offline-Python-Packager
Export and then Import your python packages to an offline environment from a directory.  
Define a local directory that will serves as a python-packages repo index for your offline pacakges installations.    
See [examples](#Examples) below


## Usage
```python
python3 main.py --help  

usage: main.py [-h] [-ep [EXPORT_PACKAGES]] [-et [EXPORT_TO]]
               [-ip [IMPORT_PACKAGES]] [-if [IMPORT_FROM]]
               [-pip [PIP_EXECUTABLE]] [-epa [EXTRA_PIP_ARGS]] [-l [LOG_FILE]]
               [-v]

Offline Exporter & Importer for python packages

optional arguments:
  -h, --help            show this help message and exit
  -ep [EXPORT_PACKAGES], --export_packages [EXPORT_PACKAGES]
                        Export packages that match pattern. Pass "*" for exporting all packages
  -et [EXPORT_TO], --export_to [EXPORT_TO]
                        Export packages to this path
  -ip [IMPORT_PACKAGES], --import_packages [IMPORT_PACKAGES]
                        Import packages that match pattern. Pass "*" for importing all packages
  -if [IMPORT_FROM], --import_from [IMPORT_FROM]
                        Import python packages from this path
  -pip [PIP_EXECUTABLE], --pip_executable [PIP_EXECUTABLE]
                        Use this pip.exe
  -epa [EXTRA_PIP_ARGS], --extra_pip_args [EXTRA_PIP_ARGS]
                        Extra pip.exe args like: --no-index
  -l [LOG_FILE], --log_file [LOG_FILE]
                        File path to write logs to
  -v, --verbose         More awesome printings.

```

Say you want to move all your installed packages to an offline env. Execute:  
```python
python3 main.py --export_packages  
```  
Your packages will be waiting at: `./exported_packages`.  
Copy **exported_packages** dir and this script to your offline env, and install the exported packages by executing:  
```python
python3 main.py --import_packages  
```  
You can export **specific packages** and then install them:  
```python  
# Export
python3 main.py --export_packages "cffi,tornado" --export_to "/opt/sources/my_packages"  
  
# Import
python3 main.py --import_packages "cffi,tornado" --import_from "/opt/sources/my_packages"  
```  
Export using **requirements.txt** file  
```python  
# Export
python3 main.py --export_packages "/opt/sources/requirements.txt" --export_to "/opt/sources/my_packages"  
  
# Import  
python3 main.py --import_packages "/opt/sources/requirements.txt" --import_from "/opt/sources/my_packages"  
```
 

## Special Envs
You can use these special env vars that are defined during the app's execution:  
- ** `OFFLINE_PYTHON_PACKAGER_HOME` ** - Path to executable dir. If main.py script is located ar: "C:\\Git\\Offline-Python-Packager\\main.py" then OFFLINE_PYTHON_PACKAGER_HOME=C:\\Git\\Offline-Python-Packager  
- ** `OFFLINE_PYTHON_PACKAGER_EXECUTABLE` ** - Path to executable file. If main.py script is located ar: "C:\\Git\\Offline-Python-Packager\\main.py" then OFFLINE_PYTHON_PACKAGER_HOME=C:\\Git\\Offline-Python-Packager\\main.py  
  
Sample usage as a parameter: **"${OFFLINE_PYTHON_PACKAGER_HOME}"**  
Example:  
`python main.py -ep "${OFFLINE_PYTHON_PACKAGER_HOME}\packages.txt"`  

If executing from Bash then you need to escape the env var:  
`python main.py -ep "\${OFFLINE_PYTHON_PACKAGER_HOME}\packages.txt"`


## Requirements

#### Python
* At least v3

#### libs
* tabulate
* pip2pi



## Test
Quick test windows batch script at: [RunTests](tests/RunTests.bat)

## PyInstaller
To pack this tool into one windows executable run script: [Compile_Exe](pyinstaller/Compile_Exe.bat)

## Examples

### Windows Examples

NOTE: All examples below are for **windows CMD**. When executing from Bash then you need to escape every '\\' with double a slash '\\\\' and every '$' sign with '\\$'


By default exported packages go to: "${OFFLINE_PYTHON_PACKAGER_HOME}\\exported_pacages"  
You can override this path by specifying: `-et, --export_to [EXPORT_TO]` flag.

##### Export packages
* Export all your local packages to default exported packages dir:     
`python main.py -ep`
* Export specific packages:  
`python main.py -ep "vboxapi==1.0, virtualbox, wrapt, tornado==6.0.4"`
* Export specific packages also from text file:  
`python main.py -ep "pywin32==227, pefile==2019.4.18, C:\packages.txt"`  
Must have the format of **pip freeze** command: **pkg_namg==pkg_version**  in each line.
* Export specific packages from text file using special env var:  
`python main.py -ep "pywin32==227, pefile==2019.4.18, ${OFFLINE_PYTHON_PACKAGER_HOME}\packages.txt"`  
packages.txt is next to main.py
##### Export to location
* Export all your local packages to default exported pacakges location:  
`python main.py -ep`
* Same as above:  
`python main.py -ep "*"`
* Export all your local packages to specific location:  
`python main.py -ep -et C:\dist\my-packages`
* Export specific packages to specific location:  
`python main.py -ep "pywin32==227, pefile==2019.4.18, ${OFFLINE_PYTHON_PACKAGER_HOME}\packages.txt" -et "C:\dist\my-packages"`
* Export specific packages with logging to file:  
`python main.py -ep "pywin32==227, pefile==2019.4.18, ${OFFLINE_PYTHON_PACKAGER_HOME}\packages.txt" -et "C:\dist\my-packages" -l "${OFFLINE_PYTHON_PACKAGER_HOME}\MyLog.log"`


##### Import packages
* Import all packages from default exported packages dir:   
`python main.py -ip `
* Same:   
`python main.py -ip "*" `
* Import all packages from specific dir:  
`python main.py -ip "*" -if "C:\dist\my-packages"`
* Import specific packages from specific dir:  
`python main.py -ip "pywin32==227, pefile==2019.4.18, ${OFFLINE_PYTHON_PACKAGER_HOME}\packages.txt" -if "C:\dist\my-packages"`
* Import specific packages with logging to file:  
`python main.py -ip "pywin32==227, pefile==2019.4.18, ${OFFLINE_PYTHON_PACKAGER_HOME}\packages.txt" -if "C:\dist\my-packages" -l "${OFFLINE_PYTHON_PACKAGER_HOME}\MyLog.log"`



### Linux Examples

* Export all your local packages:  
`python3 main.py -ep`

* Extra pip args:   
`python3 main.py -ip -epa "--index-url=http://myserv1:8081/simple/ --trusted-host=myserv1"  -v" `

* Import all packages from default exported packages dir:   
`python3 main.py -ip `


## Credits
David Wolever | https://github.com/wolever/pip2pi based on the awesome work [pip2pi](https://pypi.org/project/pip2pi/) of @wolever 