import numpy as np
import pandas as pd

from app.datasets.renewable import RenewableDatasetConfig, generate_renewable_dataset
from app.features.forecasting import chronological_split, create_forecasting_features


def test_lags_and_shifted_rolling_windows_do_not_leak() -> None:
    frame = generate_renewable_dataset(RenewableDatasetConfig(number_of_days=3, random_seed=1))
    frame["renewable_generation_mw"] = np.arange(len(frame), dtype=float)
    featured = create_forecasting_features(frame)
    first = featured.iloc[0]
    assert first["renewable_generation_mw"] == 24
    assert first["generation_lag_1"] == 23
    assert first["generation_lag_3"] == 21
    assert first["generation_lag_24"] == 0
    assert first["generation_rolling_mean_3"] == np.mean([21, 22, 23])
    assert first["generation_rolling_mean_24"] == np.mean(np.arange(24))


def test_chronological_split_keeps_order() -> None:
    frame = pd.DataFrame({"value": np.arange(100)})
    split = chronological_split(frame, train_ratio=0.7, validation_ratio=0.15)
    assert split.train["value"].tolist() == list(range(70))
    assert split.validation["value"].tolist() == list(range(70, 85))
    assert split.test["value"].tolist() == list(range(85, 100))
    assert split.train.index.max() < split.validation.index.min() < split.test.index.min()
