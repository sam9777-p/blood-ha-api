@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    height = data.get("height")  # in cm
    weight = data.get("weight")  # in kg
    gender = data.get("gender")  # "male" or "female"
    age = data.get("age")        # in years
    hemoglobin = data.get("hemoglobin")  # in g/dL

    if not all([height, weight, gender, age, hemoglobin]):
        return jsonify({"error": "Please provide height (cm), weight (kg), gender, age, and hemoglobin."}), 400

    try:
        height_m = float(height) / 100
        weight = float(weight)
        age = int(age)
        hemoglobin = float(hemoglobin)
        gender = gender.lower()

        # Check hemoglobin level
        if (gender == "male" and hemoglobin < 13.0) or (gender == "female" and hemoglobin < 12.5):
            return jsonify({"eligibility": "Not Eligible"}), 200

        # Calculate estimated blood volume using Nadler's formula
        if gender == "male":
            tbv = (0.3669 * height_m ** 3 + 0.03219 * weight + 0.6041) * 1000
        elif gender == "female":
            tbv = (0.3561 * height_m ** 3 + 0.03308 * weight + 0.1833) * 1000
        else:
            return jsonify({"error": "Gender must be 'male' or 'female'."}), 400

        tbv = round(tbv, 2)

        # Eligibility rules
        if age < 18 or age > 65:
            return jsonify({"eligibility": "Not Eligible"}), 200
        elif tbv < 5000:
            return jsonify({"eligibility": "Not Eligible"}), 200
        else:
            return jsonify({"eligibility": "Eligible"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
