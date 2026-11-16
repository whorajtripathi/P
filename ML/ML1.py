
# Uber Ride Fare Prediction using Machine Learning

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# 1. Load Dataset
df = pd.read_csv("uber.csv")

print("Dataset:")
print(df.head())

# 2. Preprocessing
df = df.dropna()

df = df.drop_duplicates()

# Convert pickup_datetime into datetime format
df["pickup_datetime"] = pd.to_datetime(
    df["pickup_datetime"], errors="coerce", utc=True
)

df = df.dropna(subset=["pickup_datetime"])

# Extract date and time features
df["hour"] = df["pickup_datetime"].dt.hour
df["day"] = df["pickup_datetime"].dt.day
df["month"] = df["pickup_datetime"].dt.month
df["day_of_week"] = df["pickup_datetime"].dt.dayofweek

# Calculate distance using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):

    lat1, lon1, lat2, lon2 = np.radians(
        [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2)
        * np.sin(dlon / 2) ** 2
    )

    c = 2 * np.arcsin(np.sqrt(a))

    return 6371 * c

df["distance"] = calculate_distance(
    df["pickup_latitude"],
    df["pickup_longitude"],
    df["dropoff_latitude"],
    df["dropoff_longitude"]
)

# Remove invalid records
df = df[
    (df["fare_amount"] > 0) &
    (df["passenger_count"] > 0) &
    (df["passenger_count"] <= 6) &
    (df["pickup_latitude"].between(-90, 90)) &
    (df["dropoff_latitude"].between(-90, 90)) &
    (df["pickup_longitude"].between(-180, 180)) &
    (df["dropoff_longitude"].between(-180, 180)) &
    (df["distance"] > 0) &
    (df["distance"] <= 100)
]

# 3. Identify and Remove Outliers using IQR
Q1 = df["fare_amount"].quantile(0.25)
Q3 = df["fare_amount"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

df = df[
    (df["fare_amount"] >= lower) &
    (df["fare_amount"] <= upper)
]

print("\nDataset after preprocessing:")
print(df.head())

# 4. Check Correlation
features = [
    "pickup_longitude",
    "pickup_latitude",
    "dropoff_longitude",
    "dropoff_latitude",
    "passenger_count",
    "distance",
    "hour",
    "day",
    "month",
    "day_of_week",
    "fare_amount"
]

plt.figure(figsize=(10, 7))

sns.heatmap(
    df[features].corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")
plt.show()

# 5. Select Features and Target
X = df[
    [
        "pickup_longitude",
        "pickup_latitude",
        "dropoff_longitude",
        "dropoff_latitude",
        "passenger_count",
        "distance",
        "hour",
        "day",
        "month",
        "day_of_week"
    ]
]

y = df["fare_amount"]

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6. Linear Regression Model
lr = LinearRegression()

lr.fit(X_train, y_train)

lr_pred = lr.predict(X_test)

# 7. Random Forest Regression Model
rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)

rf_pred = rf.predict(X_test)

# 8. Evaluate Models
def evaluate_model(name, actual, predicted):

    r2 = r2_score(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mae = mean_absolute_error(actual, predicted)

    print("\n", name)
    print("R2 Score:", r2)
    print("RMSE:", rmse)
    print("MAE:", mae)

    return r2, rmse, mae

lr_scores = evaluate_model(
    "Linear Regression", y_test, lr_pred
)

rf_scores = evaluate_model(
    "Random Forest Regression", y_test, rf_pred
)

# 9. Compare Models
comparison = pd.DataFrame({
    "Model": ["Linear Regression", "Random Forest"],
    "R2 Score": [lr_scores[0], rf_scores[0]],
    "RMSE": [lr_scores[1], rf_scores[1]],
    "MAE": [lr_scores[2], rf_scores[2]]
})

print("\nModel Comparison:")
print(comparison)

# 10. Predict Uber Fare for a New Ride
print("\nEnter New Ride Details:")

pickup_longitude = float(input("Pickup Longitude: "))
pickup_latitude = float(input("Pickup Latitude: "))
dropoff_longitude = float(input("Dropoff Longitude: "))
dropoff_latitude = float(input("Dropoff Latitude: "))
passenger_count = int(input("Passenger Count: "))
hour = int(input("Pickup Hour (0-23): "))
day = int(input("Pickup Day (1-31): "))
month = int(input("Pickup Month (1-12): "))
day_of_week = int(input("Day of Week (0-6): "))

distance = calculate_distance(
    pickup_latitude,
    pickup_longitude,
    dropoff_latitude,
    dropoff_longitude
)

new_ride = pd.DataFrame([{
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count,
    "distance": distance,
    "hour": hour,
    "day": day,
    "month": month,
    "day_of_week": day_of_week
}])

print("\nPredicted Fare using Linear Regression:",
      lr.predict(new_ride)[0])

print("Predicted Fare using Random Forest:",
      rf.predict(new_ride)[0])
