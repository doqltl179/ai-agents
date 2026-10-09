"""Tests for tools/agentkit.py. Run: python -m unittest discover -s tools/tests -v"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))

import agentkit  # noqa: E402


def run(script: Path, *args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(script), *args], cwd=cwd, capture_output=True,
                          text=True, encoding="utf-8")


class FrontmatterTests(unittest.TestCase):
    def test_scalars_lists_and_quotes(self) -> None:
        text = ('---\nname: demo\ndescription: "Does X: then Y. Use when Z."\n'
                'tags: [a, "b, c", \'d\']\nitems:\n  - one\n  - "two"\nempty: []\n---\n# Body\n')
        meta, body = agentkit.parse_frontmatter(text)
        self.assertEqual(meta["name"], "demo")
        self.assertEqual(meta["description"], "Does X: then Y. Use when Z.")
        self.assertEqual(meta["tags"], ["a", "b, c", "d"])
        self.assertEqual(meta["items"], ["one", "two"])
        self.assertEqual(meta["empty"], [])
        self.assertEqual(body, "# Body\n")

    def test_no_frontmatter(self) -> None:
        meta, body = agentkit.parse_frontmatter("# Title\n")
        self.assertIsNone(meta)
        self.assertEqual(body, "# Title\n")


class LinkTests(unittest.TestCase):
    def test_rewrite_to_project_root(self) -> None:
        project = Path("/p")
        src = project / ".ai" / "kit" / "core" / "wiki" / "x"
        out = agentkit.rewrite_links("See [a](../y/a.md#part) and [web](https://e.com).", src, project)
        self.assertEqual(out, "See [a](.ai/kit/core/wiki/y/a.md#part) and [web](https://e.com).")

    def test_keep_links_inside_skill_folder_relative(self) -> None:
        project = Path("/p")
        src = project / ".ai" / "kit" / "core" / "skills" / "s"
        dest = project / ".claude" / "skills" / "s"
        out = agentkit.rewrite_links("[c](checklist.md) [w](../../wiki/a.md)", src, project, dest, src)
        self.assertEqual(out, "[c](checklist.md) [w](.ai/kit/core/wiki/a.md)")

    def test_fenced_code_untouched(self) -> None:
        text = "```\n[a](b.md)\n```"
        self.assertEqual(agentkit.rewrite_links(text, Path("/p/x"), Path("/p")), text)


class GlobTests(unittest.TestCase):
    def test_double_star(self) -> None:
        regex = agentkit.glob_re("core/wiki/**/*.md")
        self.assertTrue(regex.match("core/wiki/a.md"))
        self.assertTrue(regex.match("core/wiki/s/a.md"))
        self.assertFalse(regex.match("core/agents/a.md"))
        self.assertFalse(agentkit.glob_re("core/*.md").match("core/wiki/a.md"))


class ReleaseTagTests(unittest.TestCase):
    def test_picks_highest_semver_tag(self) -> None:
        output = ("a1\trefs/tags/v0.9.0\nb2\trefs/tags/v0.10.0\nc3\trefs/tags/v0.2.1\n"
                  "d4\trefs/tags/nightly\ne5\trefs/tags/v1.0.0-rc.1\n")
        self.assertEqual(agentkit.latest_release_tag(output), "v0.10.0")

    def test_no_release_tag(self) -> None:
        self.assertIsNone(agentkit.latest_release_tag("a1\trefs/tags/nightly\n"))
        self.assertIsNone(agentkit.latest_release_tag(""))


class CapacityTests(unittest.TestCase):
    CLASSES = [("light", 0.5, 1.0), ("standard", 2.0, 0.5), ("heavy", 6.0, 0.25)]

    def test_small_machine_is_limited_by_memory(self) -> None:
        reserve, result = agentkit.recommend_concurrency(8, 4, 8, self.CLASSES, 0.25, 2, 0)
        self.assertEqual(reserve, 2)
        self.assertEqual(result["light"], (4, "memory", False))
        self.assertEqual(result["standard"], (1, "memory", False))
        self.assertEqual(result["heavy"], (1, "memory", True))

    def test_policy_cap_and_unknown_memory(self) -> None:
        _, capped = agentkit.recommend_concurrency(64, 40, 16, self.CLASSES, 0.25, 2, 2)
        self.assertEqual(capped["light"], (2, "policy.max_parallel_units", False))
        reserve, unknown = agentkit.recommend_concurrency(None, None, 4, self.CLASSES, 0.25, 2, 0)
        self.assertIsNone(reserve)
        self.assertEqual(unknown["heavy"], (1, "CPU", False))

    def test_capacity_command_runs(self) -> None:
        result = run(TOOLS / "agentkit.py", "capacity", cwd=agentkit.KIT_ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("recommended concurrent units", result.stdout)


class KitRepositoryTests(unittest.TestCase):
    def test_kit_repository_is_consistent(self) -> None:
        result = run(TOOLS / "agentkit.py", "check", cwd=agentkit.KIT_ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class InstallTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name) / "demo"
        self.project.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=self.project, check=True)
        self.script = self.project / ".ai" / "kit" / "tools" / "agentkit.py"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def install(self, tools: str = "claude,codex,copilot,cursor,gemini") -> subprocess.CompletedProcess[str]:
        return run(TOOLS / "agentkit.py", "install", str(self.project), "--tools", tools, cwd=self.project)

    def bind(self) -> None:
        profile = self.project / ".ai" / "project" / "profile.toml"
        text = profile.read_text(encoding="utf-8")
        text += ('\n[agents]\nenabled = ["@governance", "@quality", "@documentation", "@release", "web-frontend-engineer"]\n'
                 '\n[bindings.web-frontend-engineer]\npaths = ["web/**"]\nstacks = ["typescript", "react"]\n')
        profile.write_text(text, encoding="utf-8")

    def test_install_sync_and_check(self) -> None:
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.bind()
        self.assertEqual(run(self.script, "sync", cwd=self.project).returncode, 0)
        check = run(self.script, "check", cwd=self.project)
        self.assertEqual(check.returncode, 0, check.stdout)
        for relpath in ["AGENTS.md", "CLAUDE.md", "GEMINI.md", ".github/copilot-instructions.md",
                        ".claude/agents/web-frontend-engineer.md", ".github/agents/web-frontend-engineer.agent.md",
                        ".codex/agents/web-frontend-engineer.toml", ".claude/skills/git-commit/SKILL.md",
                        ".agents/skills/git-commit/SKILL.md", ".claude/rules/stack-typescript.md",
                        ".github/instructions/stack-react.instructions.md", ".cursor/rules/stack-react.mdc",
                        ".ai/generated/catalog.md", ".ai/project/profile.toml", ".ai/project/wiki/glossary.md",
                        ".claude/skills/translate/SKILL.md"]:
            self.assertTrue((self.project / relpath).exists(), relpath)
        self.assertFalse((self.project / ".github" / "skills").exists(), "copilot skills duplicate claude/codex skills")
        agent = (self.project / ".claude" / "agents" / "web-frontend-engineer.md").read_text(encoding="utf-8")
        self.assertIn("`web/**`", agent)
        self.assertIn(".ai/kit/core/stacks/frameworks/react.md", agent)
        reviewer = (self.project / ".claude" / "agents" / "code-reviewer.md").read_text(encoding="utf-8")
        self.assertIn("disallowedTools:", reviewer)
        gitignore = (self.project / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".ai/tasks/", gitignore)
        self.assertIn(".worktrees/", gitignore)
        self.assertIn("| `policy.integration_branch` | develop |",
                      (self.project / "AGENTS.md").read_text(encoding="utf-8"))
        import tomllib
        tomllib.loads((self.project / ".codex" / "agents" / "code-reviewer.toml").read_text(encoding="utf-8"))

    def test_drift_and_local_kit_edits_fail_check(self) -> None:
        self.install()
        agents_md = self.project / "AGENTS.md"
        agents_md.write_text(agents_md.read_text(encoding="utf-8") + "\nlocal edit\n", encoding="utf-8")
        self.assertEqual(run(self.script, "check", cwd=self.project).returncode, 1)
        run(self.script, "sync", cwd=self.project)
        self.assertEqual(run(self.script, "check", cwd=self.project).returncode, 0)
        start = self.project / ".ai" / "kit" / "core" / "START.md"
        start.write_text(start.read_text(encoding="utf-8") + "\nlocal edit\n", encoding="utf-8")
        result = run(self.script, "check", cwd=self.project)
        self.assertEqual(result.returncode, 1)
        self.assertIn("kit file edited locally", result.stdout)

    def test_refuses_to_overwrite_hand_written_entry(self) -> None:
        (self.project / "AGENTS.md").write_text("# Hand-written rules\n", encoding="utf-8")
        result = self.install()
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("installed, adoption needed", result.stdout)
        self.assertEqual((self.project / "AGENTS.md").read_text(encoding="utf-8"), "# Hand-written rules\n")

    def test_minimal_profile_takes_defaults(self) -> None:
        self.install()
        profile = (self.project / ".ai" / "project" / "profile.toml").read_text(encoding="utf-8")
        self.assertNotIn("[policy]", profile)
        self.assertIn('name = "demo"', profile)
        self.assertIn("| `policy.integration_branch` | develop |", (self.project / "AGENTS.md").read_text(encoding="utf-8"))
        path = self.project / ".ai" / "project" / "profile.toml"
        path.write_text(profile + '\n[policy]\nintegration_branch = "develop"\n', encoding="utf-8")
        self.assertIn("profile repeats 1 kit default(s): policy.integration_branch", run(self.script, "check", cwd=self.project).stdout)

    def test_unmanaged_instruction_files_are_reported(self) -> None:
        self.install()
        for relpath in (".github/prompts/old.prompt.md", ".claude/commands/legacy.md", "docs/AGENTS.md"):
            (self.project / relpath).parent.mkdir(parents=True, exist_ok=True)
            (self.project / relpath).write_text("old rules\n", encoding="utf-8")
        out = run(self.script, "check", cwd=self.project).stdout
        for relpath in (".github/prompts/old.prompt.md", ".claude/commands/legacy.md", "docs/AGENTS.md"):
            self.assertIn(f"unmanaged instruction file {relpath}", out)
        self.assertNotIn("unmanaged instruction file .claude/agents/", out)
        path = self.project / ".ai" / "project" / "profile.toml"
        path.write_text(path.read_text(encoding="utf-8") + '\n[tools]\nkeep_unmanaged = [".claude/commands/**"]\n', encoding="utf-8")
        self.assertNotIn(".claude/commands/legacy.md", run(self.script, "check", cwd=self.project).stdout)

    def test_byte_order_marks_are_tolerated(self) -> None:
        (self.project / ".editorconfig").write_text("root = true\n\n[*.md]\ncharset = utf-8-bom\n", encoding="utf-8")
        self.install()
        self.assertIn("# agentkit:", (self.project / ".editorconfig").read_text(encoding="utf-8"))
        page = self.project / ".ai" / "project" / "wiki" / "README.md"
        page.write_bytes(b"\xef\xbb\xbf" + page.read_bytes())
        result = run(self.script, "check", cwd=self.project)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("missing frontmatter", result.stdout)
        self.assertNotIn(".editorconfig forces utf-8-bom", result.stdout)

    def test_stale_generated_files_are_removed(self) -> None:
        self.install()
        self.bind()
        run(self.script, "sync", cwd=self.project)
        self.assertTrue((self.project / ".claude" / "agents" / "web-frontend-engineer.md").exists())
        profile = self.project / ".ai" / "project" / "profile.toml"
        profile.write_text(profile.read_text(encoding="utf-8").replace(', "web-frontend-engineer"]', "]")
                           .split("[bindings.web-frontend-engineer]")[0], encoding="utf-8")
        run(self.script, "sync", cwd=self.project)
        self.assertFalse((self.project / ".claude" / "agents" / "web-frontend-engineer.md").exists())
        self.assertEqual(run(self.script, "check", cwd=self.project).returncode, 0)

    def test_update_from_local_checkout(self) -> None:
        self.install()
        refused = run(self.script, "update", "--from", str(agentkit.KIT_ROOT), "--ref", "main", cwd=self.project)
        self.assertEqual(refused.returncode, 1)
        self.assertIn("--ref applies to a git URL", refused.stdout)
        result = run(self.script, "update", "--from", str(agentkit.KIT_ROOT), cwd=self.project)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("kit updated", result.stdout)
        self.assertEqual(run(self.script, "check", cwd=self.project).returncode, 0)

    def test_new_scaffolds_into_overlay(self) -> None:
        self.install()
        result = run(self.script, "new", "agent", "editor-tools", "--extends", "game-tools-engineer", cwd=self.project)
        self.assertEqual(result.returncode, 0, result.stdout)
        card = (self.project / ".ai" / "project" / "agents" / "editor-tools.md").read_text(encoding="utf-8")
        self.assertIn("extends: game-tools-engineer", card)
        self.assertIn("department: client", card)
        self.assertEqual(run(self.script, "new", "plan", "demo-task", cwd=self.project).returncode, 0)
        self.assertEqual(len(list((self.project / ".ai" / "tasks").glob("*-demo-task.md"))), 1)
        refused = run(self.script, "new", "page", "x", "--core", cwd=self.project)
        self.assertEqual(refused.returncode, 1)


if __name__ == "__main__":
    unittest.main()
