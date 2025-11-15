from typing import Dict

def summary_markdown(report: Dict) -> str:
    s = report.get("summary", {})
    plan = report.get("plan", {})
    target = plan.get("target", {})
    deltas = plan.get("deltas", {})

    lines = []
    lines.append(f"# FinGuard Summary")
    lines.append("")
    lines.append(f"- **Income:** ${s.get('income', 0):,.2f}")
    if "total_expenses" in s:
        lines.append(f"- **Total Expenses:** ${s['total_expenses']:,.2f}")
    if "savings_rate" in s:
        lines.append(f"- **Savings Rate:** {s['savings_rate']*100:.1f}%")
    lines.append(f"- **Categories Found:** {s.get('categories_found', 0)}")
    lines.append(f"- **Risk Score (0=low,1=high):** {s.get('risk_score', 0)}")
    if "runtime_seconds" in s:
        lines.append(f"- **Runtime:** {s['runtime_seconds']:.2f}s")
    lines.append("")

    lines.append("## Target Budget (After Rebalance)")
    for k in sorted(target.keys()):
        lines.append(f"- {k}: ${target[k]:,.2f}")

    lines.append("")
    lines.append("## Changes (Deltas)")
    if not deltas:
        lines.append("- No changes proposed.")
    else:
        for k in sorted(deltas.keys()):
            v = deltas[k]
            arrow = "↓" if v < 0 else ("↑" if v > 0 else "•")
            lines.append(f"- {k}: {arrow} {v:+.2f}")

    # simple guidance
    lines.append("")
    lines.append("## Next Steps")
    lines.append("- Move proposed savings to a separate account on payday.")
    lines.append("- Set category alerts where cuts are recommended.")
    lines.append("- Re-run analysis next month and compare trends.")
    return "\n".join(lines)
