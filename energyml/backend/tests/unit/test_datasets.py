import numpy as np
import pandas as pd

from app.datasets.renewable import RenewableDatasetConfig, generate_renewable_dataset
from app.datasets.state_estimation import StateDatasetConfig, generate_state_dataset


def test_renewable_generation_is_reproducible() -> None:
    config = RenewableDatasetConfig(number_of_days=10, random_seed=42)
    pd.testing.assert_frame_equal(
        generate_renewable_dataset(config), generate_renewable_dataset(config)
    )


def test_renewable_different_seed_changes_data() -> None:
    first = generate_renewable_dataset(RenewableDatasetConfig(number_of_days=5, random_seed=42))
    second = generate_renewable_dataset(RenewableDatasetConfig(number_of_days=5, random_seed=43))
    assert not np.allclose(first["renewable_generation_mw"], second["renewable_generation_mw"])


def test_renewable_columns_and_physical_relationships() -> None:
    frame = generate_renewable_dataset(RenewableDatasetConfig(number_of_days=30, random_seed=7))
    expected = {
        "timestamp",
        "hour",
        "day_of_week",
        "month",
        "day_of_year",
        "solar_irradiance",
        "temperature_c",
        "wind_speed_mps",
        "humidity_percent",
        "cloud_cover_percent",
        "renewable_generation_mw",
    }
    assert set(frame.columns) == expected
    assert len(frame) == 30 * 24
    assert frame["renewable_generation_mw"].corr(frame["solar_irradiance"]) > 0.45
    assert frame["renewable_generation_mw"].between(0, 100).all()


def test_state_generation_is_reproducible_and_multi_output() -> None:
    config = StateDatasetConfig(network_size=5, number_of_samples=100, random_seed=42)
    first = generate_state_dataset(config)
    second = generate_state_dataset(config)
    pd.testing.assert_frame_equal(first, second)
    targets = [column for column in first if column.startswith("voltage_magnitude_bus_")]
    assert len(targets) == 5
    assert first[targets].to_numpy().min() >= 0.88
    assert first[targets].to_numpy().max() <= 1.08


def test_state_different_seed_and_noise_change_measurements() -> None:
    first = generate_state_dataset(
        StateDatasetConfig(network_size=3, number_of_samples=100, random_seed=42)
    )
    second = generate_state_dataset(
        StateDatasetConfig(network_size=3, number_of_samples=100, random_seed=43)
    )
    assert not np.allclose(first, second)
    noisy = generate_state_dataset(
        StateDatasetConfig(network_size=3, number_of_samples=100, measurement_noise_std=0.03)
    )
    quiet = generate_state_dataset(
        StateDatasetConfig(network_size=3, number_of_samples=100, measurement_noise_std=0.0)
    )
    assert not np.allclose(noisy["active_power_bus_1"], quiet["active_power_bus_1"])
