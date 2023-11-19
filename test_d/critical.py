import os
import platform
import traceback
import datetime
import psutil
import GPUtil
import sys

# Define the directory for crash log files
log_directory = "crash_logs"

# Create the log directory if it doesn't exist
os.makedirs(log_directory, exist_ok=True)

def get_system_info():
    system_info = f"System: {platform.system()}\n"
    system_info += f"Node: {platform.node()}\n"
    system_info += f"Release: {platform.release()}\n"
    system_info += f"Version: {platform.version()}\n"
    system_info += f"Machine: {platform.machine()}\n"
    system_info += f"Processor: {platform.processor()}\n"

    # RAM information
    svmem = psutil.virtual_memory()
    system_info += f"Total RAM: {svmem.total} bytes\n"
    system_info += f"Available RAM: {svmem.available} bytes\n"
    system_info += f"RAM Usage: {svmem.percent}%\n"

    # GPU information
    gpus = GPUtil.getGPUs()
    for i, gpu in enumerate(gpus):
        system_info += f"GPU {i} - Name: {gpu.name}, Memory Total: {gpu.memoryTotal}, Memory Used: {gpu.memoryUsed}, GPU Usage: {gpu.load * 100}%\n"

    return system_info

def create_crash_log(error_message, system_info):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = os.path.join(log_directory, f"crash_log_{timestamp}.txt")
    with open(file_name, 'w') as file:
        file.write("System Information:\n")
        file.write(system_info)
        file.write("\n\nCritical Error:\n")
        file.write(error_message)

def main():
    # Simulate different critical errors and log them
    error_messages = [
        "Critical Error: The ABC feature encountered a severe issue.",
        "Critical Error: Invalid user input detected.",
        "Critical Error: Database connection failed.",
        "Critical Error: Out of disk space.",
        "Critical Error: Network communication error.",
        "Critical Error: File not found.",
        "Critical Error: Configuration file is missing or corrupted.",
        "Critical Error: Security breach detected.",
        "Critical Error: Internal server error."
    ]

    for error_message in error_messages:
        try:
            # Simulate different error scenarios here
            if "Database" in error_message:
                # Simulate a database connection failure
                raise ConnectionError(error_message)
            elif "File not found" in error_message:
                # Simulate a file not found error
                raise FileNotFoundError(error_message)
            else:
                # Simulate a generic error
                raise Exception(error_message)
        except Exception as e:
            exception_info = traceback.format_exc()
        else:
            exception_info = "INFO: Normal Operation"
        system_info = get_system_info()
        create_crash_log(error_message, system_info)

if __name__ == '__main__':
    main()
