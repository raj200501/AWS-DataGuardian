"""Configuration loader for DataGuardian (stdlib-only)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

DEFAULT_DATA_DIR = Path("data")
DEFAULT_DB_NAME = "audit_results.db"


def load_dotenv(path: Path = Path(".env")) -> Dict[str, str]:
    """Minimal .env loader to avoid external dependencies."""

    if not path.exists():
        return {}

    values: Dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    sqlite_path: Path
    audit_timeout_seconds: int
    user_agent: str
    log_level: str

    @classmethod
    def load(cls) -> "Settings":
        env_values = load_dotenv()
        data_dir = Path(
            os.getenv("DATAGUARDIAN_DATA_DIR", env_values.get("DATAGUARDIAN_DATA_DIR", DEFAULT_DATA_DIR))
        ).expanduser()
        sqlite_path = Path(
            os.getenv(
                "DATAGUARDIAN_SQLITE_PATH",
                env_values.get("DATAGUARDIAN_SQLITE_PATH", data_dir / DEFAULT_DB_NAME),
            )
        ).expanduser()
        timeout = int(
            os.getenv("DATAGUARDIAN_AUDIT_TIMEOUT", env_values.get("DATAGUARDIAN_AUDIT_TIMEOUT", "10"))
        )
        user_agent = os.getenv(
            "DATAGUARDIAN_USER_AGENT",
            env_values.get("DATAGUARDIAN_USER_AGENT", "DataGuardian/1.0 (+local)"),
        )
        log_level = os.getenv("DATAGUARDIAN_LOG_LEVEL", env_values.get("DATAGUARDIAN_LOG_LEVEL", "INFO"))
        return cls(
            data_dir=data_dir,
            sqlite_path=sqlite_path,
            audit_timeout_seconds=timeout,
            user_agent=user_agent,
            log_level=log_level,
        )


def ensure_data_dir(settings: Settings) -> None:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
