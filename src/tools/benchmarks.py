BENCHMARKS = {
    "rule_50_30_20": {"needs": 0.50, "wants": 0.30, "savings": 0.20},
    "max_subscription_ratio": 0.07,   # <= 7% monthly spend in subscriptions
    "max_dining_ratio": 0.12,         # <= 12% monthly spend in dining
    "healthy_savings_min": 0.20,      # 20%+ of income
    "warning_savings": 0.10           # below 10% is risky
}

def get_benchmarks():
    return BENCHMARKS
