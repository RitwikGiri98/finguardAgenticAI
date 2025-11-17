# src/utils/metrics.py
def compute_metrics(report: dict) -> dict:
    s = report.get("summary", {})
    plan = report.get("plan", {})
    flags = s.get("flags", [])

    income = float(s.get("income", 0))
    total = float(s.get("total_expenses", 0))
    cats = int(s.get("categories_found", 0))
    savings_rate = float(s.get("savings_rate", 0))
    risk = float(s.get("risk_score", 0))
    runtime = float(s.get("runtime_seconds", 0))

    # Proxies for rubric:
    ux_score = max(0.0, 1.0 - risk)  # lower risk => clearer guidance => higher UX proxy
    robustness = 1.0
    if "Subscriptions exceed" in " ".join(flags): robustness -= 0.05
    if "Dining spend" in " ".join(flags): robustness -= 0.05
    robustness = max(0.0, robustness)

    return {
        "income": income,
        "total_expenses": total,
        "categories_found": cats,
        "savings_rate": savings_rate,
        "risk_score": risk,
        "runtime_seconds": runtime,
        "ux_proxy": round(ux_score, 3),
        "robustness_proxy": round(robustness, 3),
        "num_flags": len(flags),
    }
