from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class DatasetRecord(Base):
    __tablename__ = "datasets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    dataset_type: Mapped[str] = mapped_column(String(32), index=True)
    version: Mapped[str] = mapped_column(String(32))
    random_seed: Mapped[int] = mapped_column(Integer)
    generation_config_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    row_count: Mapped[int] = mapped_column(Integer)
    file_path: Mapped[str] = mapped_column(Text)
    file_hash: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    experiments: Mapped[list["ExperimentRecord"]] = relationship(back_populates="dataset")

    __table_args__ = (Index("ix_datasets_type_version", "dataset_type", "version"),)


class ExperimentRecord(Base):
    __tablename__ = "experiments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    experiment_type: Mapped[str] = mapped_column(String(32), index=True)
    dataset_id: Mapped[str] = mapped_column(
        ForeignKey("datasets.id", ondelete="RESTRICT"), index=True
    )
    dataset_version: Mapped[str] = mapped_column(String(32))
    model_type: Mapped[str] = mapped_column(String(80))
    model_parameters_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    feature_config_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    random_seed: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), index=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metrics_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    performance_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    artifact_directory: Mapped[str | None] = mapped_column(Text, nullable=True)
    artifact_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    code_version: Mapped[str | None] = mapped_column(String(80), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    dataset: Mapped[DatasetRecord] = relationship(back_populates="experiments")
    models: Mapped[list["ModelRecord"]] = relationship(back_populates="experiment")


class ModelRecord(Base):
    __tablename__ = "models"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    experiment_id: Mapped[str] = mapped_column(
        ForeignKey("experiments.id", ondelete="CASCADE"), index=True
    )
    task_type: Mapped[str] = mapped_column(String(32), index=True)
    model_name: Mapped[str] = mapped_column(String(120))
    model_type: Mapped[str] = mapped_column(String(80))
    version: Mapped[str] = mapped_column(String(32))
    artifact_path: Mapped[str] = mapped_column(Text)
    artifact_hash: Mapped[str] = mapped_column(String(64))
    metrics_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    feature_names_json: Mapped[list[str]] = mapped_column(JSON)
    target_names_json: Mapped[list[str]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    active: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    experiment: Mapped[ExperimentRecord] = relationship(back_populates="models")
    inference_runs: Mapped[list["InferenceRun"]] = relationship(back_populates="model")

    __table_args__ = (Index("ix_models_task_active", "task_type", "active"),)


class InferenceRun(Base):
    __tablename__ = "inference_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    model_id: Mapped[str] = mapped_column(ForeignKey("models.id", ondelete="RESTRICT"), index=True)
    experiment_id: Mapped[str] = mapped_column(
        ForeignKey("experiments.id", ondelete="RESTRICT"), index=True
    )
    task_type: Mapped[str] = mapped_column(String(32), index=True)
    input_hash: Mapped[str] = mapped_column(String(64))
    prediction_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    execution_time_ms: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    model: Mapped[ModelRecord] = relationship(back_populates="inference_runs")
