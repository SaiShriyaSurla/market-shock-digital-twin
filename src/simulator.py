import numpy as np
import pandas as pd
import yfinance as yf


def load_real_data(ticker: str = "SPY", period: str = "2y") -> pd.DataFrame:
    data = yf.download(ticker, period=period, auto_adjust=True, progress=False)
    if data.empty:
        raise ValueError(f"No data returned for ticker={ticker}")

    if isinstance(data.columns, pd.MultiIndex):
        close = data[("Close", ticker)] if ("Close", ticker) in data.columns else data.xs("Close", axis=1, level=0).iloc[:, 0]
    else:
        close = data["Close"] if "Close" in data.columns else data["Adj Close"]

    df = close.rename("price").reset_index()
    date_col = "Date" if "Date" in df.columns else df.columns[0]
    df = df.rename(columns={date_col: "day"})
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"]).sort_values("day").reset_index(drop=True)
    df["return"] = df["price"].pct_change().fillna(0.0)
    return df


def load_or_create_data(n_days: int = 120, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    daily_returns = rng.normal(loc=0.0005, scale=0.01, size=n_days)
    prices = 100 * np.cumprod(1 + daily_returns)
    df = pd.DataFrame({"day": pd.date_range("2025-01-01", periods=n_days, freq="D"), "price": prices})
    df["return"] = df["price"].pct_change().fillna(0.0)
    return df


def apply_point_shock(df: pd.DataFrame, shock_pct: float, shock_day_frac: float = 0.6) -> pd.DataFrame:
    shocked = df.copy()
    idx = max(1, min(len(shocked) - 1, int(len(shocked) * shock_day_frac)))
    factor = 1.0 + shock_pct

    shocked["price_shocked"] = shocked["price"]
    shocked.loc[idx:, "price_shocked"] = shocked.loc[idx:, "price"] * factor
    shocked["return_shocked"] = shocked["price_shocked"].pct_change().fillna(0.0)
    return shocked


def max_drawdown(price_series: pd.Series) -> float:
    running_peak = price_series.cummax()
    drawdown = (price_series / running_peak) - 1.0
    return float(drawdown.min())


def summarize_metrics(df: pd.DataFrame, rolling_window: int = 20) -> dict:
    base_pnl = df["price"].iloc[-1] - df["price"].iloc[0]
    shocked_pnl = df["price_shocked"].iloc[-1] - df["price_shocked"].iloc[0]

    base_vol = float(df["return"].tail(rolling_window).std())
    shocked_vol = float(df["return_shocked"].tail(rolling_window).std())

    base_dd = max_drawdown(df["price"])
    shocked_dd = max_drawdown(df["price_shocked"])

    return {
        "base_pnl": float(base_pnl),
        "shocked_pnl": float(shocked_pnl),
        "pnl_change": float(shocked_pnl - base_pnl),
        "base_volatility": base_vol,
        "shocked_volatility": shocked_vol,
        "volatility_change": float(shocked_vol - base_vol),
        "base_max_drawdown": base_dd,
        "shocked_max_drawdown": shocked_dd,
        "drawdown_change": float(shocked_dd - base_dd),
    }
