
import os
import json
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from utils.preprocessing import (
    load_dataset,
    create_model,
    FEATURES
)

DATA_PATH = "data/student_dataset.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "career_model.joblib")
METADATA_PATH = os.path.join(MODEL_DIR, "model_metadata.json")


def train():

    print("\n========== PATHORA AI ==========")
    print("Starting Model Training...\n")

    X, y = load_dataset(DATA_PATH)

    print("Dataset Shape:", X.shape)
    print("\nCareer Distribution:")
    print(y.value_counts())

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    model = create_model()

    print("\nTraining Decision Tree Model...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("\n========== MODEL RESULTS ==========")
    print(f"Accuracy: {accuracy * 100:.2f}%")

    print("\nClassification Report:")
    print(classification_report(
        y_test,
        predictions,
        zero_division=0
    ))

    print("\nConfusion Matrix:")
    print(confusion_matrix(
        y_test,
        predictions,
        labels=model.classes_
    ))

    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    metadata = {
        "model_name": "Decision Tree Classifier",
        "accuracy": round(float(accuracy), 4),
        "features": FEATURES,
        "classes": model.classes_.tolist(),
        "training_records": len(X_train),
        "testing_records": len(X_test)
    }

    with open(METADATA_PATH, "w") as file:
        json.dump(metadata, file, indent=4)

    print("\nModel saved successfully!")
    print("Location:", MODEL_PATH)

    print("\n========== TRAINING COMPLETED ==========")


if __name__ == "__main__":
    train()
