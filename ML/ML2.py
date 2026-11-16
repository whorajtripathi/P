
# Email Spam Detection using KNN and SVM

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score, 
    f1_score,
    confusion_matrix,
    classification_report
)

# 1. Load Dataset
df = pd.read_csv("spam.csv", encoding="latin-1")

print("Original Dataset:")
print(df.head())

# 2. Select Message and Category Columns
if "v1" in df.columns and "v2" in df.columns:
    df = df.rename(columns={"v1": "label", "v2": "message"})

elif "Category" in df.columns and "Message" in df.columns:
    df = df.rename(columns={"Category": "label", "Message": "message"})

elif "label" in df.columns and "text" in df.columns:
    df = df.rename(columns={"text": "message"})

# Keep only required columns
df = df[["label", "message"]]

# 3. Preprocessing
df = df.dropna()
df = df.drop_duplicates()

df["label"] = df["label"].astype(str).str.lower().str.strip()
df["message"] = df["message"].astype(str).str.lower().str.strip()

# Convert labels into binary values
df["label"] = df["label"].map({
    "ham": 0,
    "not spam": 0,
    "normal": 0,
    "0": 0,
    "spam": 1,
    "abnormal": 1,
    "1": 1
})

df = df.dropna(subset=["label"])
df["label"] = df["label"].astype(int)

print("\nCleaned Dataset:")
print(df.head())

print("\nClass Distribution:")
print(df["label"].value_counts())

# 4. Separate Features and Target
X = df["message"]
y = df["label"]

# 5. Convert Text into Numerical Features
tfidf = TfidfVectorizer(stop_words="english", max_features=5000)

X = tfidf.fit_transform(X)

# 6. Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 7. KNN Model
knn = KNeighborsClassifier(
    n_neighbors=5,
    metric="cosine",
    algorithm="brute"
)

knn.fit(X_train, y_train)

knn_pred = knn.predict(X_test)

# 8. SVM Model
svm = SVC(kernel="linear")

svm.fit(X_train, y_train)

svm_pred = svm.predict(X_test)

# 9. Model Evaluation
def evaluate_model(name, actual, predicted):

    accuracy = accuracy_score(actual, predicted)

    precision = precision_score(
        actual, predicted, zero_division=0
    )

    recall = recall_score(
        actual, predicted, zero_division=0
    )

    f1 = f1_score(
        actual, predicted, zero_division=0
    )

    print("\n", name)
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)

    print("\nClassification Report:")
    print(classification_report(
        actual, predicted,
        target_names=["Not Spam", "Spam"],
        zero_division=0
    ))

    return accuracy, precision, recall, f1


knn_score = evaluate_model(
    "KNN Classification", y_test, knn_pred
)

svm_score = evaluate_model(
    "SVM Classification", y_test, svm_pred
)

# 10. Compare Models
comparison = pd.DataFrame({
    "Model": ["KNN", "SVM"],
    "Accuracy": [knn_score[0], svm_score[0]],
    "Precision": [knn_score[1], svm_score[1]],
    "Recall": [knn_score[2], svm_score[2]],
    "F1 Score": [knn_score[3], svm_score[3]]
})

print("\nModel Comparison:")
print(comparison)

# 11. Confusion Matrix
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
sns.heatmap(
    confusion_matrix(y_test, knn_pred),
    annot=True,
    fmt="d",
    cmap="Blues"
)
plt.title("KNN Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.subplot(1, 2, 2)
sns.heatmap(
    confusion_matrix(y_test, svm_pred),
    annot=True,
    fmt="d",
    cmap="Greens"
)
plt.title("SVM Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.tight_layout()
plt.show()

# 12. Predict a New Email
new_email = input("\nEnter an email message: ")

email_vector = tfidf.transform([new_email.lower()])

knn_result = knn.predict(email_vector)[0]
svm_result = svm.predict(email_vector)[0]

print("\nKNN Prediction:",
      "Spam" if knn_result == 1 else "Not Spam")

print("SVM Prediction:",
      "Spam" if svm_result == 1 else "Not Spam")
