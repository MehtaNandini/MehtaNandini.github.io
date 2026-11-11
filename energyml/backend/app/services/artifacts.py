import json
from pathlib import Path
from typing import Any

import joblib
from matplotlib.figure import Figure

from app.utils.hashing import sha256_file


class ArtifactSecurityError(ValueError):
    pass


class ArtifactManager:
    """Own all artifact IO and constrain it to one configured root."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def experiment_dir(self, task_type: str, experiment_id: str) -> Path:
        if task_type not in {"forecasting", "state_estimation"}:
            raise ArtifactSecurityError("unsupported artifact task")
        if not experiment_id.replace("-", "").isalnum():
            raise ArtifactSecurityError("invalid experiment identifier")
        path = (self.root / task_type / experiment_id).resolve()
        self._validate(path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def save_model(self, directory: Path, model: Any) -> tuple[Path, str]:
        path = self._child(directory, "model.joblib")
        joblib.dump(model, path, compress=3)
        return path, sha256_file(path)

    def load_model(self, registered_path: str, expected_hash: str) -> Any:
        path = self._registered_file(Path(registered_path))
        if not path.is_file():
            raise FileNotFoundError("registered model artifact is missing")
        if sha256_file(path) != expected_hash:
            raise ValueError("registered model artifact hash mismatch")
        return joblib.load(path)

    def save_json(self, directory: Path, filename: str, payload: Any) -> Path:
        if not filename.endswith(".json"):
            raise ArtifactSecurityError("JSON artifact must use a .json extension")
        path = self._child(directory, filename)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n")
        return path

    def save_figure(self, directory: Path, filename: str, figure: Figure) -> Path:
        if not filename.endswith(".png"):
            raise ArtifactSecurityError("plot artifact must use a .png extension")
        path = self._child(directory, filename)
        figure.savefig(path, dpi=130, bbox_inches="tight")
        return path

    def manifest(self, directory: Path) -> list[dict[str, Any]]:
        directory = self._registered_directory(directory)
        if not directory.is_dir():
            raise FileNotFoundError("registered artifact directory is missing")
        return [
            {
                "name": path.name,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in sorted(directory.iterdir())
            if path.is_file()
        ]

    def _child(self, directory: Path, filename: str) -> Path:
        if Path(filename).name != filename:
            raise ArtifactSecurityError("nested artifact filenames are not allowed")
        path = (directory / filename).resolve()
        self._validate(path)
        return path

    def _registered_file(self, registered: Path) -> Path:
        if registered.is_absolute():
            candidate = registered.resolve()
            if candidate != self.root and self.root not in candidate.parents:
                if len(registered.parts) < 3:
                    raise ArtifactSecurityError("invalid registered artifact path")
                candidate = (self.root / Path(*registered.parts[-3:])).resolve()
        else:
            candidate = (self.root / registered).resolve()
        self._validate(candidate)
        return candidate

    def _registered_directory(self, registered: Path) -> Path:
        if registered.is_absolute():
            candidate = registered.resolve()
            if candidate != self.root and self.root not in candidate.parents:
                if len(registered.parts) < 2:
                    raise ArtifactSecurityError("invalid registered artifact directory")
                candidate = (self.root / Path(*registered.parts[-2:])).resolve()
        else:
            candidate = (self.root / registered).resolve()
        self._validate(candidate)
        return candidate

    def _validate(self, path: Path) -> None:
        if path != self.root and self.root not in path.parents:
            raise ArtifactSecurityError("artifact path escapes configured storage")
