import argparse
import os
import time
from api import *
import signal
from discover import *
import sys
from print_status import *

socket = None

def main():

    parser = argparse.ArgumentParser(description="FlashForge Printer Utility")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Check if no arguments were provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Subparser for discovering the printer
    discover_parser = subparsers.add_parser('discover', help='Discover the printer')

    # Subparser for retrieving printer info
    info_parser = subparsers.add_parser('info', help='Retrieve printer information')

    # Subparser for listing files
    list_parser = subparsers.add_parser('list-files', help='List files on the printer')

    # Subparser for printer status
    status_parser = subparsers.add_parser('status', help='Get printer status')

    # Subparser for printer status
    temp_parser = subparsers.add_parser('temperatures', help='Get temperatures of extruder and platform')

    # Subparser for resume print command
    resume_parser = subparsers.add_parser('resume', help='Resume a paused print operation')

    # Subparser for pause print command
    pause_parser = subparsers.add_parser('pause', help='Pause an active print operation')

    # Subparser for cancel print command
    cancel_parser = subparsers.add_parser('cancel', help='Stop/cancel an active print operation')

    # Subparser for uploading a file
    upload_parser = subparsers.add_parser('upload', help='Upload a file')
    upload_parser.add_argument('file', help='File to upload')

    # Subparser for printing a file
    print_parser = subparsers.add_parser('print', help='Print a file')
    print_parser.add_argument('file', help='File to print')

    # Subparser for print progress
    progress_parser = subparsers.add_parser('progress', help='Get print progress')

    # Add common arguments
    for subparser in [info_parser, list_parser, status_parser, resume_parser, pause_parser, temp_parser, cancel_parser, upload_parser, print_parser, progress_parser]:
        subparser.add_argument('--ip', help='IP address of the printer')
        subparser.add_argument('--port', default=8899, type=int, help='Port number of the printer')

    args = parser.parse_args()

    if args.command == 'discover':
        printer_name, printer_ip = discover_printer()
        if printer_name and printer_ip:
            print(f"Printer Name: {printer_name}, IP Address: {printer_ip}")
        else:
            print("Printer not found.")

    global socket

    socket = connect({'ip': args.ip, 'port': args.port})

    if socket == None:
        print ("Failed to connect to printer")
        exit(1)

    control = control_obtain(socket)

    if (control == False):
        exit(1)

    printer_info = get_printer_info(socket)

    print (f"Connected to {printer_info['Machine Name']}@{args.ip}, Model={printer_info['Machine Type']} ({printer_info['Firmware']})")

    if args.command == 'info':
        info = get_printer_info(socket)
        print(info)

    elif args.command == 'resume':
        info = resume_print(socket)
        print(info)

    elif args.command == 'pause':
        info = pause_print(socket)
        print(info)

    elif args.command == 'cancel':
        info = cancel_print(socket)
        print(info)

    elif args.command == 'temperatures':
        info = get_temperatures(socket)
        print(info)

    elif args.command == 'list-files':
        file_list = retrieve_file_list(socket)
        print("Files on the printer:")
        for file in file_list:
            print(file)

        print(f"Total number of files: {len(file_list)}")

    elif args.command == 'status':
        status = get_printer_status(socket)
        print(status)

    elif args.command == 'upload':
        upload_file(socket, os.path.expanduser(args.file))

    elif args.command == 'print':
        result = upload_file(socket, os.path.expanduser(args.file))

        if result == True:
            # I am seeing some fairly unpredictable behaviors with the file upload, and no clear way to extract an
            # error code from the request. One reliable way I've found to confirm my upload worked is to grab the file list
            # afterwards and ensure the file is available on the printer...
            upload_found = find_file_on_printer(socket, os.path.basename(args.file))

            if upload_found[0] == True:
                result = print_file(socket, os.path.basename(args.file))
                if result == True:
                    time.sleep(10)
                    report_print_status(socket)
            else:
                print("Upload failed due to unknown reason. Cancelling...")

    elif args.command == 'progress':
        report_print_status(socket)

    control_release(socket)
    socket.close()

def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    print ("\n")

    control_release(socket)
    socket.close()
    sys.exit(1)


if __name__ == '__main__':
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    main()