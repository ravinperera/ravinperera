# Project Map

This page explains how the highlighted repositories fit together across platform engineering, AWS operations, security, observability, and AI governance.

## AI Engineering Governance Framework

The AI repositories form one layered framework with a clear responsibility boundary:

| Layer | Repository | Primary question |
| --- | --- | --- |
| Governance baseline | [`ai-security-governance-checklist`](https://github.com/ravinperera/ai-security-governance-checklist) | What controls, evidence, risk boundaries, and review expectations should apply? |
| Resource registry | [`ai-agent-registry-governance`](https://github.com/ravinperera/ai-agent-registry-governance) | Which agents, skills, MCP servers, and related resources are approved and under what conditions? |
| Engineering execution | [`ai-devops-guardrails`](https://github.com/ravinperera/ai-devops-guardrails) | How should AI-assisted infrastructure and delivery work be constrained, reviewed, and stopped safely? |
| Context efficiency | [`ai-token-efficiency-playbook`](https://github.com/ravinperera/ai-token-efficiency-playbook) | How can agents use less context and fewer tokens without dropping required evidence or verification? |

A practical reading order is governance baseline → resource registry → engineering execution → context efficiency. The repositories remain independently useful, but cross-link instead of duplicating controls where possible.

## Portfolio repositories

| Area | Repository | What it demonstrates |
| --- | --- | --- |
| AI engineering efficiency | [`ai-token-efficiency-playbook`](https://github.com/ravinperera/ai-token-efficiency-playbook) | Practical guidance, templates, and workflows for reducing low-value AI context while keeping results reproducible. |
| AI governance | [`ai-security-governance-checklist`](https://github.com/ravinperera/ai-security-governance-checklist) | Security and governance controls for engineering teams adopting AI tools. |
| AI-assisted DevOps safety | [`ai-devops-guardrails`](https://github.com/ravinperera/ai-devops-guardrails) | Review-first guardrails for safer AI-assisted infrastructure, CI/CD, IAM, and deployment work. |
| AI agent governance | [`ai-agent-registry-governance`](https://github.com/ravinperera/ai-agent-registry-governance) | Policy-as-code patterns for cataloguing, approving, pinning, and reviewing AI agents, skills, MCP servers, and related resources. |
| ECS platform delivery | [`aws-ecs-fargate-terraform-atmos`](https://github.com/ravinperera/aws-ecs-fargate-terraform-atmos) | Reusable Terraform and Atmos patterns for containerized AWS workloads. |
| Secure CI/CD | [`github-actions-oidc-aws-deployment`](https://github.com/ravinperera/github-actions-oidc-aws-deployment) | GitHub Actions to AWS deployment using OIDC instead of long-lived access keys. |
| AWS governance | [`aws-security-baseline-control-tower`](https://github.com/ravinperera/aws-security-baseline-control-tower) | Multi-account AWS security baseline concepts and operational controls. |
| Observability | [`ecs-observability-otel-opensearch`](https://github.com/ravinperera/ecs-observability-otel-opensearch) | Logging, metrics, tracing, and OpenSearch patterns for ECS workloads. |

## How to read the wider portfolio

- Start with the AI Engineering Governance Framework above for AI-assisted engineering governance and execution.
- Start with the AWS and ECS repositories for platform engineering examples.
- Review the OIDC repository for secure deployment automation.
- Use the observability repository to understand operational visibility patterns.
