"""MCP server (stdio) que expõe tools da TODO list, implementadas chamando a API 4.1.

Arquitetura:
    Agente/LLM --MCP--> este server --HTTP--> API 4.1 (localhost:8000)

As tools NÃO guardam estado próprio: cada chamada vai à API REST, que é a
fonte do dado. O MCP é só o adaptador entre o protocolo do agente e o HTTP.
"""
import httpx
from mcp.server.fastmcp import FastMCP

API = "http://localhost:8000"
mcp = FastMCP("tarefas-mcp")


@mcp.tool()
def criar_tarefa(titulo: str) -> dict:
    """Cria uma tarefa na API e devolve o objeto criado."""
    resp = httpx.post(f"{API}/tarefas", json={"titulo": titulo}, timeout=10)
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
def listar_tarefas() -> list:
    """Lista todas as tarefas da API."""
    resp = httpx.get(f"{API}/tarefas", timeout=10)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    mcp.run()  # transporte stdio por padrão
