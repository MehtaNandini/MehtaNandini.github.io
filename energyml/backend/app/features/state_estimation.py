def state_feature_target_columns(columns: list[str]) -> tuple[list[str], list[str]]:
    targets = sorted(
        (column for column in columns if column.startswith("voltage_magnitude_bus_")),
        key=lambda name: int(name.rsplit("_", 1)[1]),
    )
    features = [column for column in columns if column not in targets]
    if not targets:
        raise ValueError("state dataset contains no voltage targets")
    return features, targets
