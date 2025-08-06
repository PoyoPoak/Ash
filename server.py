# # server.py
# from mcp.server.fastmcp import FastMCP

# # Create an MCP server 
# mcp = FastMCP(
#     name="My MCP Server",
#     description="A simple server to demonstrate MCP functionality",
#     version="0.0.0.0",
#     host="localhost",
#     port=8050,
# )

# # Mock database class for example, usually ported in from a different file/module.
# class Database:
#     """Mock database class for example."""

#     @classmethod
#     async def connect(cls) -> "Database":
#         """Connect to database."""
#         return cls()

#     async def disconnect(self) -> None:
#         """Disconnect from database."""
#         pass

#     def query(self) -> str:
#         """Execute a query."""
#         return "Query result"

# # Simple tool, can DB access, message sending, etc.
# @mcp.tool()
# def say_hello(name: str) -> str:
#     """ Say hello to a user

#     Args:
#         name (str): The name of the user to greet.

#     Returns:
#         str: A greeting message.
#     """
#     return f"Hello, {name}! Nice to meet you."

# # Simple resource, can be a local file, database, etc., ideally use a RAG/CAG pipeline.
# @mcp.resource("file://documents/{name}")
# def read_document(name: str) -> str:
#     """ Read a document by name

#     Args:
#         name (str): The name of the document to read.

#     Returns:
#         str: The content of the document.
#     """
#     return f"Content of {name}"

# # Simple prompt, can be used to generate text, images, etc.
# @mcp.prompt(title="Code Review")
# def review_code(code: str) -> str:
#     """ Review a piece of code

#     Args:
#         code (str): The code to review.

#     Returns:
#         str: A review of the code.
#     """
#     return f"Please review this code:\n\n{code}"

# # Run the server
# if __name__ == "__main__":
#     transport = "sse" # Default transport method
    
#     if transport == "stdio":
#         print("Running server with stdio transport")
#         mcp.run(transport="stdio")
#     elif transport == "sse":
#         print("Running server with SSE transport")
#         mcp.run(transport="sse")
#     elif transport == "streamable-http":
#         print("Running server with Streamable HTTP transport")
#         mcp.run(transport="streamable-http")
#     else:
#         raise ValueError(f"Unknown transport method: {transport}")


import os
import json
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(
    name="Knowledge Base",
    host="0.0.0.0",  # only used for SSE transport (localhost)
    port=8050,  # only used for SSE transport (set this to any port)
)


@mcp.tool()
def get_knowledge_base() -> str:
    """Retrieve the entire knowledge base as a formatted string.

    Returns:
        A formatted string containing all Q&A pairs from the knowledge base.
    """
    try:
        kb_path = os.path.join(os.path.dirname(__file__), "data", "kb.json")
        with open(kb_path, "r") as f:
            kb_data = json.load(f)

        # Format the knowledge base as a string
        kb_text = "Here is the retrieved knowledge base:\n\n"

        if isinstance(kb_data, list):
            for i, item in enumerate(kb_data, 1):
                if isinstance(item, dict):
                    question = item.get("question", "Unknown question")
                    answer = item.get("answer", "Unknown answer")
                else:
                    question = f"Item {i}"
                    answer = str(item)

                kb_text += f"Q{i}: {question}\n"
                kb_text += f"A{i}: {answer}\n\n"
        else:
            kb_text += f"Knowledge base content: {json.dumps(kb_data, indent=2)}\n\n"

        return kb_text
    except FileNotFoundError:
        return "Error: Knowledge base file not found"
    except json.JSONDecodeError:
        return "Error: Invalid JSON in knowledge base file"
    except Exception as e:
        return f"Error: {str(e)}"


# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")