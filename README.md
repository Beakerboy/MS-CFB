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



## Contributing
Contributions are welcome. Please ensure new features include unit tests to maintain 100% coverage. All code must adhere to the [PEP8 Standards](https://peps.python.org/pep-0008/) for both formatting and naming. Method signatures must be fully annotated.

