# Security status — not certified

This is a bounded offline arithmetic test utility, **not a payment processor**. No FIPS 203/204/205 implementation or validation, authenticated transport, secure key management, live RPC, custody or production settlement is claimed.

Do not provide real financial or customer data to unreviewed tools. Report security findings through GitHub Security Advisories when available; do not post secrets in public issues.

Release blockers: independently audited settlement semantics, authorization, immutable journal, replay protection, concurrency safety, input provenance, idempotency, external reconciliation, and deployment evidence. Passing local regression tests or CodeQL alone is not security approval.
