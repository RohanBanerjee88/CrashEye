import platform
import traceback
import datetime
import sys
import psutil
import GPUtil

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

def create_crash_log(exception_info, system_info):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"crash_log_{timestamp}.txt"
    with open(file_name, 'w') as file:
        file.write("System Information:\n")
        file.write(system_info)
        file.write("\n\nException Information:\n")
        file.write(exception_info)

def main():
    try:
        # Your main program logic goes here
        # Simulate a fatal error for demonstration purposes
        sys.exit("This is a fatal error. Program closed.")
    except SystemExit as e:
        exception_info = traceback.format_exc()
        system_info = get_system_info()
        create_crash_log(exception_info, system_info)

if __name___ == '__main__':
    main()