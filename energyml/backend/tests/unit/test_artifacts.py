from pathlib import Path

import numpy as np
import pytest
from sklearn.dummy import DummyRegressor

from app.services.artifacts import ArtifactManager, ArtifactSecurityError


def test_artifact_model_round_trip_and_hash_validation(tmp_path: Path) -> None:
    manager = ArtifactManager(tmp_path / "artifacts")
    directory = manager.experiment_dir("forecasting", "abc-123")
    model = DummyRegressor(strategy="mean").fit(np.array([[1], [2]]), np.array([2, 4]))
    path, digest = manager.save_model(directory, model)
    loaded = manager.load_model(str(path), digest)
    assert loaded.predict([[3]])[0] == 3
    path.write_bytes(path.read_bytes() + b"corrupt")
    with pytest.raises(ValueError, match="hash mismatch"):
        manager.load_model(str(path), digest)


def test_artifact_manager_blocks_traversal(tmp_path: Path) -> None:
    manager = ArtifactManager(tmp_path / "artifacts")
    with pytest.raises(ArtifactSecurityError):
        manager.experiment_dir("forecasting", "../../escape")
