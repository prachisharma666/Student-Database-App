

from flask import Flask, request, jsonify
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Gaussian Naive Bayes API is Running!"
    
@app.route("/")          # Home page
@app.route("/add", methods=["POST"])
@app.route("/search", methods=["POST"])
@app.route("/train", methods=["POST"])
def train_model():
    try:
        file = request.files["file"]
        target = request.form["target"]

        df = pd.read_csv(file)

        if target not in df.columns:
            return jsonify({"error": "Target column not found"}), 400

        X = df.drop(columns=[target])
        y = df[target]

        model = GaussianNB()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model.fit(X_train, y_train)

        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)

        results = {
            "train_accuracy": accuracy_score(y_train, y_train_pred),
            "test_accuracy": accuracy_score(y_test, y_test_pred),
            "train_confusion_matrix": confusion_matrix(y_train, y_train_pred).tolist(),
            "test_confusion_matrix": confusion_matrix(y_test, y_test_pred).tolist(),
        }

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

    
