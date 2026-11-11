import argparse
import json

from _common import services

from app.experiments.forecasting import ForecastingExperimentRunner
from app.schemas.experiments import ForecastExperimentCreate


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a registered renewable forecasting experiment"
    )
    parser.add_argument("dataset_id")
    parser.add_argument("--seed", type=int, default=42)
    arguments = parser.parse_args()
    session, datasets, artifacts = services()
    try:
        experiment, model = ForecastingExperimentRunner(
            session, datasets, artifacts
        ).run(
            ForecastExperimentCreate(
                dataset_id=arguments.dataset_id, random_seed=arguments.seed
            )
        )
        print(
            json.dumps(
                {
                    "experiment_id": experiment.id,
                    "model_id": model.id,
                    "metrics": experiment.metrics_json,
                },
                indent=2,
            )
        )
    finally:
        session.close()


if __name__ == "__main__":
    main()
