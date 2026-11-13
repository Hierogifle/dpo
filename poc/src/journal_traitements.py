"""Journal JSONL minimal des exécutions; jamais d'identifiants ou de lignes utilisateurs."""
import json
from datetime import datetime, timezone
from pathlib import Path


def log_event(event: str, status: str, counts: dict | None = None,
              path: Path = Path("reports/journal/traitements.jsonl")):
    if event not in {"generation", "pseudonymisation", "controle_qualite", "purge"}:
        raise ValueError("Type d'événement non autorisé")
    if status not in {"success", "error", "dry_run"}:
        raise ValueError("Statut non autorisé")
    safe = {}
    for key, value in (counts or {}).items():
        if key not in {"input_rows", "output_rows", "removed_rows", "issues", "checked_rows"}:
            raise ValueError(f"Champ interdit dans le journal : {key}")
        if type(value) is not int or value < 0:
            raise ValueError("Le journal accepte uniquement des compteurs >= 0")
        safe[key] = value
    event_data = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "event": event, "status": status, "counts": safe,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event_data, ensure_ascii=False) + "\n")
    return event_data
