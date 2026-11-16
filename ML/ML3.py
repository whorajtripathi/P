
# Bank Customer Churn Prediction using Neural Network

# 1. Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    precision_score,
    recall_score,
    f1_score
)

# 2. Load Dataset
df = pd.read_csv("Churn_Modelling.csv")

print("Dataset:")
print(df.head())

# 3. Preprocessing
df = df.dropna()
df = df.drop_duplicates()

# Remove unnecessary columns
df = df.drop(
    columns=["RowNumber", "CustomerId", "Surname"],
    errors="ignore"
)

# Separate Features and Target
X = df.drop("Exited", axis=1)
y = df["Exited"]

# Identify numerical and categorical columns
categorical_features = ["Geography", "Gender"]

numerical_features = [
    col for col in X.columns
    if col not in categorical_features
]

# 4. Encode and Scale Data
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"),
         categorical_features)
    ]
)

# 5. Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 6. Create Neural Network Model
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", MLPClassifier(
        hidden_layer_sizes=(16, 8),
        activation="relu",
        solver="adam",
        max_iter=500,
        random_state=42
    ))
])

# 7. Train the Model
model.fit(X_train, y_train)

print("\nNeural Network Model Trained Successfully!")

# 8. Make Predictions
y_pred = model.predict(X_test)

# 9. Evaluate Model
print("\nModel Evaluation")

print("Accuracy:", accuracy_score(y_test, y_pred))

print("Precision:", precision_score(y_test, y_pred))

print("Recall:", recall_score(y_test, y_pred))

print("F1 Score:", f1_score(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 10. Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Not Churned", "Churned"],
    yticklabels=["Not Churned", "Churned"]
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Customer Churn Confusion Matrix")
plt.show()

# 11. Predict New Customer
new_customer = pd.DataFrame([{
    "CreditScore": 600,
    "Geography": "France",
    "Gender": "Male",
    "Age": 40,
    "Tenure": 3,
    "Balance": 60000,
    "NumOfProducts": 2,
    "HasCrCard": 1,
    "IsActiveMember": 1,
    "EstimatedSalary": 50000
}])

prediction = model.predict(new_customer)

probability = model.predict_proba(new_customer)[0][1]

print("\nNew Customer Prediction:")

if prediction[0] == 1:
    print("Customer is likely to leave the bank.")
else:
    print("Customer is likely to stay with the bank.")

print("Churn Probability:", round(probability * 100, 2), "%")
