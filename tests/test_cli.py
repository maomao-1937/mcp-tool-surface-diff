import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "mcp_tool_surface_diff.py"


def run(document):
    return subprocess.run([sys.executable, str(SCRIPT)], input=document, text=True,
                          capture_output=True, cwd=ROOT, timeout=5)


class SurfaceDiffTests(unittest.TestCase):
    def test_exact_example(self):
        doc = '{"before":{"tools":[{"name":"lookup","description":"Find records.","inputSchema":{"type":"object"}}]},"after":{"tools":[{"name":"lookup","description":"Find records.","inputSchema":{"type":"object"}},{"name":"delete","description":"Delete one.","inputSchema":{"type":"object"}}]}}'
        result = run(doc)
        self.assertEqual(result.returncode, 0)
        digest = hashlib.sha256(b'{"description":"Delete one.","inputSchema":{"type":"object"},"name":"delete"}').hexdigest()
        expected = {"changed": True, "before_count": 1, "after_count": 2,
                    "counts": {"added": 1, "removed": 0, "changed": 0},
                    "changes": [{"tool": "delete", "change": "added", "after_sha256": digest}]}
        self.assertEqual(json.loads(result.stdout), expected)

    def test_schema_drift_reports_digest_only(self):
        result = run('{"before":{"tools":[{"name":"lookup","description":"private old text","inputSchema":{"type":"object"}}]},"after":{"tools":[{"name":"lookup","description":"private new text","inputSchema":{"type":"object"}}]}}')
        self.assertIn('"change":"changed"', result.stdout)
        self.assertNotIn("private old text", result.stdout)
        self.assertNotIn("private new text", result.stdout)

    def test_removed_tool(self):
        result = run('{"before":{"tools":[{"name":"old","inputSchema":{}}]},"after":{"tools":[]}}')
        self.assertIn('"change":"removed"', result.stdout)

    def test_same_snapshot_is_empty(self):
        result = run('{"before":{"tools":[]},"after":{"tools":[]}}')
        self.assertEqual(result.stdout, '{"after_count":0,"before_count":0,"changed":false,"changes":[],"counts":{"added":0,"changed":0,"removed":0}}\n')

    def test_duplicate_tool_names_rejected(self):
        result = run('{"before":{"tools":[{"name":"x"},{"name":"x"}]},"after":{"tools":[]}}')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '{"error":"duplicate_tool_name"}\n')

    def test_duplicate_json_key_rejected(self):
        result = run('{"before":{"tools":[]},"after":{"tools":[],"tools":[]}}')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '{"error":"duplicate_json_key"}\n')

    def test_non_finite_json_rejected(self):
        result = run('{"before":{"tools":[{"name":"x","score":NaN}]},"after":{"tools":[]}}')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '{"error":"non_finite_number"}\n')

    def test_overflow_float_rejected(self):
        result = run('{"before":{"tools":[{"name":"x","score":1e400}]},"after":{"tools":[]}}')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '{"error":"non_finite_number"}\n')

    def test_size_cap(self):
        result = run(' ' * (512 * 1024 + 1))
        self.assertEqual(result.stdout, '{"error":"input_too_large"}\n')


if __name__ == "__main__":
    unittest.main()
