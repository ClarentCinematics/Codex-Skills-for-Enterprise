from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import install_skill
import scan_skill_security
import validate_skills


class RepositoryRegressionTests(unittest.TestCase):
    def test_installer_copies_helper_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary)
            install_skill.install_skill("ci-failure-triage", destination, force=False, dry_run=False)
            self.assertTrue((destination / "ci-failure-triage" / "scripts" / "extract_ci_signal.py").is_file())

    def test_registry_rejects_missing_trust_field(self) -> None:
        registry = json.loads((ROOT / "skill-registry.json").read_text(encoding="utf-8"))
        del registry["skills"][0]["owner"]
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8") as handle:
            json.dump(registry, handle)
            handle.flush()
            with mock.patch.object(validate_skills, "REGISTRY_FILE", Path(handle.name)):
                errors = validate_skills.validate_registry(sorted((ROOT / "skills").iterdir()))
        self.assertTrue(any("missing key(s): owner" in error for error in errors))

    def test_catalog_drift_is_detected(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8") as handle:
            handle.write("# stale catalog\n")
            handle.flush()
            with mock.patch.object(validate_skills, "CATALOG_FILE", Path(handle.name)):
                errors = validate_skills.validate_catalog()
        self.assertIn("docs/catalog.md is out of date; run python3 scripts/generate_catalog.py", errors)

    def test_malformed_plugin_manifest_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin_file = root / "plugin.json"
            marketplace_file = root / "marketplace.json"
            plugin_file.write_text('{"name": "wrong"}', encoding="utf-8")
            shutil.copy2(ROOT / ".agents" / "plugins" / "marketplace.json", marketplace_file)
            with (
                mock.patch.object(validate_skills, "PLUGIN_FILE", plugin_file),
                mock.patch.object(validate_skills, "MARKETPLACE_FILE", marketplace_file),
            ):
                errors = validate_skills.validate_plugin_metadata()
        self.assertTrue(any("plugin manifest missing key" in error for error in errors))

    def test_security_scan_rejects_process_and_file_writes(self) -> None:
        source = (
            "import os\nimport subprocess\n"
            "from pathlib import Path\n"
            "subprocess.run(['echo', 'x'])\n"
            "Path('x').open('w')\n"
            "value = os.environ['TOKEN']\n"
        )
        with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
            handle.write(source)
            handle.flush()
            errors = scan_skill_security.scan_script(
                Path(handle.name),
                {"network_access": "none", "filesystem_effects": "read-input-only"},
            )
        self.assertTrue(any("subprocess execution" in error for error in errors))
        self.assertTrue(any("undeclared writable open mode" in error for error in errors))
        self.assertTrue(any("credential/environment access" in error for error in errors))

    def test_eval_validator_rejects_malformed_json(self) -> None:
        spec = importlib.util.spec_from_file_location("validate_evals_for_test", ROOT / "scripts" / "validate_evals.py")
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8") as handle:
            handle.write("{")
            handle.flush()
            data, errors = module.load_json(Path(handle.name), "temporary eval")
        self.assertIsNone(data)
        self.assertTrue(any("invalid temporary eval" in error for error in errors))

    def test_eval_validator_detects_prompt_collisions(self) -> None:
        spec = importlib.util.spec_from_file_location("validate_evals_collision_test", ROOT / "scripts" / "validate_evals.py")
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        duplicates = module.duplicate_prompts(["Review this artifact", "  review   this artifact  ", "Different prompt"])
        self.assertEqual(duplicates, ["review this artifact"])


if __name__ == "__main__":
    unittest.main()
