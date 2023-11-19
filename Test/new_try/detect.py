import os
import re

def detect_error_type(log_file):
    with open(log_file, 'r') as file:
        log_content = file.read()

    if re.search("FATAL", log_content, re.IGNORECASE):
        return "Fatal Error"
    elif re.search("CRITICAL|ERROR", log_content, re.IGNORECASE):
        return "Critical Error"
    elif re.search("WARNING", log_content, re.IGNORECASE):
        return "Warning Message"
    else:
        return "Unknown Error"

if __name__ == "__main__":
    if not os.path.exists('phew_crash_logs'):
        print("Directory 'phew_crash_logs' does not exist.")
    else:
        log_files = os.listdir('phew_crash_logs')
        for log_file in log_files:
            print(f"{log_file}: {detect_error_type(os.path.join('phew_crash_logs', log_file))}")