import os, json, time
from dataclasses import dataclass
from src.tools.budget_rebalancer import smart_budget_rebalance
from src.tools.benchmarks import get_benchmarks
from src.tools.formatter import summary_markdown
from src.utils.plots import spending_by_category, before_after_bar
from src.utils.cache import SimpleCache

@dataclass
class AgentResult:
    name: str
    summary: str
    payload: dict

# ---- Individual Agents ----
class ExpenseAnalyzerAgent:
    def run(self, df):
        df = ensure_category(df)
        monthly_alloc = (df[df["amount"] < 0]
            .assign(abs_amt=lambda d: d["amount"].abs())
            .groupby("category")["abs_amt"].sum()
            .to_dict())
        return AgentResult("ExpenseAnalyzer", "Expenses categorized.", {"monthly_alloc": monthly_alloc})

class RiskProfilerAgent:
    def run(self, df, monthly_income, monthly_alloc):
        total_exp = sum(monthly_alloc.values())
        savings_rate = max((monthly_income - total_exp) / monthly_income, 0)
        discretionary = sum(v for k, v in monthly_alloc.items()
                            if k not in ["rent", "utilities", "insurance", "healthcare"])
        discretionary_ratio = discretionary / total_exp if total_exp else 0
        risk_score = round(0.5*(1-savings_rate) + 0.5*discretionary_ratio, 2)
        return AgentResult("RiskProfiler", "Risk computed.", {"risk_score": risk_score})

class PlanDesignerAgent:
    def run(self, monthly_alloc, monthly_income):
        target, deltas = smart_budget_rebalance(monthly_alloc, monthly_income, 0.2)
        return AgentResult("PlanDesigner", "Plan designed.", {"target": target, "deltas": deltas})

# ---- Controller ----
class ControllerAgent:
    def __init__(self, income, out_dir="outputs"):
        self.income = income
        self.out_dir = out_dir
        os.makedirs(self.out_dir, exist_ok=True)
        self.cache = SimpleCache(cache_dir=os.path.join(self.out_dir, "cache"), ttl_seconds=1800)

    def execute(self, df):
        start = time.time()

        # ---------- CACHE KEY ----------
        key_payload = {
            "income": float(self.income),
            "rows": int(len(df)),
            "sum_amount": float(df["amount"].sum()) if "amount" in df.columns else None,
        }
        cached = self.cache.get(key_payload)
        if cached:
            with open(os.path.join(self.out_dir, "report.json"), "w") as f:
                json.dump(cached, f, indent=2)
            print("✅ Agentic run complete (cache hit).")
            return

        # ---------- RUN AGENTS ----------
        from src.tasks.categorize import ensure_category
        df = ensure_category(df)

        # Expense
        exp = (df[df["amount"] < 0]
               .assign(abs_amt=lambda d: d["amount"].abs())
               .groupby("category")["abs_amt"].sum().to_dict())

        # Risk
        total_exp = sum(exp.values())
        savings_rate = max((self.income - total_exp) / self.income, 0) if self.income > 0 else 0.0
        discretionary = sum(v for k, v in exp.items() if k not in ["rent","utilities","insurance","healthcare","taxes"])
        discretionary_ratio = discretionary / total_exp if total_exp else 0.0
        risk_score = round(0.5*(1-savings_rate) + 0.5*discretionary_ratio, 2)

        # Plan
        target, deltas = smart_budget_rebalance(exp, self.income, 0.20)

        # ---------- BENCHMARK CHECKS ----------
        bm = get_benchmarks()
        flags = []
        subs = exp.get("subscriptions", 0.0)
        dining = exp.get("dining", 0.0)
        if total_exp > 0:
            if subs / total_exp > bm["max_subscription_ratio"]:
                flags.append("Subscriptions exceed recommended share.")
            if dining / total_exp > bm["max_dining_ratio"]:
                flags.append("Dining spend exceeds recommended share.")
        if savings_rate < bm["warning_savings"]:
            flags.append("Savings rate dangerously low; prioritize cuts.")

        # ---------- CHARTS ----------
        spending_by_category(df, os.path.join(self.out_dir, "spend_by_category.png"))
        before_after_bar(exp, target, os.path.join(self.out_dir, "before_after_budget.png"))

        # ---------- REPORT ----------
        runtime = time.time() - start
        report = {
            "summary": {
                "income": float(self.income),
                "total_expenses": round(total_exp, 2),
                "savings_rate": round(savings_rate, 3),
                "categories_found": len(exp),
                "risk_score": risk_score,
                "runtime_seconds": round(runtime, 3),
                "flags": flags
            },
            "plan": {"target": {k: round(v,2) for k,v in target.items()},
                     "deltas": {k: round(v,2) for k,v in deltas.items()}},
        }

        # write JSON + Markdown
        with open(os.path.join(self.out_dir, "report.json"), "w") as f:
            json.dump(report, f, indent=2)
        with open(os.path.join(self.out_dir, "report.md"), "w") as f:
            f.write(summary_markdown(report))

        # cache store
        self.cache.set(key_payload, report)

        print("✅ Agentic run complete.")
