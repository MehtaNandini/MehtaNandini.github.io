from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class StateDatasetConfig:
    network_size: int = 5
    number_of_samples: int = 5_000
    measurement_noise_std: float = 0.005
    random_seed: int = 42

    def as_dict(self) -> dict[str, int | float]:
        return asdict(self)


def generate_state_dataset(config: StateDatasetConfig) -> pd.DataFrame:
    """Generate measurements from a simplified radial distribution-network model.

    Voltage targets follow cumulative linearised resistive/reactive drops. This provides
    mathematically related states and measurements while deliberately not claiming AC power
    flow fidelity. A pandapower generator can later implement the same interface.
    """

    if config.network_size < 2 or config.network_size > 50:
        raise ValueError("network_size must be between 2 and 50")
    if config.number_of_samples < 50:
        raise ValueError("number_of_samples must be at least 50")
    if not 0 <= config.measurement_noise_std <= 0.1:
        raise ValueError("measurement_noise_std must be between 0 and 0.1")

    rng = np.random.default_rng(config.random_seed)
    samples, buses = config.number_of_samples, config.network_size
    load_factor = rng.uniform(0.45, 1.15, samples)
    generation_factor = rng.uniform(0.0, 0.75, samples)
    base_load = np.linspace(0.45, 1.0, buses)
    diversity = rng.lognormal(mean=0.0, sigma=0.12, size=(samples, buses))
    local_generation = rng.beta(2.0, 5.0, size=(samples, buses)) * generation_factor[:, None]
    active_true = load_factor[:, None] * base_load * diversity - 0.55 * local_generation
    reactive_true = 0.28 * np.maximum(active_true, 0) + rng.normal(0, 0.015, (samples, buses))

    resistance = np.linspace(0.004, 0.009, buses)
    reactance = np.linspace(0.003, 0.007, buses)
    downstream_p = np.flip(np.cumsum(np.flip(active_true, axis=1), axis=1), axis=1)
    downstream_q = np.flip(np.cumsum(np.flip(reactive_true, axis=1), axis=1), axis=1)
    segment_drop = resistance * downstream_p + reactance * downstream_q
    voltage = np.clip(1.02 - np.cumsum(segment_drop, axis=1), 0.88, 1.08)
    flows = downstream_p
    currents = np.sqrt(downstream_p**2 + downstream_q**2) / np.maximum(voltage, 0.85)

    noise = config.measurement_noise_std
    active_measured = active_true + rng.normal(0, noise, (samples, buses))
    reactive_measured = reactive_true + rng.normal(0, noise, (samples, buses))
    flow_measured = flows + rng.normal(0, noise * 2, (samples, buses))
    current_measured = currents + rng.normal(0, noise * 2, (samples, buses))

    data: dict[str, np.ndarray] = {
        "load_factor": load_factor,
        "generation_factor": generation_factor,
        "measurement_noise_std": np.full(samples, noise),
    }
    for index in range(buses):
        bus = index + 1
        data[f"active_power_bus_{bus}"] = active_measured[:, index]
        data[f"reactive_power_bus_{bus}"] = reactive_measured[:, index]
        data[f"current_measurement_bus_{bus}"] = current_measured[:, index]
        data[f"power_flow_measurement_bus_{bus}"] = flow_measured[:, index]
        if index % 2 == 0:
            data[f"selected_voltage_measurement_bus_{bus}"] = voltage[:, index] + rng.normal(
                0, noise, samples
            )
        data[f"voltage_magnitude_bus_{bus}"] = voltage[:, index]
    return pd.DataFrame(data)
