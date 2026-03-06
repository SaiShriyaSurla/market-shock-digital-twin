import json
import os

import matplotlib.pyplot as plt
import pandas as pd

from config import SimulationConfig
from simulator import apply_point_shock, load_or_create_data, load_real_data, summarize_metrics


def main() -> None:
    cfg = SimulationConfig()

    try:
        base_df = load_real_data(cfg.ticker, cfg.period)
        print(f"Loaded real data: {cfg.ticker}")
    except Exception as e:
        print(f"Real data fetch failed ({e}), using synthetic data.")
        base_df = load_or_create_data()

    os.makedirs("output", exist_ok=True)

    scenario_rows = []
    chart_df = None

    for shock in cfg.shock_scenarios:
        shocked_df = apply_point_shock(base_df, shock, cfg.shock_day_frac)
        metrics = summarize_metrics(shocked_df, cfg.rolling_window)

        scenario_name = f"{int(shock * 100)}%"
        scenario_rows.append(
            {
                "scenario": scenario_name,
                "shock_pct": shock,
                "pnl_change": metrics["pnl_change"],
                "volatility_change": metrics["volatility_change"],
                "drawdown_change": metrics["drawdown_change"],
                "base_pnl": metrics["base_pnl"],
                "shocked_pnl": metrics["shocked_pnl"],
            }
        )

        if shock == -0.10:
            chart_df = shocked_df.copy()

    comparison = pd.DataFrame(scenario_rows).sort_values("shock_pct")
    comparison.to_csv("output/scenario_comparison.csv", index=False)

    with open("output/scenario_comparison.json", "w", encoding="utf-8") as f:
        json.dump(comparison.to_dict(orient="records"), f, indent=2)

    if chart_df is not None:
        plt.figure(figsize=(10, 5))
        plt.plot(chart_df["day"], chart_df["price"], label="Base Price")
        plt.plot(chart_df["day"], chart_df["price_shocked"], label="Shocked Price (-10%)")
        plt.title("Base vs Shocked Price Path")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.tight_layout()
        plt.savefig("output/price_comparison.png", dpi=150)
        plt.close()

    print("Day 2 complete. Files generated:")
    print("- output/scenario_comparison.csv")
    print("- output/scenario_comparison.json")
    print("- output/price_comparison.png")
    print(comparison.to_string(index=False))


if __name__ == "__main__":
    main()
