#!/usr/bin/env python3
"""Refresh a weekly, evidence-based improvement backlog for Ravin's public portfolio."""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Mapping, Sequence
from typing import Any

API_ROOT = "https://api.github.com"
API_VERSION = "2026-03-10"
REPORT_TITLE = "Weekly repository research backlog"
PRIORITY = {"P0": 3, "P1": 2, "P2": 1}


@dataclasses.dataclass(frozen=True)
class Target:
    repository: str
    tags: frozenset[str]
    purpose: str


@dataclasses.dataclass(frozen=True)
class Reference:
    repository: str
    focus: str


@dataclasses.dataclass(frozen=True)
class Practice:
    key: str
    title: str
    priority: str
    why: str
    issue: str
    patterns: tuple[str, ...]
    tags: frozenset[str] = frozenset()
    exclude: frozenset[str] = frozenset()

    def applies(self, target: Target) -> bool:
        return not self.exclude.intersection(target.tags) and (
            not self.tags or bool(self.tags.intersection(target.tags))
        )


@dataclasses.dataclass(frozen=True)
class Snapshot:
    repository: str
    branch: str
    paths: Mapping[str, str]
    description: str
    topics: tuple[str, ...]
    truncated: bool

    def matches(self, patterns: Sequence[str]) -> list[str]:
        compiled = [re.compile(value, re.IGNORECASE) for value in patterns]
        return sorted(
            path for path in self.paths if any(rule.search(path) for rule in compiled)
        )


TARGETS = (
    Target("ravinperera/ravinperera", frozenset({"profile", "docs"}), "Portfolio profile and project map."),
    Target("ravinperera/ai-devops-guardrails", frozenset({"ai", "security", "docs", "actions", "code"}), "Operational guardrails for AI-assisted DevOps."),
    Target("ravinperera/ai-security-governance-checklist", frozenset({"ai", "security", "docs"}), "Practical AI security and governance controls."),
    Target("ravinperera/ai-token-efficiency-playbook", frozenset({"ai", "docs", "actions", "code"}), "Reproducible AI context-efficiency guidance and tools."),
    Target("ravinperera/aws-ecs-fargate-terraform-atmos", frozenset({"aws", "terraform", "actions"}), "ECS/Fargate reference pattern using Terraform and Atmos."),
    Target("ravinperera/aws-security-baseline-control-tower", frozenset({"aws", "terraform", "security", "actions"}), "AWS multi-account security baseline."),
    Target("ravinperera/github-actions-oidc-aws-deployment", frozenset({"aws", "actions", "security"}), "Secure GitHub-to-AWS OIDC deployment pattern."),
    Target("ravinperera/ecs-observability-otel-opensearch", frozenset({"aws", "observability", "terraform", "actions"}), "ECS telemetry and OpenSearch observability pattern."),
)

REFERENCES = (
    Reference("kubernetes/kubernetes", "ownership, governance, and security contacts"),
    Reference("hashicorp/terraform", "issue-first design, tests, and change discipline"),
    Reference("terraform-aws-modules/terraform-aws-vpc", "tested Terraform examples and pre-commit checks"),
    Reference("open-telemetry/opentelemetry-collector-contrib", "stability, support ownership, and change fragments"),
    Reference("github/docs", "structured issue routing and documentation quality"),
    Reference("actions/checkout", "architecture decisions and secure workflow defaults"),
    Reference("ossf/scorecard", "automated supply-chain security posture"),
    Reference("sigstore/cosign", "release integrity, provenance, and compatibility"),
    Reference("prometheus/prometheus", "operational documentation and release discipline"),
    Reference("argoproj/argo-cd", "GitOps operations, upgrades, and rollback guidance"),
)

