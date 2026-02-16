from __future__ import annotations
import json
from pathlib import Path

APP_DIR = Path.home() / ".cli_arcade"
PROGRESS_FILE = APP_DIR / "progress.json"

def default_progress() -> dict:
    return {"version": 1, "games": {}}

def _normalize_progress(data: dict) -> dict:
    if "games" not in data or not isinstance(data["games"], dict):
        data["games"] = {}

    for _, stats in data["games"].items():
        if not isinstance(stats, dict):
            continue
        stats.setdefault("played", 0)
        stats.setdefault("wins", 0)
        stats.setdefault("draws", 0)

    return data

def load_progress() -> dict:
    try:
        data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict) and data.get("version") == 1:
            return _normalize_progress(data)
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return default_progress()

def save_progress(progress: dict) -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(_normalize_progress(progress), indent=2), encoding="utf-8")

def record_result(
    progress: dict,
    game_id: str,
    *,
    played: int = 1,
    wins: int = 0,
    draws: int = 0,
) -> None:
    g = progress["games"].setdefault(game_id, {"played": 0, "wins": 0, "draws": 0})
    g.setdefault("played", 0)
    g.setdefault("wins", 0)
    g.setdefault("draws", 0)
    g["played"] += played
    g["wins"] += wins
    g["draws"] += draws
