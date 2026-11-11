from enum import StrEnum


class DatasetType(StrEnum):
    RENEWABLE = "renewable"
    STATE_ESTIMATION = "state_estimation"


class ExperimentType(StrEnum):
    FORECASTING = "forecasting"
    STATE_ESTIMATION = "state_estimation"


class ExperimentStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
