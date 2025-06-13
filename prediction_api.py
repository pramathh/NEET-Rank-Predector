from flask import Flask, request, jsonify
import pandas as pd
from scipy.interpolate import interp1d

app = Flask(__name__)

# Load dataset
excel_file = "NEET_Expanded_Data final.xlsx"  # Ensure this file exists in the same directory
df = pd.read_excel(excel_file)

# Interpolation functions
rank_interp = interp1d(df["Marks"], df["Rank"], kind='linear', fill_value='extrapolate')
percentile_interp = interp1d(df["Marks"], df["Percentile"], kind='linear', fill_value='extrapolate')

@app.route("/predict", methods=["GET"])
def predict():
    try:
        # Get marks from query parameter
        marks = request.args.get("marks", type=int)

        if marks is None:
            return jsonify({"error": "Please provide 'marks' in the query parameters"}), 400

        # Predict rank and percentile
        predicted_rank = int(rank_interp(marks))
        predicted_percentile = round(float(percentile_interp(marks)), 6)

        return jsonify({
            "marks": marks,
            "predicted_rank": predicted_rank,
            "predicted_percentile": predicted_percentile
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
