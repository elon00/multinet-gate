"""Offline conservation-of-value gate for a single multi-currency netting batch.

This does not execute settlement, verify signatures, or prove solvency.
"""
import json
import re
import sys
from decimal import Decimal
from pathlib import Path

CURRENCY = re.compile(r"[A-Z]{3}\Z")
AMOUNT = re.compile(r"[+-]?(?:0|[1-9][0-9]{0,11})(?:\.[0-9]{1,2})?\Z")


def validate_batch(document):
    if not isinstance(document, dict) or set(document) != {"positions"}:
        raise ValueError("document must contain only positions")
    positions = document["positions"]
    if not isinstance(positions, list) or not 2 <= len(positions) <= 1000:
        raise ValueError("positions count must be between 2 and 1000")
    totals = {}
    for index, item in enumerate(positions):
        if not isinstance(item, dict) or set(item) != {"currency", "amount"}:
            raise ValueError(f"invalid position {index}")
        currency, amount = item["currency"], item["amount"]
        if not isinstance(currency, str) or not CURRENCY.fullmatch(currency):
            raise ValueError(f"invalid currency at {index}")
        if not isinstance(amount, str) or not AMOUNT.fullmatch(amount):
            raise ValueError(f"invalid decimal amount at {index}")
        totals[currency] = totals.get(currency, Decimal(0)) + Decimal(amount)
    unbalanced = {key: str(value) for key, value in totals.items() if value != 0}
    if unbalanced:
        raise ValueError(f"unbalanced currency totals: {unbalanced}")
    return sorted(totals)


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: python netting_gate.py BATCH.json", file=sys.stderr)
        return 2
    try:
        path = Path(args[0])
        if path.stat().st_size > 1_000_000:
            raise ValueError("batch file too large")
        data = json.loads(path.read_text(encoding="utf-8"))
        currencies = validate_batch(data)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"REJECTED: {exc}", file=sys.stderr)
        return 1
    print("OFFLINE BALANCE CHECK PASSED: " + ", ".join(currencies))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
