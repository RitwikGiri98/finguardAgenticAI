# FinGuardAI – Agentic Financial Wellness System
<p >
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square" />
  <img src="https://img.shields.io/badge/Framework-Agentic%20AI-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Category-Financial%20AI-purple?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" />
</p>

A multi-agent AI system for budgeting, risk scoring, and financial planning.

## 🔍 Overview

FinGuardAI is an advanced agentic AI system designed to analyze financial behavior, detect overspending risk, rebalance user budgets, and produce actionable financial recommendations.

Built with a structured **Controller → Agents → Tools → Memory → API** architecture, the system demonstrates:

✔ Multi-agent orchestration  
✔ Custom financial optimization tool  
✔ Intelligent risk scoring  
✔ Automated budgeting insights  
✔ Visualizations and API endpoints  
✔ Full evaluation suite with metrics  

This project is part of the **Building Agentic Systems** course at Northeastern University, and it is designed to be a portfolio-quality showcase of agentic system engineering.

## 🧱 Architecture


[HighLevelDiagram.png]

<p align="center">
  <em>(Controller → Agents → Tools → Memory → API → Evaluation)</em>
</p>

## 📂 Project Structure

```
finGuardAI/
│
├── data/                   # Input financial profiles
├── outputs/                # Generated charts + reports
│
├── src/
│   ├── api.py              # Flask REST API
│   ├── main.py             # CLI execution
│   │
│   ├── agents/             # Multi-agent system
│   │   ├── agents.py       # Controller + specialized agents
│   │
│   ├── tools/              # Built-in + custom tools
│   │   ├── categorizer.py
│   │   ├── plots.py
│   │   ├── budget_rebalancer.py    # CUSTOM TOOL
│   │
│   ├── utils/              # Utility modules
│   │   ├── cache.py
│   │   ├── formatter.py
│   │   ├── metrics.py
│   │
│   ├── eval.py             # Evaluation Suite
│
├── requirements.txt
└── README.md
```

## 🤖 System Components

### 🧩 1. Controller Agent

The brain of the system:

- Task routing
- Fallback & error handling
- Sequential orchestration
- Runtime logging
- Cache-aware execution

### 🧠 2. Specialized Agents

**ExpenseAnalyzer Agent**
- Cleans transactions
- Categorizes merchants
- Computes monthly spending distribution

**RiskProfiler Agent**
- Evaluates financial risk
- Compares spend vs benchmarks (50/30/20 rule)
- Generates benchmark flags

**PlanDesigner Agent**
- Uses SmartBudgetRebalancer to rebalance user budgets
- Generates deltas and recommendations
- Formats outputs into Markdown + JSON

### 🛠️ 3. Tools Used

- **Data Processor (Pandas)** – cleaning & transformation
- **Benchmark Lookup Tool** – category caps, rules
- **Formatter Tool** – Markdown/JSON report builder
- **Visualization Tool (Matplotlib)** – charts
- **Custom Tool: SmartBudgetRebalancer** (core of the system)

### 🧨 Custom Tool: SmartBudgetRebalancer

A custom-built optimization module that:

- Ensures ≥20% savings
- Reduces discretionary categories (shopping, dining)
- Protects essential categories (rent, utilities)
- Computes target allocation + deltas
- Supports fallback logic for missing categories

This tool is the **heart** of the "intelligent planning" component.

## 🔥 Key Features

✔ Multi-agent orchestration  
✔ Full API for interactive use  
✔ Multiple visualization outputs  
✔ Stress-tested on various spending profiles  
✔ Memory cache for accelerated performance  
✔ Complete evaluation suite  
✔ Clean JSON/Markdown pipeline  

## ▶️ Running FinGuardAI

### 1. CLI Execution

```bash
python src/main.py
```

Generates:
- `report.json`
- `report.md`
- `*.png` charts

### 2. Start the API

```bash
python -m src.api
```

Available Endpoints:
- `GET /health`
- `GET /demo/<profile>`
- `POST /analyze`

Sample:

```bash
curl -X POST http://127.0.0.1:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"income": 4500, "path": "data/moderate.csv"}'
```

## 📊 Example Outputs

[Insert example PNG chart: Spending by Category]

[Insert example PNG chart: Before vs After Budget]

## 🧪 Evaluation Suite

Run:

```bash
python -m src.eval
```

The suite evaluates:

| Test Case | What It Tests |
|-----------|---------------|
| Light | baseline detection |
| Moderate | overspend risk |
| Heavy | extreme imbalance |
| Corner Dining | stress test |
| Repeat (Cache) | runtime improvement |

Generates `evaluation_results.csv`.

## 📈 Key Findings

- Sub-0.4s runtime on all profiles
- Cache improves speed by ~90%
- Accurate risk scoring
- Robust behavior under extreme conditions
- Clean agent orchestration

## ⚠️ Limitations

- Heuristic merchant categorization
- Static benchmarks (50/30/20 rule)
- No multi-month forecasting
- Deterministic risk scoring
- No LLM-based reasoning (yet)

## 🚀 Future Improvements

- Train a merchant classifier model
- Personalized financial targets
- Trend-based analysis
- LLM natural-language advisor
- Reinforcement learning risk refinement
- Live financial API integration

## 🧑‍💻 Author

**Ritwik Giri**  
Master's in Information Systems  
Northeastern University – Boston  

## 📜 License

MIT License

---

⭐ **If you like this project, consider giving it a star!** 🌟
  Made with ❤️, Python, and Agentic AI.
