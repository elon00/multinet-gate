# Multinet Gate — offline netting conservation checker

**Scope:** Approved QMOOSA-1000 component QMOOSA-0965, Batch 193, tests role.

This repository is **not production ready**. The only implemented gate checks whether a user-supplied JSON batch balances independently within each three-letter currency. It uses exact decimal arithmetic, rejects floating-point amounts and malformed inputs, and has no network, settlement, signature, identity, liquidity, credit, FX, or transaction-finality integration.

## Run locally

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python netting_gate.py batch.json
cargo check --locked
```

Example `batch.json`:

```json
{"positions":[{"currency":"USD","amount":"10.25"},{"currency":"USD","amount":"-10.25"}]}
```

Exit codes: 0 balanced; 1 invalid/unbalanced/file failure; 2 CLI usage error. The Rust binary deliberately exits 2 because a Rust settlement engine is not implemented.

## Verification limits

This offline invariant is necessary but nowhere near sufficient for settlement. It does **not** prove solvency, available balances, authorized transfers, replay protection, counterparty consent, double-entry ledger correctness, payment finality, regulatory compliance, security approval, FIPS validation, or deployment readiness. All those remain **BLOCKED / NOT VERIFIED**.

See `ARCHITECTURE.md` and `SECURITY.md`. Do not deploy or process real funds based on this gate.
