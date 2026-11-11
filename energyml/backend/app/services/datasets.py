import json
from collections.abc import Mapping
from pathlib import Path
from uuid import uuid4

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.datasets.renewable import RenewableDatasetConfig, generate_renewable_dataset
from app.datasets.state_estimation import StateDatasetConfig, generate_state_dataset
from app.models.entities import DatasetRecord, ExperimentRecord
from app.schemas.datasets import RenewableDatasetCreate, StateDatasetCreate
from app.utils.hashing import sha256_file, sha256_json


class DatasetInUseError(ValueError):
    pass


class DatasetService:
    def __init__(self, session: Session, root: Path) -> None:
        self.session = session
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def generate_renewable(self, request: RenewableDatasetCreate) -> DatasetRecord:
        config = RenewableDatasetConfig(**request.model_dump(exclude={"name"}))
        return self._store(
            name=request.name,
            dataset_type="renewable",
            version="1.0",
            random_seed=config.random_seed,
            config=config.as_dict(),
            frame=generate_renewable_dataset(config),
        )

    def generate_state(self, request: StateDatasetCreate) -> DatasetRecord:
        config = StateDatasetConfig(**request.model_dump(exclude={"name"}))
        return self._store(
            name=request.name,
            dataset_type="state_estimation",
            version="1.0",
            random_seed=config.random_seed,
            config=config.as_dict(),
            frame=generate_state_dataset(config),
        )

    def list(self) -> list[DatasetRecord]:
        return list(
            self.session.scalars(
                select(DatasetRecord).order_by(DatasetRecord.created_at.desc())
            )
        )

    def get(self, dataset_id: str) -> DatasetRecord:
        record = self.session.get(DatasetRecord, dataset_id)
        if record is None:
            raise LookupError("dataset not found")
        return record

    def load_frame(self, record: DatasetRecord) -> pd.DataFrame:
        path = Path(record.file_path).resolve()
        if self.root not in path.parents or not path.is_file():
            raise FileNotFoundError("registered dataset file is missing or unsafe")
        if sha256_file(path) != record.file_hash:
            raise ValueError("registered dataset hash mismatch")
        return pd.read_csv(
            path,
            parse_dates=["timestamp"] if record.dataset_type == "renewable" else None,
        )

    def delete(self, dataset_id: str) -> None:
        record = self.get(dataset_id)
        referenced = self.session.scalar(
            select(ExperimentRecord.id)
            .where(ExperimentRecord.dataset_id == dataset_id)
            .limit(1)
        )
        if referenced:
            raise DatasetInUseError("dataset is referenced by an experiment")
        path = Path(record.file_path).resolve()
        self.session.delete(record)
        self.session.commit()
        if path.is_file() and self.root in path.parents:
            path.unlink()

    def _store(
        self,
        *,
        name: str,
        dataset_type: str,
        version: str,
        random_seed: int,
        config: Mapping[str, str | int | float],
        frame: pd.DataFrame,
    ) -> DatasetRecord:
        dataset_id = str(uuid4())
        directory = (self.root / dataset_type).resolve()
        if self.root not in directory.parents:
            raise ValueError("invalid dataset storage path")
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{dataset_id}.csv"
        frame.to_csv(path, index=False, date_format="%Y-%m-%dT%H:%M:%S")
        version_hash = sha256_json({"type": dataset_type, "config": config})[:12]
        record = DatasetRecord(
            id=dataset_id,
            name=name,
            dataset_type=dataset_type,
            version=f"{version}+{version_hash}",
            random_seed=random_seed,
            generation_config_json=json.loads(json.dumps(config)),
            row_count=len(frame),
            file_path=str(path),
            file_hash=sha256_file(path),
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record
