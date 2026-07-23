# Tailored Repository Improvement Roadmap

Research date: 2026-07-23

This roadmap contains the strongest repository-specific opportunities identified from the reference research. It is a prioritised idea bank, not an instruction to implement everything. Each item must pass the adoption rules in [the main research document](repository-improvement-research.md).

These are the strongest next directions based on the current portfolio, not an instruction to implement all of them immediately.

### `ravinperera/ravinperera`

1. Add three compact case studies: secure AWS OIDC deployment, ECS platform pattern, and AI-governance rollout. Each should show context, constraints, decision, implementation, validation evidence, trade-offs, and outcome.
2. Add an evidence index linking directly to tests, workflows, threat models, runbooks, and architecture documents across showcase repositories.
3. Add a capability matrix showing which repository demonstrates AWS architecture, Terraform, CI/CD, security, observability, incident readiness, and governance.
4. Keep badges limited to real signals such as passing CI or a release; avoid decorative stacks of badges.

### `ravinperera/ai-devops-guardrails`

1. Build a regression corpus for safe and unsafe Terraform, IAM, workflow, secret, DNS, database, and deployment changes.
2. Add adversarial cases that test prompt injection, instructions to bypass approval, fabricated validation evidence, and excessive permissions.
3. Publish a machine-readable guardrail schema with stable rule IDs, severity, trigger, required evidence, stop condition, and remediation.
4. Add an adapter compatibility matrix with last-tested versions and known limitations.
5. Version the rule set and document behavioural changes that could alter agent decisions.

### `ravinperera/ai-security-governance-checklist`

1. Convert the core control catalogue into versioned YAML/JSON with stable control IDs and schema validation.
2. Add a sample evidence pack showing what acceptable evidence looks like for inventory, vendor review, access, incident response, and periodic reassessment.
3. Add mapping provenance: exact OWASP/NIST/ISO source version, mapping date, interpretation caveat, and owner.
4. Add automated tests that CSV/JSON/YAML templates have required columns, unique IDs, valid dates, and controlled values.
5. Introduce a lightweight release and compatibility policy so adopters can tell when mappings or controls materially changed.

### `ravinperera/ai-token-efficiency-playbook`

1. Create a fixed evaluation corpus covering CI logs, Terraform plans, code review, debugging, architecture, and handoff tasks.
2. Measure token/input reduction alongside quality safeguards such as exact-error retention, task completion, and reviewer-rated correctness.
3. Add regression tests for the context estimator and hygiene checker, including malformed, empty, Unicode, and large-input cases.
4. Add a tool compatibility matrix and a last-verified date for every adapter file.
5. Publish raw result files and a methodology before making any comparative efficiency claim.

### `ravinperera/aws-ecs-fargate-terraform-atmos`

1. Add native Terraform tests for validation rules, expected outputs, deployment settings, logging, secrets, and invalid combinations; use mock providers where live AWS is unnecessary.
2. Add TFLint and generated variable/output documentation, checked in CI.
3. Add actionlint/security linting for deployment workflows and pin action dependencies deliberately.
4. Add a tested compatibility matrix for Terraform, AWS provider, Atmos, and workflow runner assumptions.
5. Add ADRs for deployment controller/circuit breaker, network placement, secret injection, health checks, logging, and state layout.
6. Include a non-production golden-path example with expected plan characteristics and explicit cleanup steps.

### `ravinperera/aws-security-baseline-control-tower`

1. Add Terraform tests and policy-as-code assertions for public access blocks, logging, encryption, and permission-boundary expectations.
2. Add negative fixtures that intentionally violate controls and prove CI rejects them.
3. Add stable control IDs mapped to AWS Security Hub Foundational Security Best Practices and other selected baselines, with version/date provenance.
4. Add machine-readable evidence definitions: evidence source, collection command/API, owner, cadence, retention, and sensitivity.
5. Add ADRs for account structure, delegated administration, log archive trust, break-glass design, and exception handling.
6. Add a compatibility/support matrix for Terraform, AWS provider, Control Tower assumptions, and regions/features not covered.

### `ravinperera/github-actions-oidc-aws-deployment`

1. Add automated positive and negative tests for OIDC `sub`, `aud`, environment, branch, tag, and reusable-workflow claim patterns.
2. Add actionlint and workflow security analysis; treat unsafe expression use, mutable dependencies, and excessive token permissions as failures.
3. Add fixtures that prove wildcard `iam:PassRole`, broad resource scopes, or untrusted subjects are rejected.
4. Add a reusable workflow example with a clear caller/callee trust boundary and fixed permissions.
5. Add a compatibility matrix for runner, action, Terraform/provider, AWS partition, and environment-protection assumptions.
6. Add an ADR explaining the chosen subject-claim strategy and alternatives that were rejected.

### `ravinperera/ecs-observability-otel-opensearch`

1. Add syntax and schema validation for OpenTelemetry, Fluent Bit, IAM JSON, ECS task definitions, and Terraform.
2. Add golden telemetry fixtures proving field names, trace/log correlation, routing, and redaction behaviour.
3. Add sensitive-data regression tests for credentials, tokens, personal data, request bodies, and high-risk headers.
4. Add importable dashboard, alert, and saved-query examples with clear expected signals.
5. Add SLO examples for ingestion success, export failures, dropped spans/logs, queue pressure, and OpenSearch health.
6. Add a small repeatable load/cardinality experiment that records volume, index growth, query latency, retention, and cost caveats.
7. Add a tested compatibility matrix for collector, Fluent Bit, OpenSearch, Terraform/provider, and ECS platform versions.
