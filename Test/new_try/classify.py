import os
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score

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
        data = []
        labels = []
        for log_file in log_files:
            error_type = detect_error_type(os.path.join('phew_crash_logs', log_file))
            data.append(open(os.path.join('phew_crash_logs', log_file), 'r').read())
            labels.append(error_type)

        # Convert to a DataFrame
        df = pd.DataFrame({'Log': data, 'Error_Type': labels})

        # Vectorize the log content
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df['Log'])

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, df['Error_Type'], test_size=0.2, random_state=42)

        # Train the Support Vector Machine (SVM) model
        svm_model = SVC()
        svm_model.fit(X_train, y_train)

        # Make predictions
        y_pred = svm_model.predict(X_test)

        # Print the classification report and accuracy
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
