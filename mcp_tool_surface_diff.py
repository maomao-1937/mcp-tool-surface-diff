#!/usr/bin/env python3
"""Compare captured MCP tools/list surfaces without echoing schema bodies."""
import hashlib
import json
import math
import sys

MAX_BYTES = 512 * 1024
MAX_DEPTH = 64
MAX_TOOLS = 2048


class InputError(Exception):
    pass


def unique_pairs(pairs):
    value = {}
    for key, child in pairs:
        if key in value:
            raise InputError("duplicate_json_key")
        value[key] = child
    return value


def finite_float(raw):
    value = float(raw)
    if not math.isfinite(value):
        raise InputError("non_finite_number")
    return value


def check_depth(value, depth=0):
    if depth > MAX_DEPTH:
        raise InputError("maximum_depth_exceeded")
    if isinstance(value, dict):
        for child in value.values():
            check_depth(child, depth + 1)
    elif isinstance(value, list):
        for child in value:
            check_depth(child, depth + 1)


def index(snapshot):
    if not isinstance(snapshot, dict) or set(snapshot) != {"tools"}:
        raise InputError("snapshot_keys_must_be_tools")
    tools = snapshot["tools"]
    if not isinstance(tools, list) or len(tools) > MAX_TOOLS:
        raise InputError("tools_must_be_bounded_array")
    output = {}
    for tool in tools:
        if not isinstance(tool, dict) or not isinstance(tool.get("name"), str) or not tool["name"]:
            raise InputError("tool_name_invalid")
        if tool["name"] in output:
            raise InputError("duplicate_tool_name")
        canonical = json.dumps(tool, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
        output[tool["name"]] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return output


def compare(document):
    if not isinstance(document, dict) or set(document) != {"before", "after"}:
        raise InputError("top_level_keys_must_be_before_after")
    before = index(document["before"])
    after = index(document["after"])
    changes = []
    for name in sorted(before.keys() | after.keys()):
        if name not in before:
            changes.append({"tool": name, "change": "added", "after_sha256": after[name]})
        elif name not in after:
            changes.append({"tool": name, "change": "removed", "before_sha256": before[name]})
        elif before[name] != after[name]:
            changes.append({"tool": name, "change": "changed", "before_sha256": before[name], "after_sha256": after[name]})
    counts = {kind: sum(row["change"] == kind for row in changes) for kind in ("added", "removed", "changed")}
    return {"changed": bool(changes), "before_count": len(before), "after_count": len(after),
            "counts": counts, "changes": changes}


def fail(code):
    sys.stdout.write(json.dumps({"error": code}, sort_keys=True, separators=(",", ":")) + "\n")
    return 2


def main():
    if sys.argv[1:] in (["--help"], ["-h"]):
        print("usage: mcp_tool_surface_diff.py < before-after.json")
        return 0
    if sys.argv[1:]:
        return fail("arguments_not_supported")
    raw = sys.stdin.buffer.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        return fail("input_too_large")
    try:
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs,
                              parse_constant=lambda _: (_ for _ in ()).throw(InputError("non_finite_number")),
                              parse_float=finite_float)
        check_depth(document)
        result = compare(document)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return fail("invalid_json")
    except InputError as exc:
        return fail(str(exc))
    except RecursionError:
        return fail("maximum_depth_exceeded")
    sys.stdout.write(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
