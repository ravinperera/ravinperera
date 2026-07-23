from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from typing import Any

MODULE_PATH = Path(__file__).with_name("weekly_repository_research.py")
SPEC = importlib.util.spec_from_file_location("weekly_repository_research", MODULE_PATH)
assert SPEC and SPEC.loader
research = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = research
SPEC.loader.exec_module(research)


class RepositoryResearchTests(unittest.TestCase):
    def snapshot(
        self,
        repository: str,
        paths: dict[str, str] | None = None,
        *,
        description: str = "Useful repository",
        topics: tuple[str, ...] = ("aws", "terraform", "devops", "security"),
    ) -> Any:
        return research.Snapshot(
            repository=repository,
            branch="main",
            paths=paths or {},
            description=description,
            topics=topics,
            truncated=False,
        )

    def test_path_matching_is_case_insensitive_and_recursive(self) -> None:
        snapshot = self.snapshot(
            "example/repo",
            {
                "README.md": "blob",
                ".github/SECURITY.md": "blob",
                "docs/architecture/README.md": "blob",
            },
        )
        self.assertEqual(
            snapshot.matches((r"^(?:\.github/|docs/)?security\.md$",)),
            [".github/SECURITY.md"],
        )
        self.assertEqual(
            snapshot.matches((r"^docs/architecture/",)),
            ["docs/architecture/README.md"],
        )

    def test_tag_filters_prevent_irrelevant_recommendations(self) -> None:
        terraform = research.Target(
            "example/terraform", frozenset({"terraform", "actions"}), "Terraform"
        )
        profile = research.Target(
            "example/profile", frozenset({"profile", "docs"}), "Profile"
        )
        native_tests = next(
            item for item in research.PRACTICES if item.key == "terraform-tests"
        )
        security = next(item for item in research.PRACTICES if item.key == "security")
        self.assertTrue(native_tests.applies(terraform))
        self.assertFalse(native_tests.applies(profile))
        self.assertFalse(security.applies(profile))

    def test_existing_practices_are_not_recommended(self) -> None:
        target = research.Target(
            "example/repo", frozenset({"terraform", "actions"}), "Example"
        )
        snapshot = self.snapshot(
            target.repository,
            {
                "SECURITY.md": "blob",
                ".github/CODEOWNERS": "blob",
                "CONTRIBUTING.md": "blob",
                "examples/main.tf": "blob",
                "tests/basic.tftest.hcl": "blob",
                ".github/workflows/validate.yml": "blob",
            },
        )
        keys = {
            item["practice"].key
            for item in research.candidates(target, snapshot, ())
        }
        for existing in (
            "security",
            "ownership",
            "contributing",
            "examples",
            "terraform-tests",
            "ci",
        ):
            self.assertNotIn(existing, keys)

    def test_issue_chooser_config_is_not_treated_as_an_issue_form(self) -> None:
        target = research.Target(
            "example/docs", frozenset({"ai", "security", "docs"}), "Docs"
        )
        snapshot = self.snapshot(
            target.repository, {".github/ISSUE_TEMPLATE/config.yml": "blob"}
        )
        keys = {
            item["practice"].key
            for item in research.candidates(target, snapshot, ())
        }
        self.assertIn("issue-forms", keys)

    def test_reference_adoption_is_included_as_evidence(self) -> None:
        target = research.Target(
            "example/ai", frozenset({"ai", "security", "docs"}), "AI example"
        )
        reference = research.Reference("famous/repo", "testing")
        reference_snapshot = self.snapshot(
            reference.repository, {"evals/prompt-injection.json": "blob"}
        )
        items = research.candidates(
            target,
            self.snapshot(target.repository),
            ((reference, reference_snapshot),),
        )
        evaluation = next(
            item for item in items if item["practice"].key == "ai-evals"
        )
        self.assertEqual(len(evaluation["examples"]), 1)
        rendered = research.render(evaluation)
        self.assertIn("famous/repo", rendered)
        self.assertIn("Suggested issue", rendered)

    def test_actions_token_is_not_sent_to_other_public_repositories(self) -> None:
        class RecordingClient(research.Client):
            def __init__(self) -> None:
                super().__init__("token")
                self.current = "ravinperera/ravinperera"
                self.in_actions = True
                self.auth: list[bool] = []

            def request(self, path: str, **kwargs: Any) -> Any:
                self.auth.append(bool(kwargs.get("authenticate", True)))
                if "/git/trees/" in path:
                    return {"tree": [], "truncated": False}
                return {
                    "default_branch": "main",
                    "description": "",
                    "topics": [],
                }

        client = RecordingClient()
        client.snapshot("kubernetes/kubernetes")
        self.assertEqual(client.auth, [False, False])
        client.auth.clear()
        client.snapshot("ravinperera/ravinperera")
        self.assertEqual(client.auth, [True, True])


if __name__ == "__main__":
    unittest.main()