PRACTICES = (
    Practice("security", "Private vulnerability reporting", "P0", "Security reports should not be disclosed through ordinary issues.", "Add a private vulnerability reporting policy", (r"^(?:\.github/|docs/)?security\.md$",), exclude=frozenset({"profile"})),
    Practice("ownership", "Path-aware review ownership", "P0", "Sensitive workflows, IAM, Terraform, and policies need explicit reviewers.", "Add CODEOWNERS and document review ownership", (r"^(?:\.github/)?codeowners$", r"(^|/)owners$"), exclude=frozenset({"profile"})),
    Practice("contributing", "Contributor and validation workflow", "P1", "A reproducible contribution path reduces review rework.", "Document contribution and local validation", (r"^(?:\.github/|docs/)?contributing\.md$",), exclude=frozenset({"profile"})),
    Practice("support", "Support and stability policy", "P1", "Users should know what is stable, experimental, deprecated, or best-effort.", "Document support and stability expectations", (r"^(?:docs/)?(?:support|stability|maintenance)[^/]*\.md$",), exclude=frozenset({"profile"})),
    Practice("issue-forms", "Structured issue forms", "P1", "Required fields produce more actionable reports.", "Add structured issue forms and routing", (r"^\.github/issue_template/[^/]+\.ya?ml$",), exclude=frozenset({"profile"})),
    Practice("pr-template", "PR evidence template", "P1", "Risky changes need scope, tests, evidence, rollback, and residual risk.", "Add or strengthen the PR evidence template", (r"^(?:\.github/)?pull_request_template\.md$", r"^\.github/pull_request_template/"), exclude=frozenset({"profile"})),
    Practice("changelog", "Changelog or change fragments", "P1", "Reusable projects need user-facing change history.", "Add a changelog or change-fragment workflow", (r"^(?:change|changes|changelog|history|news).*\.md$", r"^\.chloggen/", r"^\.changes/"), tags=frozenset({"ai", "terraform", "actions", "observability", "code"})),
    Practice("architecture", "Architecture and data-flow document", "P1", "Trust boundaries, identities, data paths, and failure modes should be explicit.", "Add architecture and data-flow documentation", (r"^(?:docs/)?architecture.*\.md$", r"^docs/architecture/", r"^docs/design/"), tags=frozenset({"ai", "security", "terraform", "actions", "observability"})),
    Practice("adrs", "Architecture decision records", "P1", "Durable decisions preserve alternatives and consequences.", "Introduce lightweight architecture decision records", (r"^(?:docs/)?adrs?/", r"^docs/decisions/", r"^docs/rfcs?/"), tags=frozenset({"ai", "security", "terraform", "actions", "observability"})),
    Practice("examples", "Runnable golden-path examples", "P0", "Examples should prove the smallest safe path and expected result.", "Add a runnable golden-path example", (r"^(?:examples?|samples?|use-cases?)/", r"^docs/examples?/"), exclude=frozenset({"profile"})),
    Practice("case-studies", "Evidence-backed case studies", "P1", "A portfolio is stronger when it shows constraints, decisions, validation, and outcomes.", "Add an evidence-backed project case study", (r"^docs/case-stud(?:y|ies)/",), tags=frozenset({"profile"})),
    Practice("tests", "Automated regression tests", "P0", "Scripts, policies, and configuration examples need executable regression coverage.", "Add automated regression tests", (r"^(?:tests?|__tests__)/", r"(^|/)[^/]+_test\.[^/]+$", r"(^|/)test_[^/]+\.[^/]+$"), tags=frozenset({"ai", "code", "terraform", "actions", "observability"})),
    Practice("terraform-tests", "Terraform native tests", "P0", "Plan assertions and mock providers can verify important behaviour without live AWS.", "Add credential-free Terraform native tests", (r"(^|/)[^/]+\.tftest\.(?:hcl|json)$",), tags=frozenset({"terraform"})),
    Practice("pre-commit", "Pre-commit quality gate", "P1", "Local formatting, linting, generated docs, and validation should match CI.", "Add a pre-commit quality gate", (r"^\.pre-commit-config\.ya?ml$",), tags=frozenset({"docs", "code", "terraform", "actions"})),
    Practice("terraform-quality", "TFLint and generated Terraform docs", "P1", "Linting and generated interfaces catch drift and improve reuse.", "Add TFLint and generated Terraform interface docs", (r"^\.tflint\.hcl$", r"^\.terraform-docs\.ya?ml$"), tags=frozenset({"terraform"})),
    Practice("ci", "Credential-free pull-request CI", "P0", "Every meaningful change should receive deterministic validation before merge.", "Add or strengthen credential-free PR CI", (r"^\.github/workflows/[^/]+\.ya?ml$",), exclude=frozenset({"profile"})),
    Practice("docs-lint", "Markdown and link validation", "P1", "Documentation-heavy projects need checks for broken links and formatting drift.", "Add Markdown and link validation", (r"^\.markdownlint", r"^\.github/workflows/[^/]*(?:markdown|docs|link|lychee)"), tags=frozenset({"docs", "ai", "profile"})),
    Practice("dependabot", "Controlled dependency updates", "P1", "Pinned Actions, providers, and packages still need a low-noise update path.", "Configure low-noise Dependabot updates", (r"^\.github/dependabot\.ya?ml$",), tags=frozenset({"code", "terraform", "actions"})),
    Practice("actions-lint", "GitHub Actions security linting", "P0", "Workflow-specific analysis catches unsafe expressions, permissions, and dependencies.", "Add actionlint and workflow security analysis", (r"^\.github/workflows/[^/]*(?:actionlint|zizmor|workflow-security)", r"^\.github/zizmor\.ya?ml$"), tags=frozenset({"actions"})),
    Practice("scorecard", "OpenSSF Scorecard", "P1", "A repeatable security-health audit exposes branch, review, dependency, and workflow gaps.", "Add OpenSSF Scorecard scanning", (r"^\.github/workflows/[^/]*scorecard",), tags=frozenset({"code", "terraform", "actions"})),
    Practice("secret-scan", "Secret scanning gate", "P1", "Examples and fixtures can accidentally contain realistic credentials.", "Add a secret scanning gate", (r"^\.github/workflows/[^/]*(?:gitleaks|trufflehog|secret)", r"^\.gitleaks\.toml$"), tags=frozenset({"ai", "security", "terraform", "actions", "observability"})),
    Practice("compatibility", "Tested compatibility matrix", "P1", "Consumers need supported version combinations and end-of-support boundaries.", "Add a tested compatibility matrix", (r"^(?:docs/)?compatibility.*\.md$", r"^(?:docs/)?supported-versions\.md$"), tags=frozenset({"ai", "code", "terraform", "actions", "observability"})),
    Practice("threat-model", "Repository-specific threat model", "P0", "Security-sensitive guidance should state assets, actors, trust boundaries, and residual risk.", "Add or expand the repository threat model", (r"^(?:docs/)?threat[-_]?model.*\.md$", r"^docs/security/threat"), tags=frozenset({"ai", "security", "actions", "observability"})),
    Practice("machine-controls", "Machine-readable controls or schemas", "P1", "Versioned YAML/JSON controls can be validated and reused beyond prose.", "Publish a versioned machine-readable control schema", (r"^(?:schemas?|controls?|policies?)/.*\.(?:json|ya?ml|rego)$", r"^schema\."), tags=frozenset({"ai", "security"})),
    Practice("ai-evals", "AI evaluation and regression corpus", "P0", "AI guidance needs positive, negative, adversarial, and false-positive cases.", "Add a reproducible AI evaluation corpus", (r"^(?:evals?|benchmarks?|test-cases?|fixtures?)/", r"^tests?/(?:evals?|fixtures?|cases?)/"), tags=frozenset({"ai"})),
    Practice("runbooks", "Operational runbooks and stop conditions", "P0", "Production guidance needs detection, triage, rollback, validation, and escalation.", "Add operational runbooks with stop conditions", (r"^(?:docs/)?runbooks?/", r"^docs/(?:incident|operations|rollback|troubleshooting)(?:/|[-_])"), tags=frozenset({"aws", "terraform", "actions", "observability"})),
    Practice("slos", "SLO, alert, and dashboard examples", "P1", "Observability guidance should include actionable objectives and signals.", "Add SLO, alert, and dashboard examples", (r"^(?:dashboards?|alerts?|slos?)/", r"^docs/(?:dashboards?|alerts?|slos?)/"), tags=frozenset({"observability"})),
    Practice("data-safety", "Sensitive-data and redaction tests", "P0", "AI, security, and telemetry examples should prove block or redact behaviour.", "Add sensitive-data and redaction regression tests", (r"^tests?/(?:security|redaction|privacy|sensitive-data)/",), tags=frozenset({"ai", "security", "observability"})),
    Practice("local-check", "Single local validation command", "P1", "One reproducible entry point makes contribution and CI behaviour clearer.", "Add a single local validation command", (r"^(?:makefile|justfile)$", r"^taskfile\.ya?ml$", r"^scripts/(?:check|validate|test).*(?:\.sh|\.py)$"), tags=frozenset({"docs", "code", "terraform", "actions"})),
)


