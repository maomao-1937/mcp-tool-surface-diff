# 测试说明：mcp-tool-surface-diff

- 运行环境：Windows Python 3.11.15。
- 依赖：仅 Python 标准库。
- 命令：`python -m unittest discover -s tests -v`；`python examples/run_examples.py`。
- GitHub Actions：Ubuntu 和 Windows，Python 3.11。
- 单元测试覆盖输入长度/深度、重复键、畸形数据、输出脱敏与退出码。

测试验证文档所述输入范围和 CLI 行为，不连接 MCP 服务，也不推断所有客户端的一致行为。
