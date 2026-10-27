"""Real, implementation-coupled negative tests for the offline netting gate."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from netting_gate import validate_batch


def batch(*positions):
    return {"positions": [{"currency": c, "amount": a} for c, a in positions]}


class NettingGateTests(unittest.TestCase):
    def test_balanced_single_currency(self):
        self.assertEqual(validate_batch(batch(("USD", "10.25"), ("USD", "-10.25"))), ["USD"])

    def test_balanced_multi_currency(self):
        data = batch(("USD", "2.00"), ("EUR", "-3"), ("USD", "-2"), ("EUR", "+3.00"))
        self.assertEqual(validate_batch(data), ["EUR", "USD"])

    def test_unbalanced_fails(self):
        with self.assertRaises(ValueError):
            validate_batch(batch(("USD", "1"), ("USD", "-0.99")))

    def test_cross_currency_cannot_cancel(self):
        with self.assertRaises(ValueError):
            validate_batch(batch(("USD", "1"), ("EUR", "-1")))

    def test_float_fails(self):
        with self.assertRaises(ValueError):
            validate_batch(batch(("USD", 0.1), ("USD", "-0.10")))

    def test_nan_fails(self):
        with self.assertRaises(ValueError):
            validate_batch(batch(("USD", "NaN"), ("USD", "-1")))

    def test_fractional_precision_fails(self):
        with self.assertRaises(ValueError):
            validate_batch(batch(("USD", "0.001"), ("USD", "-0.001")))

    def test_invalid_currency_fails(self):
        with self.assertRaises(ValueError):
            validate_batch(batch(("usd", "1"), ("usd", "-1")))

    def test_missing_field_fails(self):
        with self.assertRaises(ValueError):
            validate_batch({"positions": [{"currency": "USD"}, {"currency": "USD", "amount": "0"}]})

    def test_extra_field_fails(self):
        with self.assertRaises(ValueError):
            validate_batch({"positions": [], "approved": True})

    def test_empty_fails(self):
        with self.assertRaises(ValueError):
            validate_batch({"positions": []})

    def test_oversized_amount_fails(self):
        with self.assertRaises(ValueError):
            validate_batch(batch(("USD", "1000000000000"), ("USD", "-1000000000000")))

    def test_cli_success_and_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "batch.json"
            path.write_text(json.dumps(batch(("USD", "3"), ("USD", "-3"))), encoding="utf-8")
            good = subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / "netting_gate.py"), str(path)], capture_output=True, text=True)
            self.assertEqual(good.returncode, 0, good.stderr)
            path.write_text(json.dumps(batch(("USD", "3"), ("USD", "-2"))), encoding="utf-8")
            bad = subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / "netting_gate.py"), str(path)], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 1)

    def test_cli_missing_file_fails(self):
        p = subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / "netting_gate.py"), "/nonexistent/qmoosa-batch.json"], capture_output=True)
        self.assertEqual(p.returncode, 1)


if __name__ == "__main__":
    unittest.main()
