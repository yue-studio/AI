# Agno OpenDIA Agent

This project contains a Python script (`test-mcp.py`) that demonstrates how to use an Agno (https://github.com/agno-agi/agno) agent to interact with the web via the OpenDIA Model Context Protocol (MCP) tool.
It also uses the local LLM via ollama.

The following were implemented:

1.  **Local LLM**
    *   Uses llama3.2 via Ollama (https://ollama.com/)

2.  **`MCPTools` Initialization:**
    *   Uses OpenDIA (https://github.com/aaronjmars/opendia) to connect to a locally installed browser (Google Chrome).
    *   Utilizes `mcp_servers_config`, dynamically constructing the command string (`npx -y opendia`) from the dictionary's `command` and `args` entries.

3.  **Increased MCP Timeout:**
    *   The `MCPTools` initialization includes `timeout_seconds=30`, providing more time for the OpenDIA MCP server to respond and preventing premature timeouts.

