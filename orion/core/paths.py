import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESOURCES_DIR = PROJECT_ROOT.parent / "resources"


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    resources_candidate = (RESOURCES_DIR / relative_path).resolve()
    if resources_candidate.exists():
        return str(resources_candidate)

    project_candidate = (PROJECT_ROOT / relative_path).resolve()
    return str(project_candidate)