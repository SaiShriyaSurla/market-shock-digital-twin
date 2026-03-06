from dataclasses import dataclass, field


@dataclass(frozen=True)
class SimulationConfig:
    ticker: str = "SPY"
    period: str = "2y"
    rolling_window: int = 20
    shock_scenarios: list[float] = field(default_factory=lambda: [-0.02, -0.05, -0.10, -0.20])
    shock_day_frac: float = 0.6  # shock at 60% of timeline
