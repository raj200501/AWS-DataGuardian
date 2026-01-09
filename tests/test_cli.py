import json
import os
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


class CliTestCase(unittest.TestCase):
    def test_cli_audit_and_list(self):
        html_file = Path("tests/fixtures/sample_page.html")
        with TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["DATAGUARDIAN_DATA_DIR"] = tmp
            env["DATAGUARDIAN_SQLITE_PATH"] = str(Path(tmp) / "audit.db")

            result = subprocess.run(
                ["python", "-m", "dataguardian.cli", "audit", "--html-file", str(html_file)],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )

            payload = json.loads(result.stdout)
            self.assertGreaterEqual(payload["trackers"], 3)
            self.assertGreaterEqual(payload["id"], 1)

            list_result = subprocess.run(
                ["python", "-m", "dataguardian.cli", "list"],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertIn("trackers", list_result.stdout)


if __name__ == "__main__":
    unittest.main()
