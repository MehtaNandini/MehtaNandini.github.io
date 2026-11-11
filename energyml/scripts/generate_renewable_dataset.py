import argparse
import json

from _common import services

from app.schemas.datasets import RenewableDatasetCreate


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and register renewable energy data")
    parser.add_argument("--days", type=int, default=365)
    parser.add_argument("--seed", type=int, default=42)
    arguments = parser.parse_args()
    session, datasets, _ = services()
    try:
        record = datasets.generate_renewable(
            RenewableDatasetCreate(number_of_days=arguments.days, random_seed=arguments.seed)
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
