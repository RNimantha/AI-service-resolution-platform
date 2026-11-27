"""HTTP and startup regression checks after moving the application package."""

import subprocess
import sys
import unittest

import httpx

from src.main.app.controller.app_factory import create_app


class TestApplication(unittest.IsolatedAsyncioTestCase):
    async def test_liveness_works_without_model_or_database_adapters(self):
        transport = httpx.ASGITransport(app=create_app())
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/health/live")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_importing_entry_point_does_not_start_a_server(self):
        result = subprocess.run(
            [sys.executable, "-c", "import src.main.app.main"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")
