# Evidence-Based Repository Improvement Research

Research date: 2026-07-23

This research converts proven practices from mature open-source projects into a practical improvement system for Ravin Perera's public DevOps, AWS, observability, and AI-governance portfolio.

The aim is not to copy every file used by a large project. A practice is useful only when it improves usability, review evidence, regression protection, security, compatibility, maintainability, or the credibility of the portfolio.

## Scope

The weekly audit focuses on original showcase repositories rather than forks and older learning resources:

- `ravinperera/ravinperera`
- `ravinperera/ai-devops-guardrails`
- `ravinperera/ai-security-governance-checklist`
- `ravinperera/ai-token-efficiency-playbook`
- `ravinperera/aws-ecs-fargate-terraform-atmos`
- `ravinperera/aws-security-baseline-control-tower`
- `ravinperera/github-actions-oidc-aws-deployment`
- `ravinperera/ecs-observability-otel-opensearch`

Repository-specific opportunities are in the [tailored improvement roadmap](repository-improvement-roadmap.md).

## Reference repositories

| Reference | Pattern worth learning |
| --- | --- |
| [`kubernetes/kubernetes`](https://github.com/kubernetes/kubernetes) | Path-aware reviewers and approvers, security contacts, and explicit governance. |
| [`hashicorp/terraform`](https://github.com/hashicorp/terraform) | Issue-first proposals, small PRs, test expectations, and disciplined change history. |
| [`terraform-aws-modules/terraform-aws-vpc`](https://github.com/terraform-aws-modules/terraform-aws-vpc) | Runnable scenarios, pre-commit checks, Terraform validation, TFLint, and generated docs. |
| [`open-telemetry/opentelemetry-collector-contrib`](https://github.com/open-telemetry/opentelemetry-collector-contrib) | Stability levels, support ownership, visible build/release state, and change fragments. |
| [`github/docs`](https://github.com/github/docs) | Structured issue forms, contact routing, and documentation quality controls. |
| [`actions/checkout`](https://github.com/actions/checkout) | Architecture decisions, scenario-driven usage, and explicit credential behaviour. |
| [`ossf/scorecard`](https://github.com/ossf/scorecard) | Repeatable supply-chain and repository-security posture checks. |
| [`sigstore/cosign`](https://github.com/sigstore/cosign) | Release integrity, signatures, provenance, and compatibility expectations. |
| [`prometheus/prometheus`](https://github.com/prometheus/prometheus) | Operational documentation, maintainership, compatibility, and releases. |
| [`argoproj/argo-cd`](https://github.com/argoproj/argo-cd) | GitOps operations, security, upgrades, rollout, and rollback guidance. |

## Adoption test

A recommendation becomes implementation work only when it is:

1. **Applicable:** it closes a real gap in the target repository.
2. **Non-duplicate:** equivalent guidance or automation is not already present elsewhere.
3. **Verifiable:** it has acceptance criteria and a concrete check or expected result.
4. **Maintainable:** its ongoing cost fits a small public reference project.
5. **Safe:** it needs no production credentials, private data, or unsupported claims.
6. **Focused:** one issue and PR deliver one coherent outcome.
7. **Credible:** it improves engineering value, not merely contribution activity.

## Practice matrix

| Domain | P0: strongest defaults | P1: mature follow-through | P2: adopt selectively |
| --- | --- | --- | --- |
| Trust and contribution | Private security reporting; path-aware ownership; explicit licence for reusable work | Contributor workflow; PR evidence template; support/stability policy; structured issue forms | Code of conduct; issue chooser routing; governance expansion for multi-maintainer projects |
| Architecture and change | Runnable golden path; expected output and rollback | Architecture/data flow; ADRs; compatibility matrix; upgrade/deprecation guide; changelog; release process | Roadmap, non-goals, citation metadata |
| Quality | Credential-free PR CI; regression tests; Terraform native tests; workflow/config syntax checks | One local validation command; pre-commit; TFLint; generated Terraform docs; Markdown/link checks; golden fixtures | Reproducible dev container for complex projects |
| Security and supply chain | Least-privilege workflow permissions; fixed dependencies; branch rules; threat model | Dependabot; dependency review; CodeQL where language support is meaningful; secret scanning; Scorecard | Provenance and SBOM only when publishing real artifacts |
| Operations | Incident/rollback runbooks with stop conditions | SLOs; alerts; dashboards; audit evidence; cost/performance methodology; failure scenarios | Advanced load/failure injection when the example is stable enough to maintain |
| AI assurance | Evaluation corpus; adversarial cases; sensitive-data tests; human-approval boundaries | Machine-readable controls; tool/model compatibility; mapping provenance; reproducible measurement | Broader benchmark suites only after the methodology and quality guardrails are stable |

## What mature repositories do especially well

### 1. They provide executable proof

The biggest step beyond a polished README is turning claims into checks. Terraform examples should have `.tftest.hcl` assertions or credential-free plans. Workflow examples should pass action-specific linting. IAM, OIDC, telemetry, policy, and AI guidance should include valid and invalid fixtures. Documentation links and helper scripts should be tested automatically.

For this portfolio, executable proof is now more valuable than adding another generic checklist. The strongest next work includes Terraform mock-provider tests, OIDC claim fixtures, AI adversarial evals, CSV/schema validation, telemetry redaction tests, and golden expected outputs.

### 2. They separate support levels from marketing language

OpenTelemetry-style stability labels and compatibility matrices set realistic expectations. A reference repository should state whether an area is stable, experimental, illustrative, deprecated, or not tested in production. It should also record the last verified tool/provider versions and the boundaries of support.

This is especially important for copied Terraform patterns, GitHub Actions examples, OpenTelemetry/OpenSearch configuration, and agent instruction adapters.

### 3. They make ownership and decisions visible

Kubernetes-style ownership files route sensitive changes to the right reviewers. ADRs used by projects such as `actions/checkout` preserve context, alternatives, security assumptions, and consequences.

For a personal portfolio, ownership can remain lightweight, but workflows, IAM, security controls, Terraform state, and release files should still have clear review responsibility. ADRs are valuable for OIDC claim design, account structure, state layout, secret injection, observability routing, and AI approval boundaries.

### 4. They make change consumption predictable

Mature projects combine changelogs, versioning, support matrices, upgrade notes, and deprecation policy. This matters even for reference repositories because users may copy a version and return later.

A lightweight policy is enough: define what constitutes a breaking change, when a tag is created, what validation is required, and how an adopter can migrate or roll back.

### 5. They treat repository security as a system

A `SECURITY.md` alone is not the whole security posture. Strong projects combine private reporting, branch rules, least-privilege workflow permissions, controlled dependency updates, secret scanning, dependency review, static analysis where applicable, and periodic security-health checks.

Artifact attestations and SBOMs are valuable only for repositories that publish binaries, containers, packages, or archives. Adding them to documentation-only projects would be ceremony without a real artifact trust problem.

### 6. They document operational evidence, not only architecture

Production-facing examples should explain what proves success or failure. Useful evidence includes expected Terraform plan characteristics, CloudTrail correlation, alert queries, SLOs, deployment health signals, rollback verification, evidence ownership, and retention expectations.

Observability and deployment repositories gain credibility from importable dashboards, queries, sample alerts, redaction fixtures, and small reproducible load/cardinality experiments.

### 7. AI projects test refusal and escalation paths

AI safety guidance should be evaluated against unsafe as well as normal inputs. A useful corpus covers prompt injection, attempts to bypass approval, secret disclosure, fabricated validation evidence, excessive permissions, false positives, and cases where the agent must stop and escalate.

AI efficiency claims should measure quality together with token/input reduction. A smaller context is not an improvement when exact errors, task completion, safety evidence, or correctness are lost.

## Weekly research workflow

`.github/workflows/weekly-repository-research.yml` runs every Monday at `07:17 UTC` and supports manual dispatch. A path-limited push trigger validates changes to the audit itself.

The workflow:

1. fetches the exact workflow revision without a third-party checkout action;
2. runs unit tests for matching, relevance filters, reference evidence, and token scoping;
3. inspects public file trees and metadata for the eight showcase repositories;
4. inspects the curated reference set;
5. detects applicable practices that appear absent;
6. ranks them by risk, relevance, and observed reference adoption;
7. creates or refreshes one standing issue named **Weekly repository research backlog**.

It does **not** create commits, branches, or PRs. The report is input to the existing weekday routine, which remains limited to up to three meaningful improvements and should skip duplicate or unsuitable recommendations.

## Weekly review checklist

Before implementing a reported item:

- search for equivalent content under another filename or README section;
- confirm a real user, reviewer, operator, or security outcome;
- define acceptance criteria and validation evidence;
- prefer tests, examples, schemas, or operational evidence over prose-only changes;
- keep examples free of real credentials, account IDs, customer data, and internal configuration;
- use a focused issue, branch, and PR;
- merge only after checks pass and the issue is resolved;
- record why a recommendation was skipped when it does not fit.

## Limitations

- File presence is a signal, not a quality assessment.
- Branch rules, private vulnerability reporting, push protection, and some security settings require manual review.
- Adoption by a famous repository is supporting evidence, not proof that a practice belongs everywhere.
- Public cross-repository inspection uses a deliberately small GitHub API request budget.
- GitHub schedules use UTC, may be delayed during high load, and run from the default branch.
- GitHub may disable a public repository's scheduled workflow after 60 days with no repository activity; manual dispatch remains available.
- The reference set and practice catalogue should be reviewed quarterly to avoid outdated assumptions.

## Primary documentation consulted

- [GitHub healthy-contribution guidance](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions)
- [GitHub issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [GitHub Actions permissions](https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs)
- [GitHub scheduled workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
- [GitHub CodeQL default setup](https://docs.github.com/en/code-security/code-scanning/enabling-code-scanning/configuring-default-setup-for-code-scanning)
- [OpenSSF Scorecard action](https://github.com/ossf/scorecard-action)
- [GitHub artifact attestations](https://docs.github.com/en/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds)
- [Terraform native tests](https://developer.hashicorp.com/terraform/language/tests)
