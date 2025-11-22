from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import diagnose, fuzzy_match, feature_cols
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)   # Allow React frontend to access backend


@app.route("/diagnose", methods=["POST"])
def diagnose_route():
    data = request.json
    symptoms_text = data.get("symptoms", "")

    # ---- Predict disease ----
    disease = diagnose(symptoms_text)

    # ---- Clean fuzzy-matched symptoms ----
    cleaned = []
    raw = (
        symptoms_text.lower()
        .replace(" and ", ",")
        .replace(".", "")
        .split(",")
    )
    raw = [s.strip().replace(" ", "_") for s in raw if s.strip()]

    for s in raw:
        match = fuzzy_match(s, feature_cols)
        if match:
            cleaned.append(match)

    # ---- Build QR Text ----
    qr_text = f"Symptoms: {', '.join(cleaned)}\nPredicted Disease: {disease}"

    # ---- Generate QR Code ----
    img_buffer = BytesIO()
    img = qrcode.make(qr_text)
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    # Convert QR to base64
    qr_base64 = base64.b64encode(img_buffer.read()).decode("utf-8")

    return jsonify({
        "disease": disease,
        "cleaned": cleaned,
        "qr": qr_base64
    })


if __name__ == "__main__":
    print(" Backend running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000)
