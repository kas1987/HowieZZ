import sys
from pathlib import Path

# Ensure scripts/ is importable so tests can do: import build_profiles, etc.
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
