from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HelperCliTests(unittest.TestCase):
    CASES = [
        {
            "name": "ci",
            "script": "skills/ci-failure-triage/scripts/extract_ci_signal.py",
            "suffix": ".log",
            "content": "+ pytest\nFAIL test_checkout.py\nAssertionError: expected 200 actual 500\ntoken=super-secret-value\n",
            "args": [],
            "title": "CI Failure Signal",
            "json_key": "primary_failure_signal",
        },
        {
            "name": "crm",
            "script": "skills/crm-hygiene-auditor/scripts/audit_crm_csv.py",
            "suffix": ".csv",
            "content": (
                "id,account,owner,stage,next_step,close_date,last_activity_date,forecast_category\n"
                "1,Acme,,Proposal,,2026-06-30,2026-05-01,Commit\n"
            ),
            "args": ["--today", "2026-06-12"],
            "title": "CRM Hygiene Audit",
            "json_key": "missing_fields",
        },
        {
            "name": "data",
            "script": "skills/data-quality-triage/scripts/audit_data_quality.py",
            "suffix": ".csv",
            "content": "id,status,last_updated\n1,Active,2026-01-01\n1,active,not-a-date\n",
            "args": ["--key-fields", "id", "--date-fields", "last_updated", "--today", "2026-06-12"],
            "title": "Data Quality Audit",
            "json_key": "duplicate_keys",
        },
        {
            "name": "incident",
            "script": "skills/incident-postmortem-assistant/scripts/check_incident_timeline.py",
            "suffix": ".md",
            "content": "10:02 Alert fired. Owner: On-call. Action: triage started.\n10:02 TODO confirm impact.\n",
            "args": [],
            "title": "Incident Timeline Check",
            "json_key": "repeated_timestamps",
        },
        {
            "name": "kb",
            "script": "skills/knowledge-base-capture/scripts/check_kb_metadata.py",
            "suffix": ".md",
            "content": "# Reset Billing Sync\nAudience: Support\nSummary: Restart steps.\nOwner: TBD\nReview Date: 2026-01-01\n",
            "args": ["--today", "2026-06-12"],
            "title": "KB Metadata Check",
            "json_key": "publishing_readiness",
        },
        {
            "name": "requirements",
            "script": "skills/requirements-to-acceptance-criteria/scripts/check_requirements_spec.py",
            "suffix": ".md",
            "content": "# Export Feature\n\n## Requirements\n\nUsers can export records.\n\nTBD: acceptance criteria.\n",
            "args": [],
            "title": "Requirements Spec Check",
            "json_key": "missing_sections",
        },
        {
            "name": "support",
            "script": "skills/support-deflection-miner/scripts/mine_support_themes.py",
            "suffix": ".txt",
            "content": "Billing sync reset missing\nBilling sync reset missing\nSSO login loop\n",
            "args": [],
            "title": "Support Deflection Theme Mining",
            "json_key": "top_repeated_issues",
        },
        {
            "name": "vendor",
            "script": "skills/vendor-security-review/scripts/check_vendor_security_answers.py",
            "suffix": ".md",
            "content": "# Vendor\nSOC 2 Type II available.\nEncryption at rest is stated.\nDPA: TBD.\n",
            "args": [],
            "title": "Vendor Security Coverage Check",
            "json_key": "missing_topics",
        },
    ]

    def run_helper(self, case: dict[str, object], content: str, *, json_mode: bool) -> subprocess.CompletedProcess[str]:
        with tempfile.NamedTemporaryFile("w", suffix=str(case["suffix"]), encoding="utf-8", delete=False) as handle:
            handle.write(content)
            input_path = Path(handle.name)
        try:
            command = ["python3", str(ROOT / str(case["script"])), "--input", str(input_path)]
            command.extend(str(value) for value in case["args"])
            if json_mode:
                command.append("--json")
            return subprocess.run(command, text=True, capture_output=True, check=False)
        finally:
            input_path.unlink(missing_ok=True)

    def test_human_and_json_interfaces(self) -> None:
        for case in self.CASES:
            with self.subTest(helper=case["name"], mode="human"):
                human = self.run_helper(case, str(case["content"]), json_mode=False)
                self.assertEqual(human.returncode, 0, human.stderr)
                self.assertIn(str(case["title"]), human.stdout)
            with self.subTest(helper=case["name"], mode="json"):
                first = self.run_helper(case, str(case["content"]), json_mode=True)
                second = self.run_helper(case, str(case["content"]), json_mode=True)
                self.assertEqual(first.returncode, 0, first.stderr)
                self.assertEqual(first.stdout, second.stdout)
                parsed = json.loads(first.stdout)
                self.assertIn(str(case["json_key"]), parsed)
                self.assertIn("caveats", parsed)

    def test_empty_inputs_do_not_crash(self) -> None:
        for case in self.CASES:
            with self.subTest(helper=case["name"]):
                completed = self.run_helper(case, "", json_mode=True)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertIsInstance(json.loads(completed.stdout), dict)

    def test_missing_input_file_fails(self) -> None:
        for case in self.CASES:
            with self.subTest(helper=case["name"]):
                command = [
                    "python3",
                    str(ROOT / str(case["script"])),
                    "--input",
                    "/tmp/cse-definitely-missing-input",
                ]
                completed = subprocess.run(command, text=True, capture_output=True, check=False)
                self.assertNotEqual(completed.returncode, 0)

    def test_ci_output_redacts_secret_like_values(self) -> None:
        case = self.CASES[0]
        completed = self.run_helper(case, str(case["content"]), json_mode=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotIn("super-secret-value", completed.stdout)
        self.assertIn("[REDACTED]", completed.stdout)

    def test_invalid_date_arguments_fail(self) -> None:
        date_cases = [self.CASES[1], self.CASES[2], self.CASES[4]]
        for case in date_cases:
            with tempfile.NamedTemporaryFile("w", suffix=str(case["suffix"]), encoding="utf-8", delete=False) as handle:
                handle.write(str(case["content"]))
                input_path = Path(handle.name)
            try:
                command = [
                    "python3",
                    str(ROOT / str(case["script"])),
                    "--input",
                    str(input_path),
                    "--today",
                    "not-a-date",
                ]
                completed = subprocess.run(command, text=True, capture_output=True, check=False)
                self.assertNotEqual(completed.returncode, 0)
            finally:
                input_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
