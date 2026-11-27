"""Check Python file limits, service ownership, and HTTP framework boundaries."""

from __future__ import annotations

import argparse
import ast
import os
from importlib.util import resolve_name
from pathlib import Path

MAX_LINES = 749
APP_PARTS = ("src", "main", "app")
SERVICE_PARTS = (*APP_PARTS, "services")
SERVICE_PREFIX = ".".join(SERVICE_PARTS)
CONTROLLER_PARTS = (*APP_PARTS, "controller")
CONTROLLER_PREFIX = ".".join(CONTROLLER_PARTS)
EXCLUDED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    ".cache",
    ".ruff_cache",
    ".pytest_cache",
    ".mypy_cache",
    "__pycache__",
    "node_modules",
    "build",
    "dist",
    "data",
    "artifacts",
}


def python_files(root: Path):
    """Traverse authored source without walking dependencies or runtime data."""
    for directory, subdirectories, filenames in os.walk(root):
        subdirectories[:] = sorted(
            name for name in subdirectories if name not in EXCLUDED_DIRECTORIES
        )
        for filename in sorted(filenames):
            if filename.endswith(".py"):
                yield Path(directory) / filename


def check_file(path: Path, root: Path, service_names: set[str]) -> list[str]:
    """Inspect physical lines, nested classes, and absolute or relative imports."""
    relative = path.relative_to(root)
    source = path.read_text(encoding="utf-8")
    errors = []
    lines = len(source.splitlines())
    if lines > MAX_LINES:
        errors.append(f"{relative}: {lines} lines; maximum is {MAX_LINES}")
    try:
        tree = ast.parse(source, filename=str(relative))
    except SyntaxError as error:
        return [*errors, f"{relative}:{error.lineno}: {error.msg}"]

    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    if len(classes) > 1:
        names = ", ".join(node.name for node in classes)
        errors.append(f"{relative}: one class per file; found {names}")

    parts = relative.parts
    owner = parts[4] if parts[:4] == SERVICE_PARTS and len(parts) > 4 else None
    is_app = parts[:3] == APP_PARTS
    is_shared = parts[:4] == (*APP_PARTS, "shared")
    is_controller = parts[:4] == CONTROLLER_PARTS
    package = ".".join(parts[:-1])
    for node in ast.walk(tree):
        imported = []
        if isinstance(node, ast.Import):
            imported = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if any(alias.name == "*" for alias in node.names):
                errors.append(f"{relative}:{node.lineno}: wildcard imports are forbidden")
            if node.level:
                try:
                    imported = [resolve_name("." * node.level + (node.module or ""), package)]
                except (ValueError, ImportError) as error:
                    errors.append(f"{relative}:{node.lineno}: invalid relative import: {error}")
            elif node.module:
                imported = [node.module]
        for module in imported:
            if module.startswith(SERVICE_PREFIX + "."):
                suffix = module.removeprefix(SERVICE_PREFIX + ".").split(".")
                service = suffix[0]
                if service in service_names and (
                    is_shared or (owner and service != owner and len(suffix) > 1)
                ):
                    errors.append(
                        f"{relative}:{node.lineno}: cannot import service internals {module}; "
                        "use its public package interface"
                    )
            if (owner or is_shared) and (
                module == CONTROLLER_PREFIX or module.startswith(CONTROLLER_PREFIX + ".")
            ):
                errors.append(
                    f"{relative}:{node.lineno}: services and contracts cannot import controllers"
                )
            if is_app and not is_controller and module.split(".")[0] in {"fastapi", "starlette"}:
                errors.append(f"{relative}:{node.lineno}: FastAPI code belongs in controller")
            if module.split(".")[0] in service_names | {"asrp_contracts"}:
                errors.append(f"{relative}:{node.lineno}: use the src.main.app package path")
    return errors


def check_project(root: Path) -> tuple[list[str], int]:
    """Check the application; third-party code is outside this policy."""
    service_root = root.joinpath(*SERVICE_PARTS)
    service_names = (
        {
            path.name
            for path in service_root.iterdir()
            if path.is_dir() and path.name != "__pycache__"
        }
        if service_root.exists()
        else set()
    )
    files = list(python_files(root))
    errors = []
    for path in files:
        errors.extend(check_file(path, root, service_names))
    return errors, len(files)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    arguments = parser.parse_args()
    root = arguments.root.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    errors, count = check_project(root)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Structure checks passed for {count} Python files (maximum {MAX_LINES} lines).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
