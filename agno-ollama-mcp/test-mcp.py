import asyncio
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.mcp import MCPTools

mcp_servers_config = {
    "opendia": {
      "command": "npx",
      "args": ["-y", "opendia"]
    }
}

def print_welcome():
    print('''
Agno to use OpenDIA to browse the web
---------------------------------
Type 'quit' to stop.
''')

async def main():
    print_welcome()

    opendia_config = mcp_servers_config["opendia"]
    command_str = f"{opendia_config['command']} {' '.join(opendia_config['args'])}"
    async with MCPTools(command_str, timeout_seconds=30) as mcp_tools:
        agent = Agent(
            name="Agno OpenDIA Agent",
            role="An AI assistant that uses the browser via MCP.",
            model=Ollama(id="llama3.2", provider="Ollama"),
            tools=[mcp_tools],
            instructions='''
You are an AI assistant specialized in web browsing through the openDIA MCP tool.
Your task is to understand user requests, navigate the web to find relevant information, and perform actions as needed.
Always explain your thought process, show the output of your tool calls, and summarize findings concisely.
''',
            show_tool_calls=True,
            add_state_in_messages=True,
            markdown=True
        )
        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in {"quit"}:
                print("Goodbye!")
                break

            try:
                await agent.aprint_response(user_input, stream=True)
            except Exception as e:
                print(f"\n Error: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
