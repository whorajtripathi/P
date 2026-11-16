import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Load dataset
df = pd.read_csv('Churn_Modelling.csv')

# One-Hot Encoding
df = pd.get_dummies(df, columns=['Geography', 'Gender'], dtype=int)

# Remove unnecessary columns
df.drop(columns=['RowNumber', 'CustomerId', 'Surname'], inplace=True)

# Split input and output
x = df.drop('Exited', axis=1).values
y = df['Exited'].values

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.25, random_state=20
)

# Feature scaling
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

# Build ANN model
model = Sequential([
    Dense(100, activation='relu', input_shape=(x_train.shape[1],)),
    Dense(1, activation='sigmoid')
])

# Compile model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train model
model.fit(x_train, y_train, epochs=100, batch_size=64,
          validation_split=0.1)

# Prediction
pred = model.predict(x_test)
y_pred = (pred > 0.5).astype(int).ravel()

# Evaluate model
print("Accuracy:", accuracy_score(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(cm).plot()
plt.show()