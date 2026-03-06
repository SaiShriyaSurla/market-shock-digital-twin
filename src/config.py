from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationConfig:
    shock_pct: float = -0.05  # -5% price shock
    rolling_window: int = 20
