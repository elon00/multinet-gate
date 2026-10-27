# Multinet Gate — bounded architecture and evidence

Canonical QMOOSA-1000 ID: **QMOOSA-0965**; role: **TESTS**; family: institutional multi-currency liquidity netting (Batch 193).

## Implemented and testable

- `netting_gate.py`: deterministic, offline, exact-Decimal per-currency zero-sum checker for a bounded JSON batch (2–1000 entries; <=1 MB input file).
- `tests/test_netting_gate.py`: positive, negative, adversarial and subprocess regression cases.
- GitHub Actions: Python regression and CodeQL analysis with initialization, plus Rust formatting and compilation.
- Rust entrypoint: explicitly fail-closed, with no simulated settlement or false RPC/PQC/production claims.

## Not implemented

Settlement orchestration, ledger persistence, counterparty authentication, authorization, replay protection, FX conversion, slippage control, liquidity proof, regulated custody, transaction finality, live RPC, PQC/FIPS, x402, Conway automata, AI agents, and mainnet/testnet deployment. These are **not verified** and must not be inferred from offline tests.

## Security gates

Reject invalid currencies, float/NaN, excessive precision, oversized amounts, missing/extra fields, empty batches, cross-currency offsetting and unbalanced sums. Independent threat modeling, ledger-level reconciliation, concurrency/restart negative tests and security review are required before any production claim.
