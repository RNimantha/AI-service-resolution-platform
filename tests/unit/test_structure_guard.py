"""Regression cases for architectural rules rather than only compliant files."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[2] / "scripts" / "check_structure.py"


class TestStructureGuard(unittest.TestCase):
    def run_guard(self, files: dict[str, str]) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, source in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(source, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(CHECKER), "--root", str(root)],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_accepts_one_class_and_exactly_749_lines(self):
        result = self.run_guard({"component.py": "class Component:\n    pass\n" + "\n" * 747})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_750_lines(self):
        result = self.run_guard({"component.py": "# comment\n" * 750})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("750 lines", result.stdout)

    def test_rejects_nested_second_class(self):
        result = self.run_guard({"component.py": "class Outer:\n    class Inner:\n        pass\n"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("one class per file", result.stdout)

    def test_rejects_wildcard_import(self):
        result = self.run_guard({"component.py": "from typing import *\n"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("wildcard imports", result.stdout)

    def test_rejects_cross_service_and_shared_to_service_imports(self):
        files = {
            "src/main/app/services/rag_service/__init__.py": "",
            "src/main/app/services/agent_service/run.py": "from src.main.app.services.rag_service.application.rag_service import RagService\n",
            "src/main/app/shared/contracts/bad.py": "import src.main.app.services.rag_service\n",
        }
        result = self.run_guard(files)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout.count("cannot import service internals"), 2)

    def test_allows_public_cross_service_imports(self):
        result = self.run_guard(
            {
                "src/main/app/services/rag_service/__init__.py": "",
                "src/main/app/services/agent_service/run.py": "from src.main.app.services.rag_service import RagService\n",
            }
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_allows_own_service_imports_and_shared_contracts(self):
        result = self.run_guard(
            {
                "src/main/app/services/rag_service/run.py": "from src.main.app.services.rag_service.ports.retriever import Retriever\n"
                "from src.main.app.shared.contracts import RequestContext\n",
            }
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_ignores_dependency_directories(self):
        result = self.run_guard({".venv/library.py": "class A: pass\nclass B: pass\n"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_invalid_syntax(self):
        result = self.run_guard({"component.py": "class Broken\n"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected ':'", result.stdout)

    def test_rejects_fastapi_inside_a_business_service(self):
        result = self.run_guard(
            {
                "src/main/app/services/rag_service/http.py": "from fastapi import APIRouter\n",
            }
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FastAPI code belongs in controller", result.stdout)

    def test_allows_fastapi_inside_controller(self):
        result = self.run_guard(
            {
                "src/main/app/controller/router.py": "from fastapi import APIRouter\n",
            }
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_service_importing_controller(self):
        result = self.run_guard(
            {
                "src/main/app/services/rag_service/run.py": "from src.main.app.controller.router import router\n",
            }
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot import controllers", result.stdout)

    def test_rejects_relative_cross_service_internal_imports(self):
        result = self.run_guard(
            {
                "src/main/app/services/rag_service/__init__.py": "",
                "src/main/app/services/agent_service/run.py": "from ..rag_service.application.rag_service import RagService\n",
            }
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot import service internals", result.stdout)
