"""Non-semantic store classification shared with the CLI implementation."""
from pathlib import Path
import subprocess

SCRIPT = Path(__file__).resolve().with_name("classify-record-store.mjs")

def is_archival_record_store(root: Path, change_id: str, revision: str | None = None) -> bool:
    command = ["node", str(SCRIPT), str(root), change_id]
    if revision is not None:
        command.append(revision)
    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    # Errors must continue to the owning validator, never exclude malformed data.
    return result.returncode == 0 and result.stdout.strip() == "archive"
