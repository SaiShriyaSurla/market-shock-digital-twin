
# market-shock-digital-twin

A simple **market shock digital twin** that simulates stress scenarios on market price data and compares risk/performance metrics before and after shock.

## Project Goal

Build a lightweight sandbox to answer:

- What happens to PnL when a market shock is applied?
- How do risk metrics (like volatility) change under shock scenarios?

This project is for **scenario testing**, not price prediction.

## MVP (Current)

- Loads real market data (`SPY`) using `yfinance`
- Falls back to synthetic data if download fails
- Applies a baseline shock scenario (`-5%`)
- Computes and saves:
  - Baseline PnL
  - Shocked PnL
  - PnL change
  - Baseline volatility
  - Shocked volatility
  - Volatility change
- Exports results to:
  - `output/simulation_results.csv`
  - `output/metrics.json`

## Project Structure

```text
market-twin/
├── src/
│   ├── main.py
│   ├── simulator.py
│   └── config.py
├── output/
├── requirements.txt
├── .gitignore
└── README.md

## Key Findings 

- Tested four point-shock scenarios on SPY: `-2%`, `-5%`, `-10%`, `-20%`.
- PnL impact scaled roughly linearly with shock size:
  - `-2%`: `pnl_change = -13.50`
  - `-5%`: `pnl_change = -33.74`
  - `-10%`: `pnl_change = -67.49`
  - `-20%`: `pnl_change = -134.98`
- `volatility_change` is effectively `0` in all cases (values around `e-17` are numerical noise).
- Max drawdown worsened materially only in the `-20%` case (`drawdown_change = -0.0543`), meaning this shock pushed the path into a deeper trough than baseline.
- Conclusion: the current model clearly captures stress impact on price level and PnL, but has limited sensitivity in volatility due to the current shock construction.

![Price Comparison](output/price_comparison.png)