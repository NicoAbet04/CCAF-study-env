# Module 05 — Introduction to Model Context Protocol

> **What this file is.** The CCAF prep track has seven courses; my notes cover
> five. This file stands in for the *Introduction to Model Context Protocol*
> course I did not take, so Domain 2 (Tool Design & MCP Integration, 18% of the
> exam and one of the two highest-failure domains) is not built on a gap.
>
> It follows that course's published syllabus and is written from two sources
> only: the official MCP documentation (modelcontextprotocol.io) and the MCP
> project I actually built in the *Building with the Claude API* course
> (`src/02_building_with_claude_api/mcp/cli_project/`). Treat it as a PRIMARY
> source like any other course note.
>
> Doc references: [Server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts).

---

## 1. Introducing MCP

**Model Context Protocol (MCP)** is a standard way for an AI application to
connect to outside capabilities. Without it, every app has to hand-roll its own
integration for every backend it touches. With it, a server exposes its
capabilities once, and any MCP-aware client can use them.

The mental model that matters for the exam: MCP is a **protocol**, not a
library. A *server* publishes capabilities; a *client* discovers and calls them.
Claude Code, the desktop app, and your own scripts can all be clients.

### MCP clients

A client connects to one or more servers, asks each what it offers, and makes
those capabilities available to the model. Two facts worth remembering:

- Tools from **all connected servers are discovered at connection time** and are
  available to the agent simultaneously. Connecting five servers means the model
  is choosing among the union of their tools — which is exactly why tool count
  and description quality matter (see Domain 2, task 2.3).
- The client, not the server, decides how retrieved data reaches the model.

---

## 2. The three server primitives

This is the core of the course and the single most exam-relevant idea in it.
A server exposes capability through exactly three building blocks, and they are
distinguished by **who controls them**:

| Primitive | What it is | Who controls it |
|---|---|---|
| **Tools** | Functions the model can actively call to *do* something — write to a database, call an API, modify a file | **Model** |
| **Resources** | Passive, read-only data sources that supply context — file contents, schemas, documentation | **Application** |
| **Prompts** | Pre-built instruction templates that direct the model to use specific tools and resources | **User** |

If you remember one line from this module: **tools are model-controlled,
resources are application-controlled, prompts are user-controlled.** The
protocol operations follow the same three-way split — `tools/list` and
`tools/call`; `resources/list`, `resources/templates/list` and `resources/read`;
`prompts/list` and `prompts/get`.

A useful corollary: exposing data as a **resource** rather than forcing the
agent to discover it through tool calls reduces exploratory tool traffic. That
is the reasoning behind exposing content catalogs — issue summaries,
documentation hierarchies, database schemas — as resources.

---

## 3. Hands-on with MCP servers

### Project setup

The Python SDK's `FastMCP` class wraps the protocol so you declare capabilities
with decorators instead of writing JSON-RPC handlers. My server starts with:

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("DocumentMCP", log_level="ERROR")
```

and ends by choosing a transport:

```python
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**stdio** is the transport for a locally-launched server: the client starts the
server as a subprocess and speaks over standard input/output. That is why the
client configuration is a *command plus arguments* rather than a URL.

### Defining tools

A tool is a decorated function. The name and description are not decoration —
they are the entire basis on which the model decides whether to call it:

```python
@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string"
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]
```

Two things to notice, both of which the exam tests:

- **Per-parameter descriptions** via Pydantic `Field` become the JSON Schema the
  model reads. `doc_id` is not self-explanatory; the description makes it so.
- **Input schemas are generated from type hints.** MCP validates with JSON
  Schema, and each tool should perform one clearly-bounded operation.

My `edit_document` tool is a good example of a description that removes
ambiguity — it spells out that `old_str` "must match exactly, including
whitespace," which is precisely the kind of boundary detail that stops a model
from misusing a tool.

### The server inspector

