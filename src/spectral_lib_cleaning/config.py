import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    project_root: Path = field(default_factory=lambda: Path.cwd())

    def __post_init__(self) -> None:
        if not isinstance(self.project_root, Path):
            self.project_root = Path(self.project_root)

    @property
    def raw_dir(self) -> Path:
        return self.project_root / "data" / "raw"

    @property
    def processed_dir(self) -> Path:
        return self.project_root / "data" / "processed"

    @property
    def download_dir(self) -> Path:
        return self.project_root / "data" / "downloads"
