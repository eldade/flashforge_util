# FlashForge Printer Utility

## Overview
This utility provides experimental support for interacting with FlashForge 3D printers. It has been developed and tested with the FlashForge Guider 2S, but it may work with other models. The utility allows users to discover printers on the network, list files available on the printer, check printer status, and upload files for printing.

## Features
- Discovering printers on the network
- Listing files stored in the printer's internal storage
- Checking the printer's current status
- Uploading files to the printer

## Installation
(Provide instructions on how to install the utility, including any prerequisites or dependencies that need to be installed beforehand.)

## Usage
The utility is command-line based and supports the following commands:

### Discover Printer
Discover and display information about the printer on the network.
```
python main.py discover
```

### Retrieve Printer Information
Get basic information about the printer, such as model and serial number.
```
python main.py info --ip <printer_ip> --port <printer_port>
```

### List Files on Printer
List all files stored on the printer's internal storage.
```
python main.py list-files --ip <printer_ip> --port <printer_port>
```

### Check Printer Status
Get the current status of the printer, including if it is currently printing.
```
python main.py status --ip <printer_ip> --port <printer_port>
```

### Upload File
Upload a file to the printer without printing it. The file path should be absolute or relative to the current directory.
```
python main.py upload --ip <printer_ip> --port <printer_port> <file_path>
```

### Print File
Start printing a file that has already been uploaded to the printer.

```
python main.py print --ip <printer_ip> --port <printer_port> <file_name>
```

### Manage Active Print Job
Stop, pause, and resume an active print job

```
python main.py pause --ip <printer_ip> --port <printer_port>
python main.py resume --ip <printer_ip> --port <printer_port>
python main.py cancel --ip <printer_ip> --port <printer_port>
```


## Credits

This project was derived from work done here [flashforgefinder-protocol](https://github.com/ztripez/flashforgefinder-protocol), though sadly the protocol seems to be a bit different nowadays.

Since I've only tested this on one printer (Guider 2S), I am not sure if these protocol differences are just the protocol evolving over the years, or if there's some printer-specific aspects to this protocol.