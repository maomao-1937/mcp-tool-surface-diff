# mcp-tool-surface-diff

Compare two captured MCP tools/list snapshots and identify tool additions, removals, or contract changes using hashes.

For MCP maintainers diagnosing changes between tool listings captured before and after a deployment or server update.

## Quick start

Requires Python 3.11 or newer. There are no third-party dependencies. The CLI reads one JSON document from standard input and writes one deterministic JSON line.

```console
python mcp_tool_surface_diff.py < examples/input.json
```

Output:

```json
{"after_count":2,"before_count":1,"changed":true,"changes":[{"after_sha256":"7dda98f8726509478a778725fc4f8e76345bc48ee4893b1801d20a5ecbcae42b","change":"added","tool":"delete"}],"counts":{"added":1,"changed":0,"removed":0}}
```

To run the tests and the exact example check:

```console
python -m unittest discover -s tests -v
python examples/run_examples.py
```

Inputs are limited to 512 KiB; malformed, duplicate-key, or over-depth JSON fails with a fixed error code. Output avoids echoing schema descriptions and values; issue pointers can include schema object keys. No MCP server is started or contacted.

## Problem evidence and scope

The official MCP Python SDK troubleshooting guide describes clients that can keep a stale tool listing when they do not handle notifications/tools/list_changed. This tool compares two snapshots; it does not observe live notifications.

This evidence describes specific reports and documented behavior. It does not establish how often the problem occurs or predict GitHub stars.

## Limits

Reports exact-name additions/removals and byte-stable canonical JSON changes. It does not infer semantic equivalence, monitor servers, or verify notification delivery. Tool names are included in output; schema bodies are not.

## License and attribution

MIT. This repository contains original code and synthetic fixtures; no upstream source code or assets are included.

## Verified environment

Python 3.11.15 on Windows and GitHub Actions on Ubuntu and Windows using Python 3.11.
