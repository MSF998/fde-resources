import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool,TextContent


def greet_user(user_name):
    return(f"Hello {user_name}")


server = Server("test-mcp-server")

async def main():
    print("Init-ing MCP Server")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="say_hello",
            description=(
                "Say hello to the user"
            ),
            inputSchema={
                "type":"object",
                "properties":{
                    "user_name":{"type":"string"}
                },
                "required":["user_name"],
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "say_hello":
            result = greet_user(**arguments)
        else:
            raise ValueError(f"Unknown Tool: {name}")
        return [TextContent(type="text", text=json.dumps(result, default=str))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}))]

if __name__ == "__main__":
    asyncio.run(main())