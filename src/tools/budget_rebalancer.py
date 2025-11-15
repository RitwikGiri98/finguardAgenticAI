from typing import Dict, Tuple

def smart_budget_rebalance(current_alloc: Dict[str, float], income: float, target_savings_pct: float=0.2
                           ) -> Tuple[Dict[str,float], Dict[str,float]]:
  fixed = {'rent','utilities','insurance'}
  protected = {k:v for k,v in current_alloc.items() if k.lower() in fixed}
  discretionary = {k:v for k,v in current_alloc.items() if k.lower() not in fixed}
  target_savings = max(income*target_savings_pct, 0.0)
  remaining = max(income - target_savings - sum(protected.values()), 0.0)
  total_disc = sum(discretionary.values()) or 1.0
  target_disc = {k: remaining*(v/total_disc) for k,v in discretionary.items()}
  target = {**protected, **target_disc, 'savings': target_savings}
  deltas = {k: target.get(k,0)-current_alloc.get(k,0) for k in set(target)|set(current_alloc)}
  return target, deltas