The MCP Inspector is a development tool that connects to a server and lets you
list and invoke its tools, resources, and prompts by hand — before wiring up any
client. The practical value: it isolates *"is my server correct?"* from *"is the
model choosing my tool correctly?"* Those are different failures with different
fixes, and testing them separately saves a lot of confusion.

---

## 4. Connecting with MCP clients

### Implementing a client

A client's job is connect → initialize → discover → call. Mine wraps a session:

```python
server_params = StdioServerParameters(command=self._command, args=self._args, env=self._env)
stdio_transport = await self._exit_stack.enter_async_context(stdio_client(server_params))
self._session = await self._exit_stack.enter_async_context(ClientSession(_stdio, _write))
await self._session.initialize()
```

The `initialize()` call is the protocol handshake — capabilities are negotiated
before anything else happens. After that, the session exposes one method per
protocol operation: `list_tools()`, `call_tool()`, `list_prompts()`,
`get_prompt()`, `read_resource()`.

### Defining and accessing resources

Resources are addressed by **URI**, and they come in two flavours:

```python
@mcp.resource("docs://documents", mime_type="application/json")
def list_docs() -> list[str]:
    return list(docs.keys())

@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_doc(doc_id: str) -> str:
    return docs[doc_id]
```

- `docs://documents` is a **direct resource** — a fixed URI returning a specific
  piece of data.
- `docs://documents/{doc_id}` is a **resource template** — a parameterized URI
  that answers a family of queries. Templates carry metadata (title,
  description, MIME type), which makes them self-documenting and discoverable,
  and they support parameter completion so a user typing "dep" can be offered
  `deposition.md`.

The `mime_type` matters on the client side. My client branches on it:

```python
if isinstance(resource, types.TextResourceContents):
    if resource.mimeType == "application/json":
        return json.loads(resource.text)
return resource.text
```

The server declares how to interpret the bytes; the client honours that
declaration. Getting the MIME type wrong means the client hands the model a JSON
string it treats as prose.

### Defining prompts, and prompts in the client

A prompt returns *messages*, not a string — it is a pre-built conversation
opener, and it can instruct the model which tools to use:

```python
@mcp.prompt(name="format", description="Rewrites the contents of the document in Markdown format.")
def format_document(doc_id=Field(description="Id of the document to format")) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.
    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>
    Use the 'edit_document' tool to edit the document.
    """
    return [base.UserMessage(prompt)]
```

This shows the three primitives composing: a **user** invokes the prompt, the
prompt names a **tool**, and the tool operates on data the server also exposes as
a **resource**. Note the XML-style `<document_id>` delimiter — the same
structured-prompting habit that Domain 4 tests.

In the client, `get_prompt()` returns `result.messages` — a ready-made message
list to feed to Claude. Applications typically surface prompts as slash commands
or a command palette, which is the UI expression of "user-controlled."

> **Left unfinished in my project:** a `summarize` prompt is stubbed with a
> comment and never implemented. Worth completing as practice — it is the
> smallest possible exercise in the full loop.

---

## 5. Where this connects to the exam

Domain 2 tests judgment, not syntax. The bridges from this module:

- **Scoping** — project-level `.mcp.json` for shared team tooling versus
  user-level `~/.claude.json` for personal or experimental servers; environment
  variable expansion (`${GITHUB_TOKEN}`) so credentials are never committed.
- **Descriptions decide selection.** A capable MCP tool with a thin description
  loses to a built-in like Grep, because the model picks on description quality.
- **Resources vs tools** is a design decision, not a formality: passive context
  belongs in resources, actions belong in tools.
- **Prefer existing community servers** for standard integrations (Jira,
  GitHub); build custom servers for team-specific workflows.
- **Structured errors** are Domain 2's other half — the MCP `isError` flag plus
  an error category and a retryable flag, so the agent can decide between
  retrying, explaining, and escalating. A uniform "Operation failed" strips the
  agent of any basis for that decision.
