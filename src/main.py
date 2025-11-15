import os, json, pandas as pd
from tasks.categorize import ensure_category
from utils.plots import spending_by_category, before_after_bar
from tools.budget_rebalancer import smart_budget_rebalance

def analyze(csv_path: str, monthly_income: float, out_dir: str="outputs"):
  os.makedirs(out_dir, exist_ok=True)
  df = pd.read_csv(csv_path, parse_dates=['date'])
  df = ensure_category(df)

  # CURRENT monthly allocation (positive per category)
  spend = df[df['amount']<0].copy()
  spend['abs'] = spend['amount'].abs()
  current_alloc = spend.groupby('category')['abs'].sum().to_dict()

  # Simple “risk” proxy for Day-1
  total_exp = spend['abs'].sum()
  income = monthly_income
  savings_rate = max((income - total_exp)/income, 0.0) if income>0 else 0.0
  discretionary = sum(v for k,v in current_alloc.items() if k not in ['rent','utilities','insurance','healthcare','taxes'])
  discretionary_ratio = (discretionary/total_exp) if total_exp>0 else 0.0
  risk_score = round(0.5*(1-savings_rate) + 0.5*discretionary_ratio, 2)

  # Rebalance proposal
  target, deltas = smart_budget_rebalance(current_alloc, income, target_savings_pct=0.2)

  # Charts
  spending_by_category(df, os.path.join(out_dir, "spend_by_category.png"))
  before_after_bar(current_alloc, target, os.path.join(out_dir, "before_after_budget.png"))

  report = {
    "summary": {"income": income, "total_expenses": round(total_exp,2), "savings_rate": round(savings_rate,2),
                "categories_found": len(current_alloc), "risk_score": risk_score},
    "plan": {"target": {k: round(v,2) for k,v in target.items()},
             "deltas": {k: round(v,2) for k,v in deltas.items()}}
  }
  with open(os.path.join(out_dir, "report.json"), "w") as f:
    json.dump(report, f, indent=2)
  print("✅ Analysis complete → outputs/report.json + charts")

if __name__ == "__main__":
  csv = os.environ.get("FIN_GUARD_CSV", "data/moderate.csv")
  analyze(csv, monthly_income=4500.0)
