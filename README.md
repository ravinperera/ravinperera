# Hi, I'm Ravin Perera

DevOps Manager focused on AWS platforms, infrastructure automation, CI/CD, security, and reliable delivery.

I work across cloud architecture, platform engineering, release automation, and operational governance, with a strong focus on building secure and repeatable systems for multi-environment SaaS platforms.

## What I Work On

- AWS platform architecture across development, staging, and production environments
- ECS/Fargate workloads, ALB, CloudFront, Cloudflare, Route 53, RDS, Redis, and OpenSearch
- Terraform and Atmos-based infrastructure as code
- GitHub Actions CI/CD with OIDC-based AWS deployments
- Secrets management using AWS Secrets Manager and least-privilege IAM
- Observability using CloudWatch, OpenTelemetry, and centralized logging
- Security and compliance alignment for ISO 27001, SOC 2, GDPR, and client assurance requirements

## Platform Engineering Principles

- Make secure defaults easy for engineering teams to adopt.
- Prefer repeatable infrastructure patterns over one-off manual fixes.
- Keep deployment pipelines simple enough to operate under pressure.
- Treat observability, access control, and rollback planning as part of delivery, not afterthoughts.
- Document operational decisions so future support and audits are easier.

## Current Focus

- Production-grade ECS deployment patterns for Django and Celery workloads
- Secure GitHub-to-AWS deployment automation using OIDC
- Reducing manual infrastructure operations through reusable Terraform components
- Improving access governance, secrets handling, logging, and monitoring across cloud environments
- Practical AI security, governance, and token efficiency for engineering teams

## AI Engineering Governance Framework

The four AI repositories below are designed to be read together as one practical framework rather than as isolated projects:

1. Start with [`ai-security-governance-checklist`](https://github.com/ravinperera/ai-security-governance-checklist) for organisation-level controls, risk boundaries, evidence, and governance expectations.
2. Use [`ai-agent-registry-governance`](https://github.com/ravinperera/ai-agent-registry-governance) to catalogue and approve agents, skills, MCP servers, and related AI resources.
3. Apply [`ai-devops-guardrails`](https://github.com/ravinperera/ai-devops-guardrails) when AI is reviewing or assisting with infrastructure, CI/CD, IAM, deployments, and other operational changes.
4. Use [`ai-token-efficiency-playbook`](https://github.com/ravinperera/ai-token-efficiency-playbook) to reduce unnecessary context and token use without weakening verification or traceability.

Together, they cover **what is allowed, what is registered, how engineering actions are constrained, and how AI context is used efficiently**. See the [project map](docs/project-map.md) for the wider portfolio and repository relationships.

## Showcase Projects

- [`ai-token-efficiency-playbook`](https://github.com/ravinperera/ai-token-efficiency-playbook) - drop-in instructions, prompts, and workflows to reduce token usage across AI coding agents
- [`ai-security-governance-checklist`](https://github.com/ravinperera/ai-security-governance-checklist) - practical AI security and governance checklist for engineering, DevOps, SaaS, and regulated environments
- [`ai-devops-guardrails`](https://github.com/ravinperera/ai-devops-guardrails) - operational guardrails for safer AI-assisted DevOps reviews and deployment decisions
- [`ai-agent-registry-governance`](https://github.com/ravinperera/ai-agent-registry-governance) - policy-as-code approach for cataloguing and approving AI agents, skills, and MCP resources
- [`aws-ecs-fargate-terraform-atmos`](https://github.com/ravinperera/aws-ecs-fargate-terraform-atmos) - reusable Terraform/Atmos pattern for ECS services
- [`github-actions-oidc-aws-deployment`](https://github.com/ravinperera/github-actions-oidc-aws-deployment) - secure GitHub Actions deployment flow using AWS OIDC roles
- [`aws-security-baseline-control-tower`](https://github.com/ravinperera/aws-security-baseline-control-tower) - AWS multi-account governance and security baseline
- [`ecs-observability-otel-opensearch`](https://github.com/ravinperera/ecs-observability-otel-opensearch) - ECS logging, telemetry, and OpenSearch observability pattern

See the [project map](docs/project-map.md) for how these repositories fit together.

## Validate Profile Documentation

Run the dependency-free checks before changing the profile README or project documentation:

```bash
python3 -m unittest discover -s tests -p 'test_validate_profile.py' -v
python3 scripts/validate_profile.py
```

The validator checks `README.md` and Markdown under `docs/` for UTF-8 text hygiene, final newlines, trailing whitespace, repository-boundary-safe relative links, and missing local link targets. It ignores external URLs, anchors, and links shown inside fenced code examples.

GitHub Actions runs the same dependency-free tests and validation on relevant pull requests and pushes to `main` with read-only repository permissions and no cloud credentials.

## Portfolio Maintenance

The [repository improvement research](docs/repository-improvement-research.md) records the engineering practices used to evaluate this portfolio and a tailored backlog for each showcase repository. A weekly GitHub Actions audit refreshes one standing research issue; weekday implementation work remains limited to focused, useful changes with issues, validation, and normal pull-request review.

## Core Stack

AWS, Terraform, Atmos, GitHub Actions, Docker, ECS Fargate, RDS, Redis, OpenSearch, CloudWatch, OpenTelemetry, Cloudflare, Microsoft Entra ID, IAM Identity Center, Secrets Manager, Linux, Python, Django, Bash.

## Profile Note

Some older repositories on this profile are forks or learning resources. The pinned repositories are intended to represent my own architecture, automation, and platform engineering work.