class Client:
    def __init__(self, token: str | None) -> None:
        self.token = token
        self.requests = 0
        self.current = os.environ.get("GITHUB_REPOSITORY")
        self.in_actions = os.environ.get("GITHUB_ACTIONS", "").lower() == "true"

    def request(self, path: str, *, method: str = "GET", payload: Mapping[str, Any] | None = None, authenticate: bool = True) -> Any:
        url = path if path.startswith("https://") else API_ROOT + path
        data = json.dumps(payload).encode() if payload is not None else None
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "ravinperera-weekly-research/1.0", "X-GitHub-Api-Version": API_VERSION}
        if authenticate and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if data is not None:
            headers["Content-Type"] = "application/json"
        for attempt in range(4):
            try:
                self.requests += 1
                request = urllib.request.Request(url, data=data, method=method, headers=headers)
                with urllib.request.urlopen(request, timeout=45) as response:
                    raw = response.read()
                    return json.loads(raw.decode()) if raw else None
            except urllib.error.HTTPError as exc:
                body = exc.read().decode(errors="replace")
                if exc.code not in {403, 429, 500, 502, 503, 504} or attempt == 3:
                    raise RuntimeError(f"GitHub API {method} {url} failed ({exc.code}): {body[:300]}") from exc
                time.sleep(min(2**attempt, 15))
            except urllib.error.URLError as exc:
                if attempt == 3:
                    raise RuntimeError(f"GitHub API request failed: {url}: {exc}") from exc
                time.sleep(min(2**attempt, 15))
        raise AssertionError("unreachable")

    def snapshot(self, repository: str) -> Snapshot:
        encoded = urllib.parse.quote(repository, safe="/")
        authenticate = not self.in_actions or repository == self.current
        metadata = self.request(f"/repos/{encoded}", authenticate=authenticate)
        branch = str(metadata["default_branch"])
        tree = self.request(f"/repos/{encoded}/git/trees/{urllib.parse.quote(branch, safe='')}?recursive=1", authenticate=authenticate)
        paths = {str(item["path"]): str(item.get("type", "blob")) for item in tree.get("tree", ()) if item.get("path")}
        return Snapshot(repository, branch, paths, str(metadata.get("description") or ""), tuple(metadata.get("topics") or ()), bool(tree.get("truncated")))

    def upsert_issue(self, repository: str, body: str) -> str:
        encoded = urllib.parse.quote(repository, safe="/")
        issues = self.request(f"/repos/{encoded}/issues?state=open&per_page=100")
        existing = next((item for item in issues if "pull_request" not in item and item.get("title") == REPORT_TITLE), None)
        if existing:
            result = self.request(f"/repos/{encoded}/issues/{existing['number']}", method="PATCH", payload={"body": body})
        else:
            result = self.request(f"/repos/{encoded}/issues", method="POST", payload={"title": REPORT_TITLE, "body": body})
        return str(result["html_url"])


