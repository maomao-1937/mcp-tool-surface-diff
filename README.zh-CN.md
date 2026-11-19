# mcp-tool-surface-diff

比较两份 MCP tools/list 快照，用摘要标出工具新增、移除或契约变化。

适用对象：排查部署或服务端更新前后工具列表差异的 MCP 维护者。

## 快速开始

需要 Python 3.11 或更新版本，无第三方依赖。CLI 从标准输入读取一份 JSON，并输出一行确定性 JSON。

```console
python mcp_tool_surface_diff.py < examples/input.json
```

输出：

```json
{"after_count":2,"before_count":1,"changed":true,"changes":[{"after_sha256":"7dda98f8726509478a778725fc4f8e76345bc48ee4893b1801d20a5ecbcae42b","change":"added","tool":"delete"}],"counts":{"added":1,"changed":0,"removed":0}}
```

运行测试和精确示例检查：

```console
python -m unittest discover -s tests -v
python examples/run_examples.py
```

输入限制为 512 KiB；畸形 JSON、重复键或过深输入会返回固定错误码。输出不会回显 schema 描述或值，问题指针可能包含 schema 对象键名。程序不会启动或连接 MCP 服务。

## 问题证据与范围

MCP Python SDK 官方排障文档提到，客户端若不处理 notifications/tools/list_changed，可能继续使用旧工具列表。本工具只比较两份快照，不监听实时通知。

这些证据仅说明具体报告和公开记录的行为，不能证明问题发生频率，也不能预测 GitHub Star。

## 限制

按精确名称报告新增/移除，并比较规范化 JSON 摘要。不推断语义等价、不监控服务器、不验证通知投递。输出会包含工具名，不包含 schema 正文。

## 许可证与署名

MIT。本仓库使用原创代码和合成样例，不包含上游代码或素材。

## 已验证环境

Windows Python 3.11.15；GitHub Actions Ubuntu 与 Windows，Python 3.11。
