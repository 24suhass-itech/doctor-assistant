import pandas as pd
import pickle
import json
from rapidfuzz import process

# --------------------------
# Load model + features
# --------------------------
with open("disease_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("feature_columns.json", "r") as f:
    feature_cols = json.load(f)

# Convert all feature columns to lowercase
feature_cols = [c.lower() for c in feature_cols]


# --------------------------
# Fuzzy Match System
# --------------------------
def fuzzy_match(symptom, choices, threshold=70):
    """
    symptom: spoken symptom text (lowercase)
    choices: list of valid symptom names
    threshold: Match required score (70 = smart mode)

    Returns: matched symptom OR None
    """

    match, score, idx = process.extractOne(symptom, choices)

    if score >= threshold:
        return match  
    return None


# --------------------------
# MAIN DIAGNOSE FUNCTION
# --------------------------
def diagnose(symptom_text):
    # Normalize text
    symptom_text = symptom_text.lower()

    # Step 1: split by comma AND by "and"
    raw_parts = (
        symptom_text.replace(" and ", ",")
                    .replace(".", "")
                    .split(",")
    )

    raw_parts = [p.strip() for p in raw_parts if p.strip()]

    # Step 2: fuzzy match each symptom
    final_symptoms = []

    for s in raw_parts:
        s_clean = s.replace(" ", "_")       # chest pain -> chest_pain
        match = fuzzy_match(s_clean, feature_cols)

        if match:
            final_symptoms.append(match)

    # Remove duplicates
    final_symptoms = list(set(final_symptoms))

    print(final_symptoms)

    # Step 3: One-hot encoding
    row = [1 if col in final_symptoms else 0 for col in feature_cols]
    X = pd.DataFrame([row], columns=feature_cols)

    # Step 4: Predict
    probs = model.predict_proba(X)[0]
    classes = model.classes_

    best = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)[0][0]
    return best
