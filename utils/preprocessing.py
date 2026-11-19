
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

FEATURES = [
    "math_marks",
    "programming_marks",
    "communication",
    "logical_reasoning",
    "interest_coding",
    "interest_management"
]

TARGET = "field"


def load_dataset(path):
    df = pd.read_csv(path)

    required_columns = FEATURES + [TARGET]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns in dataset: {missing_columns}"
        )

    df = df[required_columns].copy()

    df = df.dropna(subset=[TARGET])

    X = df[FEATURES]
    y = df[TARGET].astype(str).str.strip()

    return X, y


def create_model():
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", DecisionTreeClassifier(
            criterion="gini",
            max_depth=6,
            min_samples_split=10,
            min_samples_leaf=5,
            class_weight="balanced",
            random_state=42
        ))
    ])

    return model
