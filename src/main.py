import json
import os

from config import SimulationConfig
from simulator import apply_price_shock, load_or_create_data, load_real_data, summarize_metrics


def main() -> None:
    cfg = SimulationConfig()

    try:
        df = load_real_data("SPY", "2y")
        print("Loaded real SPY data.")
    except Exception as e:
        print(f"Real data fetch failed ({e}), using synthetic data.")
        df = load_or_create_data()

    df = apply_price_shock(df, cfg.shock_pct)
    metrics = summarize_metrics(df, cfg.rolling_window)

    os.makedirs("output", exist_ok=True)
    df.to_csv("output/simulation_results.csv", index=False)
    with open("output/metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("Simulation complete.")
    for k, v in metrics.items():
        print(f"{k}: {v:.6f}" if isinstance(v, float) else f"{k}: {v}")


if __name__ == "__main__":
    main()
