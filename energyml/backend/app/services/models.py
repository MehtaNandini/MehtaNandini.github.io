from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.entities import ExperimentRecord, ModelRecord
from app.models.enums import ExperimentStatus


class ModelService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[ModelRecord]:
        return list(
            self.session.scalars(
                select(ModelRecord).order_by(ModelRecord.created_at.desc())
            )
        )

    def get(self, model_id: str) -> ModelRecord:
        model = self.session.get(ModelRecord, model_id)
        if model is None:
            raise LookupError("model not found")
        return model

    def activate(self, model_id: str) -> ModelRecord:
        model = self.get(model_id)
        experiment = self.session.get(ExperimentRecord, model.experiment_id)
        if experiment is None or experiment.status != ExperimentStatus.COMPLETED.value:
            raise ValueError(
                "only a model from a completed experiment can be activated"
            )
        self.session.execute(
            update(ModelRecord)
            .where(ModelRecord.task_type == model.task_type)
            .values(active=False)
        )
        model.active = True
        self.session.commit()
        self.session.refresh(model)
        return model

    def resolve_for_inference(
        self, task_type: str, model_id: str | None
    ) -> ModelRecord:
        if model_id is not None:
            explicit_model = self.get(model_id)
            if explicit_model.task_type != task_type:
                raise ValueError(f"model does not support {task_type}")
            return explicit_model
        model = self.session.scalar(
            select(ModelRecord).where(
                ModelRecord.task_type == task_type, ModelRecord.active.is_(True)
            )
        )
        if model is None:
            raise LookupError(f"no active {task_type} model")
        return model
