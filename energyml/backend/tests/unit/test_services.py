import shutil
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.experiments.forecasting import ForecastingExperimentRunner
from app.models.entities import ExperimentRecord
from app.models.enums import ExperimentStatus
from app.schemas.datasets import RenewableDatasetCreate
from app.schemas.experiments import ForecastExperimentCreate, ForecastModelConfig
from app.services.artifacts import ArtifactManager
from app.services.datasets import DatasetInUseError, DatasetService
from app.services.models import ModelService


def test_registry_activation_and_referenced_dataset_protection(
    session: Session, tmp_path: Path
) -> None:
    datasets = DatasetService(session, tmp_path / "datasets")
    artifacts = ArtifactManager(tmp_path / "artifacts")
    dataset = datasets.generate_renewable(RenewableDatasetCreate(number_of_days=35, random_seed=42))
    experiment, model = ForecastingExperimentRunner(session, datasets, artifacts).run(
        ForecastExperimentCreate(
            dataset_id=dataset.id,
            model=ForecastModelConfig(max_iter=20, max_depth=4, min_samples_leaf=5),
        )
    )
    assert experiment.status == ExperimentStatus.COMPLETED.value
    activated = ModelService(session).activate(model.id)
    assert activated.active
    with pytest.raises(DatasetInUseError):
        datasets.delete(dataset.id)


def test_failed_training_updates_experiment_status(
    session: Session, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    datasets = DatasetService(session, tmp_path / "datasets")
    dataset = datasets.generate_renewable(RenewableDatasetCreate(number_of_days=30))
    runner = ForecastingExperimentRunner(session, datasets, ArtifactManager(tmp_path / "artifacts"))

    def fail(*args: object, **kwargs: object) -> None:
        raise RuntimeError("intentional training failure")

    monkeypatch.setattr("app.experiments.forecasting.train_forecasting_pipeline", fail)
    with pytest.raises(RuntimeError, match="intentional"):
        runner.run(ForecastExperimentCreate(dataset_id=dataset.id))
    experiments = list(session.scalars(select(ExperimentRecord)))
    assert experiments[-1].status == ExperimentStatus.FAILED.value
    assert experiments[-1].error_message is not None
    assert "intentional training failure" in experiments[-1].error_message


def test_registered_dataset_remains_loadable_after_project_is_moved(
    session: Session, tmp_path: Path
) -> None:
    original_root = tmp_path / "original" / "datasets"
    datasets = DatasetService(session, original_root)
    record = datasets.generate_renewable(RenewableDatasetCreate(number_of_days=5, random_seed=42))
    original_path = Path(record.file_path)
    relocated_root = tmp_path / "relocated" / "datasets"
    relocated_path = relocated_root / record.dataset_type / original_path.name
    relocated_path.parent.mkdir(parents=True)
    shutil.copy2(original_path, relocated_path)

    relocated = DatasetService(session, relocated_root)
    frame = relocated.load_frame(record)

    assert len(frame) == 5 * 24
    assert "renewable_generation_mw" in frame
