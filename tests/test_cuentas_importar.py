import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "herramientas" / "cuentas_importar.py"

class ImportadorTests(unittest.TestCase):
    def test_auditoria_y_aplicacion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "cuentas.txt"
            config = root / "config.json"
            config.write_text(json.dumps({"accounts": [
                {"id": "Account_1", "email": "usuario@gmail.com", "password": "original"}
            ]}), encoding="utf-8")
            source.write_text("u.s.u.a.r.i.o@gmail.com----nueva\notra@gmail.com----clave\n", encoding="utf-8")
            command = [sys.executable, str(SCRIPT), "--source", str(source), "--config", str(config)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(json.loads(config.read_text())["accounts"]), 1)
            result = subprocess.run(command + ["--apply"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            accounts = json.loads(config.read_text())["accounts"]
            self.assertEqual(len(accounts), 2)
            self.assertEqual(accounts[0]["password"], "original")
            self.assertEqual(accounts[1]["status"], "pending")
            self.assertTrue(list(root.glob("config.json.bak-*")))
            result = subprocess.run(command + ["--apply"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(json.loads(config.read_text())["accounts"]), 2)

if __name__ == "__main__":
    unittest.main()
