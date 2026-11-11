from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class RenewableDatasetConfig:
    start_date: str = "2025-01-01"
    number_of_days: int = 365
    solar_capacity_mw: float = 60.0
    wind_capacity_mw: float = 40.0
    noise_level: float = 0.04
    random_seed: int = 42

    def as_dict(self) -> dict[str, str | int | float]:
        return asdict(self)


def _ar1_process(
    rng: np.random.Generator, size: int, persistence: float, innovation_std: float
) -> np.ndarray:
    result = np.zeros(size, dtype=float)
    innovations = rng.normal(0.0, innovation_std, size)
    for index in range(1, size):
        result[index] = persistence * result[index - 1] + innovations[index]
    return result


def generate_renewable_dataset(config: RenewableDatasetConfig) -> pd.DataFrame:
    """Generate hourly weather and physically related renewable production.

    The equations are simplified research signals rather than operational forecasts. All
    randomness comes from a local NumPy Generator, making the output deterministic.
    """

    if config.number_of_days < 2:
        raise ValueError("number_of_days must be at least 2")
    if config.solar_capacity_mw <= 0 or config.wind_capacity_mw <= 0:
        raise ValueError("generation capacities must be positive")
    if not 0 <= config.noise_level <= 0.5:
        raise ValueError("noise_level must be between 0 and 0.5")

    rng = np.random.default_rng(config.random_seed)
    periods = config.number_of_days * 24
    timestamps = pd.date_range(config.start_date, periods=periods, freq="h")
    hour = timestamps.hour.to_numpy()
    day_of_year = timestamps.dayofyear.to_numpy()

    seasonal_sun = np.clip(
        0.72 + 0.28 * np.sin(2 * np.pi * (day_of_year - 80) / 365.25), 0, 1
    )
    daylight = np.clip(np.sin(np.pi * (hour - 6) / 12), 0, None)
    weather_state = _ar1_process(rng, periods, persistence=0.92, innovation_std=0.12)
    cloud_cover = np.clip(50 + 25 * weather_state + rng.normal(0, 8, periods), 0, 100)
    clear_sky_irradiance = 1000 * seasonal_sun * daylight
    solar_irradiance = np.clip(
        clear_sky_irradiance * (1 - 0.0072 * cloud_cover) + rng.normal(0, 18, periods),
        0,
        None,
    )

    seasonal_temperature = 12 + 10 * np.sin(2 * np.pi * (day_of_year - 172) / 365.25)
    daily_temperature = 4.5 * np.sin(2 * np.pi * (hour - 8) / 24)
    temperature = (
        seasonal_temperature
        + daily_temperature
        + 0.8 * weather_state
        + rng.normal(0, 1.2, periods)
    )

    wind_state = _ar1_process(rng, periods, persistence=0.88, innovation_std=0.45)
    wind_speed = np.clip(
        6.5 + 1.2 * np.sin(2 * np.pi * day_of_year / 14) + wind_state, 0.1, 25
    )
    humidity = np.clip(
        72 - 0.75 * temperature + 0.18 * cloud_cover + rng.normal(0, 4, periods),
        20,
        100,
    )

    solar_efficiency = np.clip(1 - 0.004 * np.maximum(temperature - 25, 0), 0.75, 1.05)
    solar_power = (
        config.solar_capacity_mw
        * np.clip(solar_irradiance / 1000, 0, 1)
        * solar_efficiency
    )
    cut_in, rated, cut_out = 3.0, 12.0, 25.0
    wind_fraction = np.where(
        wind_speed < cut_in,
        0,
        np.where(
            wind_speed < rated,
            ((wind_speed - cut_in) / (rated - cut_in)) ** 3,
            np.where(wind_speed <= cut_out, 1, 0),
        ),
    )
    wind_power = config.wind_capacity_mw * wind_fraction
    capacity = config.solar_capacity_mw + config.wind_capacity_mw
    production_noise = rng.normal(0, config.noise_level * capacity, periods)
    generation = np.clip(solar_power + wind_power + production_noise, 0, capacity)

    return pd.DataFrame(
        {
            "timestamp": timestamps,
            "hour": hour,
            "day_of_week": timestamps.dayofweek.to_numpy(),
            "month": timestamps.month.to_numpy(),
            "day_of_year": day_of_year,
            "solar_irradiance": solar_irradiance,
            "temperature_c": temperature,
            "wind_speed_mps": wind_speed,
            "humidity_percent": humidity,
            "cloud_cover_percent": cloud_cover,
            "renewable_generation_mw": generation,
        }
    )
