import os, pandas as pd, matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")  # headless backend for macOS / servers


def spending_by_category(df: pd.DataFrame, out_path: str):
  os.makedirs(os.path.dirname(out_path), exist_ok=True)
  spend = df[df['amount']<0].copy()
  spend['abs'] = spend['amount'].abs()
  agg = spend.groupby('category')['abs'].sum().sort_values(ascending=False)
  plt.figure()
  agg.plot(kind='bar')
  plt.title('Spending by Category'); plt.ylabel('Total'); plt.tight_layout()
  plt.savefig(out_path); plt.close()

def before_after_bar(current: dict, target: dict, out_path: str):
  import numpy as np
  labels = sorted(set(current)|set(target))
  cur = [current.get(k,0) for k in labels]
  tgt = [target.get(k,0) for k in labels]
  x = np.arange(len(labels)); w=0.35
  plt.figure()
  plt.bar(x-w/2, cur, w, label='Current')
  plt.bar(x+w/2, tgt, w, label='Target')
  plt.xticks(x, labels, rotation=45, ha='right'); plt.legend(); plt.tight_layout()
  os.makedirs(os.path.dirname(out_path), exist_ok=True)
  plt.savefig(out_path); plt.close()
