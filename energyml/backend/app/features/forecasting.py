from dataclasses import dataclass

import pandas as pd

TARGET = "renewable_generation_mw"
FORECAST_FEATURES = [
    "hour",
    "day_of_week",
    "month",
    "day_of_year",
    "solar_irradiance",
    "temperature_c",
    "wind_speed_mps",
    "humidity_percent",
    "cloud_cover_percent",
    "generation_lag_1",
    "generation_lag_3",
    "generation_lag_6",
    "generation_lag_24",
    "generation_rolling_mean_3",
    "generation_rolling_mean_6",
    "generation_rolling_mean_24",
]


@dataclass(frozen=True)
class ChronologicalSplit:
    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame


def create_forecasting_features(frame: pd.DataFrame) -> pd.DataFrame:
    required = {TARGET, *FORECAST_FEATURES[:9]}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"missing renewable columns: {sorted(missing)}")
    featured = frame.copy()
    for lag in (1, 3, 6, 24):
        featured[f"generation_lag_{lag}"] = featured[TARGET].shift(lag)
    past_generation = featured[TARGET].shift(1)
    for window in (3, 6, 24):
        featured[f"generation_rolling_mean_{window}"] = past_generation.rolling(
            window=window, min_periods=window
        ).mean()
    return featured.dropna(subset=FORECAST_FEATURES).reset_index(drop=True)


def chronological_split(
    frame: pd.DataFrame, train_ratio: float = 0.7, validation_ratio: float = 0.15
) -> ChronologicalSplit:
    if not 0 < train_ratio < 1 or not 0 <= validation_ratio < 1:
        raise ValueError("split ratios must be within (0, 1)")
    if train_ratio + validation_ratio >= 1:
        raise ValueError(
            "train and validation ratios must leave a non-empty test split"
        )
    train_end = int(len(frame) * train_ratio)
    validation_end = train_end + int(len(frame) * validation_ratio)
    if train_end < 1 or validation_end <= train_end or validation_end >= len(frame):
        raise ValueError("dataset is too small for the requested split")
    return ChronologicalSplit(
        train=frame.iloc[:train_end].copy(),
        validation=frame.iloc[train_end:validation_end].copy(),
        test=frame.iloc[validation_end:].copy(),
    )
