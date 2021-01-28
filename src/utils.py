from pathlib import Path

def get_project_rootdir() -> Path:
    return Path(__file__).parent
