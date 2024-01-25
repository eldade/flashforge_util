import time
import api
import os
from api import *

def get_estimated_remaining_time(start_byte, start_time, current_byte, current_time, total_bytes):
    if current_byte == start_byte:
        # No progress made or still at the initial byte, cannot estimate time
        return None

    bytes_printed_since_start = current_byte - start_byte
    time_elapsed_since_start = current_time - start_time

    if bytes_printed_since_start > 0:
        total_time_estimate = (time_elapsed_since_start / bytes_printed_since_start) * (total_bytes - start_byte)
        remaining_time = total_time_estimate - time_elapsed_since_start
        return max(0, remaining_time)  # Ensure it's not negative
    return None


def report_print_status(socket):
    start_time = time.time()
    status = get_printer_status(socket)

    progress = get_print_progress(socket)
    start_byte = int(progress['BytesPrinted'])

    while True:
        status = get_printer_status(socket)

        if status['CurrentFile'] == None:
            print ('No active print job.')
            return

        temperatures = get_temperatures(socket)
        progress = get_print_progress(socket)

        remaining_time = get_estimated_remaining_time(start_byte, start_time, int(progress['BytesPrinted']), time.time(), int(progress['BytesTotal']))

        # Clear the line and print the status
        print("\033[K", end='\r')  # Clear the line
        print(f"File: {os.path.basename(status['CurrentFile'])}  Progress: {progress['PercentageCompleted']:.1f}%  ", end='')
        print(f"Extruder: {temperatures['Extruder_Current']}°C/{temperatures['Extruder_Target']}°C, Platform: {temperatures['Platform_Current']}°C/{temperatures['Platform_Target']}°C  ", end='')
        if remaining_time:
            print(f"Time Remaining: ", end='')
            hours = remaining_time // 3600
            days = remaining_time // 3600 // 24
            minutes = remaining_time // 60 % 60

            if days > 0:
                print(f"{days:.0f}d " ,end='')

            if hours > 0:
                print(f"{hours:.0f}h ",end='')

            if minutes > 0:
                print(f"{minutes:.0f}m ",end='')

        time.sleep(1)  # Update every second