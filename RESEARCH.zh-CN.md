# 研究记录：mcp-tool-surface-diff

## 来源中可观察的事实

MCP Python SDK 官方排障文档提到，客户端若不处理 notifications/tools/list_changed，可能继续使用旧工具列表。本工具只比较两份快照，不监听实时通知。

来源链接见 [RESEARCH.md](RESEARCH.md)。

## 选题判断

比较两份 MCP tools/list 快照，用摘要标出工具新增、移除或契约变化。 这是基于上述观察形成的离线工具设想；来源不能证明发生率、市场规模或预期 Star。
