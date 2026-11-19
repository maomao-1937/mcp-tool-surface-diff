# Testing: mcp-tool-surface-diff

- Runtime: Python 3.11.15, Windows.
- Dependencies: Python standard library only.
- Commands: `python -m unittest discover -s tests -v`; `python examples/run_examples.py`.
- GitHub Actions matrix: Ubuntu and Windows, Python 3.11.
- Input size/depth, duplicate keys, malformed values, output redaction and exit codes are covered by unit tests.

The tests validate the documented input profile and CLI behavior. They do not connect to an MCP server or assert universal behavior across clients.
