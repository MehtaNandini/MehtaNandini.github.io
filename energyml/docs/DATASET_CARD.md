# EnergyML synthetic dataset card

## Purpose

These datasets support reproducible software and machine-learning research demonstrations for
renewable forecasting and voltage state estimation. They contain no personal, operational or
proprietary data.

## Renewable generation

Hourly solar, temperature, wind, humidity and cloud signals drive capacity-limited synthetic
solar/wind production. The target includes controlled noise but is causally related to the
features. The default span is one year. This data does not reproduce a named location or plant.

## Distribution-network states

Independent operating samples use load/generation factors, bus diversity and simplified radial
line drops to create voltage targets. Measurement features receive Gaussian noise. This model
is useful for testing multi-output workflows but is not an AC power-flow simulator and must not
be used for grid operation or safety decisions.

## Reproducibility

Generation configuration, NumPy seed, version, row count, file path and SHA-256 hash are stored
in the dataset registry. Equal seed/configuration yields equal values; different seeds are
tested to diverge.

## Known limitations

Weather variables are stylised rather than calibrated to a geography. Network topology is
radial and fixed within a dataset. No equipment switching, harmonics, outages, cyber events or
sensor dropout is simulated. Real-world evaluation is required before any applied use.
