import asyncio
import sys
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def main():
    # Configure the stdio transport to spawn server.py as a subprocess
    server_params = StdioServerParameters(
        command=sys.executable,  # Uses the current Python interpreter
        args=["server.py"],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. Initialize the MCP connection
            await session.initialize()
            print("Connected to MCP Server!\n")

            # 2. Call list_tools
            tools = await session.list_tools()
            print("--- Available Tools ---")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # 3. Call add_company tool
            response = await session.call_tool(
                name="say_hello",
                arguments={
                    "user_name": "Sahnoon",
                },
            )

            # Print tool execution results
            for content in response.content:
                if content.type == "text":
                    print("Result:", content.text)


if __name__ == "__main__":
    asyncio.run(main())