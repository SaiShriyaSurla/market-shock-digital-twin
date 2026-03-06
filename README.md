
# market-shock-digital-twin

A simple **market shock digital twin** that simulates stress scenarios on market price data and compares risk/performance metrics before and after shock.

## Project Goal

Build a lightweight sandbox to answer:

- What happens to PnL when a market shock is applied?
- How do risk metrics (like volatility) change under shock scenarios?

This project is for **scenario testing**, not price prediction.

## Day 1 MVP (Current)

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
