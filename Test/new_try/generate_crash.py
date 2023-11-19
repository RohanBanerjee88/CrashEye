import random
import os
import logging
from datetime import datetime
import platform
import traceback
import sys
import psutil
import GPUtil
#from sql_aggregator import mysql_data_insert
from crash_logs_upload import upload_crash_to_mongo

# Create a directory for crash logs
if not os.path.exists('./phew_crash_logs'):
    os.makedirs('./phew_crash_logs')

random.seed(str(datetime.now()))

# Configure logging
time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file = f'crash_{time_stamp}.log'
log_filename = f"./phew_crash_logs/{file}"
logging.basicConfig(filename=log_filename, level=logging.DEBUG)

def fatal_error(msg):
    logging.fatal(msg)
    logging.fatal("Fatal error: Segmentation fault")
    raise Exception("Segmentation fault")

def critical_error(msg):
    logging.error(msg)
    logging.error("Critical error: Data corruption")
    raise Exception("Data corruption")

def warning_message(msg):
    logging.warning(msg)
    logging.warning("Warning: High memory usage")

def generate_random_crash():
    pl_sys = platform.system()
    pl_node = platform.node()
    pl_rel = platform.release()
    pl_ver = platform.version()
    pl_mach = platform.machine()
    pl_proc = platform.processor()

    system_info = f"\nSystem: {pl_sys}\n"
    system_info += f"Node: {pl_node}\n"
    system_info += f"Release: {pl_rel}\n"
    system_info += f"Version: {pl_ver}\n"
    system_info += f"Machine: {pl_mach}\n"
    system_info += f"Processor: {pl_proc}\n"

    # RAM information
    svmem = psutil.virtual_memory()
    system_info += f"Total RAM: {svmem.total} bytes\n"
    system_info += f"Available RAM: {svmem.available} bytes\n"
    system_info += f"RAM Usage: {svmem.percent}%\n"

    gpus = GPUtil.getGPUs()

    gpu_sql = None

    for i, gpu in enumerate(gpus):
        if not gpu_sql:
            gpu_sql = gpu.name
        system_info += f"GPU {i} - Name: {gpu.name}, Memory Total: {gpu.memoryTotal}, Memory Used: {gpu.memoryUsed}, GPU Usage: {gpu.load * 100}%\n"

    # logging.log(msg=system_info)

    crash_type = random.randint(0,2)
    if crash_type == 0:
        err_type = "FATAL"
        # mysql_data_insert(file,time_stamp,pl_sys,pl_node,pl_rel,pl_ver,pl_mach,pl_proc,svmem.percent,err_type,gpu_sql)
        upload_crash_to_mongo([file,time_stamp,pl_sys,pl_node,pl_rel,pl_ver,pl_mach,pl_proc,svmem.percent,"FATAL",gpu_sql])
        fatal_error(system_info)
    elif crash_type == 1:
        err_type = "CRITICAL"
        # mysql_data_insert(file,time_stamp,pl_sys,pl_node,pl_rel,pl_ver,pl_mach,pl_proc,svmem.percent,err_type, gpu_sql)
        upload_crash_to_mongo([file,time_stamp,pl_sys,pl_node,pl_rel,pl_ver,pl_mach,pl_proc,svmem.percent,"CRITICAL",gpu_sql])
        critical_error(system_info)
    else:
        err_type = "WARNING"
        # mysql_data_insert(file,time_stamp,pl_sys,pl_node,pl_rel,pl_ver,pl_mach,pl_proc,svmem.percent,err_type, gpu_sql)
        upload_crash_to_mongo([file,time_stamp,pl_sys,pl_node,pl_rel,pl_ver,pl_mach,pl_proc,svmem.percent,"WARNING",gpu_sql])
        warning_message(system_info)



if __name__ == "__main__":
    try:
        generate_random_crash()
    except Exception as e:
        logging.exception("Exception occurred", exc_info=True)