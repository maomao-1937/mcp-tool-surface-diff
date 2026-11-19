# Research notes: mcp-tool-surface-diff

## Observed source facts

The official MCP Python SDK troubleshooting guide describes clients that can keep a stale tool listing when they do not handle notifications/tools/list_changed. This tool compares two snapshots; it does not observe live notifications.

Sources:
- https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/troubleshooting.md
- https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/server/tools.mdx

## Selection judgment

Compare two captured MCP tools/list snapshots and identify tool additions, removals, or contract changes using hashes. This is a narrowly scoped offline utility derived from those observations. The sources do not establish prevalence, market size, or expected stars.
