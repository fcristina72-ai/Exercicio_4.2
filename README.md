# Exercício 4.2 — MCP server local que consome a API 4.1

**Aluna:** Flávia Cristina de Sousa Silva Dias Paz

Camada do meio entre um agente de IA e a API REST de TODO list do exercício 4.1:
um **MCP server** (stdio) que expõe duas tools e as implementa chamando a API.

```
Agente / LLM  --MCP-->  servidor_mcp.py  --HTTP-->  API 4.1 (localhost:8000)
```

## Tools expostas

| Tool | Assinatura | O que faz |
|------|-----------|-----------|
| `criar_tarefa` | `criar_tarefa(titulo: str) -> dict` | faz `POST /tarefas` e devolve a tarefa criada |
| `listar_tarefas` | `listar_tarefas() -> list` | faz `GET /tarefas` e devolve a lista |

## Como rodar

**Terminal A** — suba a API do 4.1 (reinicie para o store ficar limpo):
```bash
uvicorn app.main:app --port 8000     # no repo do 4.1
```

**Terminal B** — no repo do 4.2:
```bash
pip install -r requirements.txt
python cliente_teste.py
```
Deve imprimir o envelope JSON com `tools`, `criar_resultado` e `listar_resultado`.

## Estrutura

```
servidor_mcp.py      # MCP server (tools que chamam a API 4.1)
cliente_teste.py     # imprime o envelope JSON que o autograder lê
requirements.txt     # mcp, httpx
README.md
.autograde-exercise  # 4.2
```

## Reflexão (Aula 6)

> No 4.1 o cliente precisava falar HTTP. No 4.2, o agente só precisa saber que existe uma tool `criar_tarefa(titulo)`. O que o MCP tornou irrelevante para quem chama?

O MCP transformou uma **chamada de protocolo** (onde detalhamos *como* fazer) em uma **chamada de intenção** (onde dizemos apenas *o que* queremos).

- **Como era antes (cliente HTTP):** o agente precisava lidar com a burocracia da rede — saber a URL (`localhost:8000`), o verbo adequado (`POST`) e montar o corpo do JSON manualmente.
- **Como é com o MCP (usuário de função):** o agente apenas chama `criar_tarefa(titulo)` pelo nome, como se fosse uma função local do próprio código.
- **Onde foi parar a complexidade?** Ela foi movida para o servidor MCP. É ele quem faz o trabalho sujo de traduzir a execução da ferramenta em uma requisição HTTP real para a API.

**O grande ganho:** o MCP padronizou o *contrato*. O agente agora fala uma linguagem universal de ferramentas, tornando irrelevante o protocolo específico de cada API externa.