def file_url(snapshot: Snapshot, path: str) -> str:
    view = "tree" if snapshot.paths.get(path) == "tree" else "blob"
    encoded_path = "/".join(urllib.parse.quote(part, safe="") for part in path.split("/"))
    return f"https://github.com/{snapshot.repository}/{view}/{urllib.parse.quote(snapshot.branch, safe='')}/{encoded_path}"


def candidates(target: Target, snapshot: Snapshot, references: Sequence[tuple[Reference, Snapshot]]) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    for practice in PRACTICES:
        if not practice.applies(target) or snapshot.matches(practice.patterns):
            continue
        examples = []
        for reference, reference_snapshot in references:
            matches = reference_snapshot.matches(practice.patterns)
            if matches:
                examples.append((reference, reference_snapshot, matches[0]))
        relevance = len(practice.tags.intersection(target.tags))
        found.append({"practice": practice, "examples": examples, "sort": (-PRIORITY[practice.priority], -len(examples), -relevance, practice.title.lower())})
    if not snapshot.description.strip():
        practice = Practice("description", "Clear repository description", "P0", "Search and repository lists should explain the project in one sentence.", "Add a concise repository description", ())
        found.append({"practice": practice, "examples": [], "sort": (-3, 0, 0, practice.title)})
    if len(snapshot.topics) < 4:
        practice = Practice("topics", "Focused repository topics", "P2", "Relevant topics improve discovery and portfolio navigation.", "Add focused repository topics", ())
        found.append({"practice": practice, "examples": [], "sort": (-1, 0, 0, practice.title)})
    return sorted(found, key=lambda item: item["sort"])


def render(item: Mapping[str, Any], include_issue: bool = True) -> str:
    practice: Practice = item["practice"]
    examples = item["examples"]
    text = f"**{practice.priority} — {practice.title}.** {practice.why}"
    if examples:
        links = ", ".join(f"[`{reference.repository}`]({file_url(snapshot, path)})" for reference, snapshot, path in examples[:3])
        text += f" Observed in {len(examples)}/{len(REFERENCES)} references; examples: {links}."
    else:
        text += " Portfolio-specific signal; verify settings and existing prose before creating work."
    if include_issue:
        text += f" Suggested issue: `{practice.issue}`."
    return text


