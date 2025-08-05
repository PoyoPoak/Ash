import asyncio
import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

nest_asyncio.apply()  # Needed to run interactive python

async def main():
    # Define server parameters for the CLI server, both the client and server will run in the same process
    server_params = StdioServerParameters(
        command="python",  # The command to run your server
        args=["server.py"],  # Arguments to the command
    )
    
    """
    By default, the server will run in the same process as the client, 
    using stdio transport. That way we don't have to spin the server up
    in a separate process first.
    """
   

    # Connect to the server
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # # Call our name tool
            # name_result = await session.call_tool("say_hello", {"name": "Alice"})
            # print(f"Tool call result: {name_result}")


if __name__ == "__main__":
    asyncio.run(main())