[![Coverage Status](https://coveralls.io/repos/github/Beakerboy/MS-CFB/badge.png?branch=main)](https://coveralls.io/github/Beakerboy/MS-CFB?branch=main) ![Build Status](https://github.com/Beakerboy/MS-CFB/actions/workflows/python-package.yml/badge.svg)
# MS-CFB

## About
MS-CFB allows users to create, modify, and disassemble Microsoft Compound File Binary Files. This software can be used from the command line, or as a library within other projects.

This software operates as recommended in the [Microsoft interoperability guidelines](https://winprotocoldoc.blob.core.windows.net/productionwindowsarchives/MS-CFB/%5bMS-CFB%5d.pdf) 

## Requirements
MS-CFB is tested on python 3.7 and higher.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install MS_OVBA_Compression.
```
pip install git+https://github.com/Beakerboy/MS-CFB
```

## Getting Started
MS-CFB will take a specified directory, and combine all directories and files within the directory tree into a compound binary file. Each storage directory will be given the name of the directory, and each stream directory will be given the name of the file minus its extension.

For example, the following
```
./project
├── PROJECT.txt
└───VBA
     ├── Sheet1.bin
     ├── ThisWorkbook.bin
     ├── Module1.bin
     ├── dir.bin
     └── _VBA_PROJECT
```

Will be transformed to:
```
Root Entry
├── PROJECT
└───VBA
     ├── Sheet1
     ├── ThisWorkbook
     ├── Module1
     ├── dir
     └── _VBA_PROJECT
```
To run the program
```
python ole_file.py [-h] [-c] [-l] [-x] [-v {3,4}]
                   [-f FILE] [-X EXTRA]
                   [directory]

positional arguments:
  directory             The input or output directory.

options:
  -h, --help            show this help message and
                        exit
  -c, --create          Create an OLE file from a
                        directory.
  -l, --list            Display metadata on the OLE
                        file and list the files that
                        it contains.
  -x, --extract         Extract files from an OLE file
                        to a directory.
  -v {3,4}, --version {3,4}
                        The OLE version to use.
  -f FILE, --file FILE  The input or output bin file
                        name
  -X EXTRA, --extra EXTRA
                        Path to exta settings yml
                        file.

examples:
  python -m ms_cfb -c -f vbaProject.bin -v 3 -X info.yml ./project

  python -m ms_cfb -x -f vbaProject.bin ./project

  python -m ms_cfb -l -f vbaProject.bin
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
The tests directory contains examples of how the classes can be used within other projects. There are also complete functional tests that include full working examples of creating the OLE file from CLI or using the module's objects.

## Contributing
Contributions are welcome. Please ensure new features include unit tests to maintain 100% coverage. All code must adhere to the [PEP8 Standards](https://peps.python.org/pep-0008/) for both formatting and naming. Method signatures must be fully annotated.

