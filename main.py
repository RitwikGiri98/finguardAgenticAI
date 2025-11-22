import os
import pandas as pd
from src.agents.agents import ControllerAgent


def analyze_agentic(csv_path: str, monthly_income: float, out_dir: str = "outputs"):
    """Run the full agentic analysis pipeline."""
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(csv_path, parse_dates=["date"])
    ControllerAgent(monthly_income, out_dir).execute(df)


if __name__ == "__main__":
    analyze_agentic("data/moderate.csv", 4500)
