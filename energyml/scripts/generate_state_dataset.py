import argparse
import json

from _common import services

from app.schemas.datasets import StateDatasetCreate


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and register voltage-state data")
    parser.add_argument("--buses", type=int, default=5)
    parser.add_argument("--samples", type=int, default=5000)
    parser.add_argument("--noise", type=float, default=0.005)
    parser.add_argument("--seed", type=int, default=42)
    arguments = parser.parse_args()
    session, datasets, _ = services()
    try:
        record = datasets.generate_state(
            StateDatasetCreate(
                network_size=arguments.buses,
                number_of_samples=arguments.samples,
                measurement_noise_std=arguments.noise,
                random_seed=arguments.seed,
            )
        )
        print(
            json.dumps(
                {
                    "dataset_id": record.id,
                    "rows": record.row_count,
                    "sha256": record.file_hash,
                }
            )
        )
    finally:
        session.close()


if __name__ == "__main__":
    main()
