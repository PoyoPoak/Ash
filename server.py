# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server 
mcp = FastMCP(
    name="My MCP Server",
    description="A simple server to demonstrate MCP functionality",
    version="0.0.0.0",
    host="localhost",
    port=8050,
)

# Mock database class for example, usually ported in from a different file/module.
class Database:
    """Mock database class for example."""

    @classmethod
    async def connect(cls) -> "Database":
        """Connect to database."""
        return cls()

    async def disconnect(self) -> None:
        """Disconnect from database."""
        pass

    def query(self) -> str:
        """Execute a query."""
        return "Query result"

# Simple tool, can DB access, message sending, etc.
@mcp.tool()
def say_hello(name: str) -> str:
    """ Say hello to a user

    Args:
        name (str): The name of the user to greet.

    Returns:
        str: A greeting message.
    """
    return f"Hello, {name}! Nice to meet you."

# Simple resource, can be a local file, database, etc., ideally use a RAG/CAG pipeline.
@mcp.resource("file://documents/{name}")
def read_document(name: str) -> str:
    """ Read a document by name

    Args:
        name (str): The name of the document to read.

    Returns:
        str: The content of the document.
    """
    return f"Content of {name}"

# Simple prompt, can be used to generate text, images, etc.
@mcp.prompt(title="Code Review")
def review_code(code: str) -> str:
    """ Review a piece of code

    Args:
        code (str): The code to review.

    Returns:
        str: A review of the code.
    """
    return f"Please review this code:\n\n{code}"

# Run the server
if __name__ == "__main__":
    transport = "sse" # Default transport method
    
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    elif transport == "streamable-http":
        print("Running server with Streamable HTTP transport")
        mcp.run(transport="streamable-http")
    else:
        raise ValueError(f"Unknown transport method: {transport}")