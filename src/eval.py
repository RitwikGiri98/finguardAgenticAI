# src/eval.py
import os, json, pandas as pd, time
from pathlib import Path
from src.agents.agents import ControllerAgent
from src.utils.metrics import compute_metrics

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True, parents=True)

CASES = [
    ("light", DATA/"light.csv", 3500),
    ("moderate", DATA/"moderate.csv", 4500),
    ("heavy", DATA/"heavy.csv", 5200),
    # corner: all dining maxed, to test flags + robustness
    ("corner_dining", None, 4500),
]

def _corner_df():
    import pandas as pd
    rows = []
    for i in range(30):
        rows.append({"txn_id":i+1,"date":"2025-11-{:02d}".format(min(i+1,28)),
                     "account":"Credit","merchant":"Fancy Place","description":"dining purchase",
                     "amount":-100.0,"category":"dining","subcategory":"general","channel":"card","is_recurring":0,"is_income":0})
    rows.append({"txn_id":999,"date":"2025-11-01","account":"Checking","merchant":"ACME Corp","description":"Paycheck",
                 "amount":2250.0,"category":"income","subcategory":"salary","channel":"ach","is_recurring":1,"is_income":1})
    rows.append({"txn_id":1000,"date":"2025-11-15","account":"Checking","merchant":"ACME Corp","description":"Paycheck",
                 "amount":2250.0,"category":"income","subcategory":"salary","channel":"ach","is_recurring":1,"is_income":1})
    return pd.DataFrame(rows)

def run_case(name, path, income):
    print(f"[eval] {name} ...")
    if path and path.exists():
        df = pd.read_csv(path, parse_dates=["date"])
    else:
        df = _corner_df()

    t0 = time.time()
    ControllerAgent(income, out_dir=str(OUT)).execute(df)
    with open(OUT/"report.json","r") as f:
        report = json.load(f)
    m = compute_metrics(report)
    m.update({"case": name, "elapsed": round(time.time()-t0, 3)})
    return m

if __name__ == "__main__":
    results = [run_case(n,p,i) for (n,p,i) in CASES]
    df = pd.DataFrame(results)
    df.to_csv(OUT/"evaluation_results.csv", index=False)
    print(df)
    print(f"[eval] wrote {OUT/'evaluation_results.csv'}")
# cache speed test: repeat moderate
rep1 = run_case("moderate_repeat_1", DATA/"moderate.csv", 4500)
rep2 = run_case("moderate_repeat_2", DATA/"moderate.csv", 4500)
results += [rep1, rep2]
