## About
MS-CFB allows users to create, modify, and disassemble Microsoft Compound File Binary Files. This software can be used from the command line, or as a library within other projects.

This software operates as recommended in the [Microsoft interoperability guidelines](https://winprotocoldoc.blob.core.windows.net/productionwindowsarchives/MS-CFB/%5bMS-CFB%5d.pdf) 

## Requirements
MS-CFB is tested on python 3.7 and higher.

## Installation
MS-CFB is currently under development, but can be installed from GitHub using `pip`.
```
pip install git+https://github.com/Beakerboy/MS-CFB@dev
```

## Getting Started
MS-CFB will take a specified directory, and combine all directories and files within the directory tree into a compound binary file. Each storage directory will be given the name of the directory, and each stream directory will be given the name of the file minus its extension.

For example, the following
```
./project
├── PROJECT.bin
├── PROJECTwm.bin
└───VBA
     ├── Sheet1.bin
     ├── ThisWorkbook.bin
     ├── Module1.bin
     ├── dir
     └── _VBA_PROJECT
```

Will be transformed to:
```
Root Entry
├── PROJECT
├── PROJECTwm
└───VBA
     ├── Sheet1
     ├── ThisWorkbook
     ├── Module1
     ├── dir
     └── _VBA_PROJECT
```
To run the program
```
python ole_file.py [-h] [-v {3,4}] [-o OUTPUT] [-x EXTRA] directory
positional arguments:
  directory             The directory that contains your files.

optional arguments:
  -h, --help            show this help message and exit
  -v {3,4}, --version {3,4}
                        The OLE version to use.
  -o OUTPUT, --output OUTPUT
                        The output file name.
  -x EXTRA, --extra EXTRA
                        Path to exta directory settings yml file.
```

Some directory settings can be specified from a YAML file. Directory paths are relative to the project root. Users can specify creation and modification date in ISO format, class id as a UUID string, and user flags as a four byte integer.
```yaml
directories:
  .:
    clsid: 56616700-C154-11CE-8553-00AA00A1F95B
  Storage 1:
    created: "1995-11-16 17:43:44"
    clsid: 56616100-C154-11CE-8553-00AA00A1F95B
```

## Tests
The tests directory contains examples of how the classes can be used within other projects. There are also complete functional tests the include full working examples of creating the OLE file from CLI or using the module's objects.

## Contributing
Contributions are welcome. Please ensure new features include unit tests to maintain 100% coverage. All code must adhere to the [PEP8 Standards](https://peps.python.org/pep-0008/) for both formatting and naming. Method signatures must be fully annotated.

