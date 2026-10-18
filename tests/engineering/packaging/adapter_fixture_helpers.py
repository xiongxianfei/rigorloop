"""Own diagnostics for the real archive/install observation."""
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

def configure_adapter_case(add_cleanup) -> None:
    """Own the diagnostics of real installed CLI children for this case."""
    temporary = tempfile.TemporaryDirectory(prefix="adapter-case-")
    add_cleanup(temporary.cleanup)
    environment = patch.dict(os.environ, {
        "RIGORLOOP_LOG_DIR": str(Path(temporary.name) / "logs"),
    })
    environment.start()
    add_cleanup(environment.stop)
