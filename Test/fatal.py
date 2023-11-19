import os
import platform
import traceback
import datetime
import random
import psutil
import GPUtil
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# Function to get system information
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

# Function to create crash log
def create_crash_log(exception_info, system_info, error_type, folder_path):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"crash_log_{error_type}_{timestamp}.txt"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w') as file:
        file.write(f"Error Type: {error_type}\n")
        file.write("System Information:\n")
        file.write(system_info)
        file.write("\n\nException Information:\n")
        file.write(exception_info)

# Generate random errors
def generate_random_errors(folder_path, num_errors=5):
    error_types = ["ZeroDivisionError", "NameError", "AssertionError", "TypeError", "ValueError"]
    for _ in range(num_errors):
        error_type = random.choice(error_types)
        try:
            if error_type == "ZeroDivisionError":
                x = 1 / 0
            elif error_type == "NameError":
                print(my_variable)
            elif error_type == "AssertionError":
                assert False, "This is an assertion error."
            elif error_type == "TypeError":
                a = "5" + 5
            elif error_type == "ValueError":
                int("string")
        except Exception as e:
            exception_info = traceback.format_exc()
            system_info = get_system_info()
            create_crash_log(exception_info, system_info, error_type, folder_path)

# Training the model
def train_model(folder_path):
    data = []
    targets = []
    for file in os.listdir(folder_path):
        if file.startswith("crash_log"):
            error_type = file.split("_")[2]
            targets.append(error_type)
            with open(os.path.join(folder_path, file), 'r') as f:
                data.append(f.read())

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data)

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(targets)
    y = to_categorical(y)

    X_train, X_test, y_train, y_test = train_test_split(X.toarray(), y, test_size=0.2, random_state=42)

    model = Sequential()
    model.add(Dense(512, input_shape=(X_train.shape[1],), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(label_encoder.classes_), activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.0001), metrics=['accuracy'])

    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

if __name__ == '__main__':
    folder_path = "crash_logs"  # Folder with crash logs
    os.makedirs(folder_path, exist_ok=True)
    generate_random_errors(folder_path, num_errors=5)
    train_model(folder_path)
