"""Sobe o servidor_mcp via stdio, exercita as tools e imprime UM envelope JSON.

CRÍTICO: o stdout contém SOMENTE o JSON final. Qualquer log vai para stderr,
senão o autograder não consegue parsear o envelope.
"""
import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _parse_bloco(bloco):
    """Converte um bloco de conteúdo em objeto Python (JSON se possível)."""
    texto = getattr(bloco, "text", None)
    if texto is None:
        return None
    try:
        return json.loads(texto)
    except (json.JSONDecodeError, TypeError):
        return texto


def _como_objeto(resultado):
    """Para tools que retornam um dict: pega o primeiro bloco."""
    content = getattr(resultado, "content", None)
    if content:
        return _parse_bloco(content[0])
    structured = getattr(resultado, "structuredContent", None)
    if isinstance(structured, dict) and set(structured.keys()) == {"result"}:
        return structured["result"]
    return structured


def _como_lista(resultado):
    """Para tools que retornam uma lista: reconstrói a lista a partir dos blocos.

    O FastMCP serializa uma list em N blocos de conteúdo (um por item). Aqui
    juntamos todos. Também cobrimos o caso de um único bloco que já é uma lista.
    """
    # Preferir structuredContent quando ele já traz a lista pronta.
    structured = getattr(resultado, "structuredContent", None)
    if isinstance(structured, dict) and "result" in structured and isinstance(structured["result"], list):
        return structured["result"]

    content = getattr(resultado, "content", None) or []
    itens = []
    for bloco in content:
        valor = _parse_bloco(bloco)
        if isinstance(valor, list):
            itens.extend(valor)        # bloco já era a lista inteira
        elif valor is not None:
            itens.append(valor)        # bloco é um item
    return itens


async def main() -> dict:
    params = StdioServerParameters(command="python", args=["servidor_mcp.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            nomes = [t.name for t in tools.tools]

            criar = await session.call_tool("criar_tarefa", {"titulo": "tarefa via mcp"})
            listar = await session.call_tool("listar_tarefas", {})

            return {
                "tools": nomes,
                "criar_resultado": _como_objeto(criar),
                "listar_resultado": _como_lista(listar),
            }


if __name__ == "__main__":
    envelope = asyncio.run(main())
    print(json.dumps(envelope))
