import numpy as np
import pandas as pd
import yfinance as yf


def load_real_data(ticker: str = "SPY", period: str = "2y") -> pd.DataFrame:
    data = yf.download(ticker, period=period, auto_adjust=True, progress=False)

    if data.empty:
        raise ValueError(f"No data returned for ticker={ticker}")

    # Normalize possible MultiIndex columns from yfinance.
    if isinstance(data.columns, pd.MultiIndex):
        if ("Close", ticker) in data.columns:
            close = data[("Close", ticker)]
        elif ("Adj Close", ticker) in data.columns:
            close = data[("Adj Close", ticker)]
        else:
            close = data.xs("Close", axis=1, level=0).iloc[:, 0]
    else:
        close = data["Close"] if "Close" in data.columns else data["Adj Close"]

    df = close.rename("price").reset_index()
    # yfinance index is usually Date/Datetime.
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

    df = pd.DataFrame(
        {
            "day": pd.date_range("2025-01-01", periods=n_days, freq="D"),
            "price": prices,
        }
    )
    df["return"] = df["price"].pct_change().fillna(0.0)
    return df


def apply_price_shock(df: pd.DataFrame, shock_pct: float) -> pd.DataFrame:
    shocked = df.copy()
    shocked["price_shocked"] = shocked["price"] * (1 + shock_pct)
    shocked["return_shocked"] = shocked["price_shocked"].pct_change().fillna(0.0)
    return shocked


def summarize_metrics(df: pd.DataFrame, rolling_window: int = 20) -> dict:
    base_pnl = df["price"].iloc[-1] - df["price"].iloc[0]
    shocked_pnl = df["price_shocked"].iloc[-1] - df["price_shocked"].iloc[0]

    base_vol = df["return"].tail(rolling_window).std()
    shocked_vol = df["return_shocked"].tail(rolling_window).std()

    return {
        "base_pnl": float(base_pnl),
        "shocked_pnl": float(shocked_pnl),
        "pnl_change": float(shocked_pnl - base_pnl),
        "base_volatility": float(base_vol),
        "shocked_volatility": float(shocked_vol),
        "volatility_change": float(shocked_vol - base_vol),
    }