def build_report(target_snapshots: Mapping[str, Snapshot], reference_snapshots: Sequence[tuple[Reference, Snapshot]], max_per_repo: int) -> tuple[str, Mapping[str, Sequence[Mapping[str, Any]]]]:
    generated = dt.datetime.now(dt.timezone.utc)
    backlog = {target.repository: candidates(target, target_snapshots[target.repository], reference_snapshots) for target in TARGETS}
    lines = [
        f"# Weekly repository research — {generated.date().isoformat()}",
        "",
        "This is an evidence-based research backlog, **not an instruction to add every missing file**. Confirm fit, avoid duplicates, and prefer executable proof over repository decoration.",
        "",
        "## Cross-portfolio priorities",
        "",
    ]
    all_items = sorted(((repo, item) for repo, items in backlog.items() for item in items), key=lambda pair: (pair[1]["sort"], pair[0]))
    seen: set[str] = set()
    for repo, item in all_items:
        key = item["practice"].key
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"- `{repo}` — {render(item, include_issue=False)}")
        if len(seen) == 10:
            break
    lines += ["", "## Repository backlog", ""]
    for target in TARGETS:
        snapshot = target_snapshots[target.repository]
        lines += [f"### `{target.repository}`", "", target.purpose, ""]
        selected = backlog[target.repository][:max_per_repo]
        lines += [f"- {render(item)}" for item in selected] or ["- No high-confidence structural gap detected this week."]
        if snapshot.truncated:
            lines.append("- Audit warning: GitHub returned a truncated tree; existing files may have been missed.")
        lines.append("")
    lines += ["## References inspected", ""]
    lines += [f"- [`{reference.repository}`](https://github.com/{reference.repository}) — {reference.focus}." for reference, _ in reference_snapshots]
    lines += [
        "",
        "## Guardrails",
        "",
        "- Search for equivalent content under different filenames before opening an issue.",
        "- Prefer tests, examples, schemas, and operational evidence over another prose-only file.",
        "- Keep each implementation focused, validated, and rollback-aware.",
        "- Do not create empty commits, duplicate templates, unsupported claims, or changes intended only to increase activity.",
        "- Review branch rules, private reporting, push protection, and other repository settings manually.",
        "",
        f"_Generated at {generated.isoformat()} with GitHub REST API {API_VERSION}._",
    ]
    run_id = os.environ.get("GITHUB_RUN_ID")
    if run_id:
        lines.append(f"_Workflow run: {os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{os.environ.get('GITHUB_REPOSITORY')}/actions/runs/{run_id}_")
    return "\n".join(lines) + "\n", backlog


def summary(issue_url: str | None, backlog: Mapping[str, Sequence[Mapping[str, Any]]], requests: int) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not path:
        return
    lines = ["## Weekly repository research", "", f"- Candidate signals: {sum(map(len, backlog.values()))}", f"- API requests: {requests}"]
    if issue_url:
        lines.append(f"- Backlog issue: {issue_url}")
    with open(path, "a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-per-repo", type=int, default=5)
    args = parser.parse_args(argv or sys.argv[1:])
    if not 1 <= args.max_per_repo <= 10:
        parser.error("--max-per-repo must be between 1 and 10")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    client = Client(token)
    reference_snapshots: list[tuple[Reference, Snapshot]] = []
    warnings: list[str] = []
    for reference in REFERENCES:
        try:
            reference_snapshots.append((reference, client.snapshot(reference.repository)))
        except RuntimeError as exc:
            warnings.append(f"{reference.repository}: {exc}")
    if len(reference_snapshots) < 5:
        raise RuntimeError("Too few reference repositories could be inspected: " + "; ".join(warnings))
    target_snapshots = {target.repository: client.snapshot(target.repository) for target in TARGETS}
    report, backlog = build_report(target_snapshots, reference_snapshots, args.max_per_repo)
    if warnings:
        report += "\n## Reference fetch warnings\n\n" + "\n".join(f"- {warning}" for warning in warnings) + "\n"
    if args.dry_run:
        print(report)
        summary(None, backlog, client.requests)
        return 0
    if not token:
        raise RuntimeError("GH_TOKEN or GITHUB_TOKEN is required to update the backlog issue")
    report_repo = os.environ.get("REPORT_REPOSITORY", os.environ.get("GITHUB_REPOSITORY", "ravinperera/ravinperera"))
    issue_url = client.upsert_issue(report_repo, report)
    print(f"Weekly repository research backlog updated: {issue_url}")
    summary(issue_url, backlog, client.requests)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
