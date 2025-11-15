import io, os, json, csv
from flask import Flask, request, jsonify
import pandas as pd
from src.agents.agents import ControllerAgent

app = Flask(__name__)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
def analyze_endpoint():
    """
    Accepts either:
      - {"csv_text": "...", "monthly_income": 4500}
      - {"transactions": [ {...}, {...} ], "monthly_income": 4500}
    """
    payload = request.get_json(force=True, silent=True) or {}
    income = float(payload.get("monthly_income", 4000))

    # case A: CSV text
    if "csv_text" in payload:
        csv_text = payload["csv_text"]
        df = pd.read_csv(io.StringIO(csv_text), parse_dates=["date"])
    # case B: JSON transactions list
    elif "transactions" in payload:
        df = pd.DataFrame(payload["transactions"])
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
    else:
        return jsonify({"status":"error","message":"Provide csv_text or transactions"}), 400

    ControllerAgent(income, out_dir="outputs").execute(df)
    with open(os.path.join("outputs","report.json"), "r") as f:
        report = json.load(f)
    return jsonify({"status":"success","report":report})

@app.get("/demo/<profile>")
def demo_profile(profile):
    path = f"data/{profile}.csv"
    if not os.path.exists(path):
        return jsonify({"status":"error","message":f"demo profile not found: {path}"}), 404
    df = pd.read_csv(path, parse_dates=["date"])
    ControllerAgent(4500, out_dir="outputs").execute(df)
    with open(os.path.join("outputs","report.json"), "r") as f:
        report = json.load(f)
    return jsonify({"status":"success","report":report})

if __name__ == "__main__":
    # stable run on macOS: no debug, no reloader
    app.run(host="127.0.0.1", port=5050, debug=False, use_reloader=False, threaded=False)


