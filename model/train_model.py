import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report


# Load dataset
df = pd.read_csv("data/heart.csv")

print("Dataset loaded successfully!")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())


# Features and target
X = df.drop("target", axis=1)
y = df["target"]


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Scaling
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# KNN model
model = KNeighborsClassifier(n_neighbors=5)

model.fit(X_train_scaled, y_train)


# Prediction
y_pred = model.predict(X_test_scaled)


# Evaluation
accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# Save model
with open("model/heart_disease_model.pkl", "wb") as file:
    pickle.dump(model, file)


# Save scaler
with open("model/scaler.pkl", "wb") as file:
    pickle.dump(scaler, file)


print("\nModel saved successfully!")
print("Scaler saved successfully!")