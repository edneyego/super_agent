# Sistema Multi-Agente com LangGraph + MCP

🤖 Sistema inteligente de agentes especializados orquestrados via LangGraph e Model Context Protocol (MCP).

## 📋 Visão Geral

Este projeto implementa um sistema multi-agente onde:

- **Orquestrador LangGraph**: Coordena e roteia queries entre agentes
- **MCP Server**: Expõe ferramentas e recursos via protocolo padronizado
- **Agentes Especializados**: Weather, Data, Finance, Information
- **Comunicação MCP**: Protocolo unificado para interação entre componentes

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│ CLI / User Interface                                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Orquestrador LangGraph                                  │
│ ┌──────────────────────────────────────────────────┐   │
│ │ Supervisor (LLM)                                 │   │
│ │ - Analisa query                                  │   │
│ │ - Roteia para agente apropriado                  │   │
│ │ - Coordena multi-agente                          │   │
│ └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼────────┐ ┌────▼───────┐ ┌─────▼──────┐
│ Weather    │ │ Data       │ │ Finance    │
│ Agent      │ │ Agent      │ │ Agent      │
└────────────┘ └────────────┘ └────────────┘
```

## ✨ Características

- ✅ **Arquitetura Hexagonal**: Core isolado da infraestrutura
- ✅ **MCP Protocol**: Comunicação padronizada entre componentes
- ✅ **LangGraph**: Orquestração inteligente com LLM
- ✅ **Agentes Especializados**: Cada agente com domínio específico
- ✅ **Async/Await**: Performance otimizada
- ✅ **Type Hints**: Código fortemente tipado
- ✅ **Extensível**: Fácil adicionar novos agentes e ferramentas

## 🚀 Quick Start

### Pré-requisitos

- Python 3.13+
- pip ou uv
- Chave de API OpenAI/Google/Anthropic

### Instalação

```bash
# Clone o repositório
git clone https://github.com/edneyego/super_agent.git
cd super_agent

# Crie ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instale dependências
pip install -e .

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais
```

### Configuração

Edite `.env`:

```bash
# LLM Configuration
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini

# MCP Server
MCP_HOST=127.0.0.1
MCP_PORT=8000
MCP_TRANSPORT=stdio

# Weather API
WEATHER_API_BASE_URL=https://api.open-meteo.com/v1/forecast

# System
LOG_LEVEL=INFO
```

## 📖 Uso do Sistema

O sistema possui **4 modos de execução** através do script `run.sh`:

### 1️⃣ Modo CLI - Query Única

Execute uma query diretamente:

```bash
./run.sh cli "Como está o clima em São Paulo?"
```

**Exemplos:**
```bash
./run.sh cli "Qual a temperatura no Rio de Janeiro?"
./run.sh cli "Converta 1000 USD para BRL"
./run.sh cli "O que é inteligência artificial?"
```

### 2️⃣ Modo Interativo

Entre em modo de conversação contínua:

```bash
./run.sh interactive
```

**Sessão interativa:**
```
╔═══════════════════════════════════════════════════════════╗
║         Super Agent - Sistema Multi-Agente             ║
║              LangGraph + MCP Protocol                  ║
╚═══════════════════════════════════════════════════════════╝

💬 Modo Interativo - Digite 'sair' para encerrar

Você: Como está o clima em Belo Horizonte?
Agente: [resposta sobre o clima]

Você: Converta 500 EUR para BRL
Agente: [resposta com conversão]

Você: sair
👋 Até logo!
```

### 3️⃣ Modo Teste

Execute queries de teste automaticamente:

```bash
./run.sh test
```

**Testes executados:**
- ✅ Weather Agent: Consulta clima de São Paulo
- ✅ Information Agent: Pergunta sobre sistemas multi-agente

### 4️⃣ Modo Server (MCP Server Standalone)

Inicia apenas o MCP Server para uso com clientes MCP externos:

```bash
./run.sh server
```

**Nota:** Este modo aguarda conexões de clientes MCP via STDIO.

## 📚 Exemplos de Uso por Agente

### Weather Agent 🌤️

```bash
./run.sh cli "Como está o clima em São Paulo?"
./run.sh cli "Qual a temperatura no Rio de Janeiro?"
./run.sh cli "Me diga o clima em Brasília"
```

### Data Agent 🗄️

```bash
./run.sh cli "Quantas reservas temos no banco?"
./run.sh cli "Qual o destino mais popular?"
./run.sh cli "Liste as últimas 5 reservas"
```

### Finance Agent 💰

```bash
./run.sh cli "Converta 1000 USD para BRL"
./run.sh cli "Calcule juros compostos de 10000 a 0.5% por 12 meses"
./run.sh cli "Quanto é 500 EUR em reais?"
```

### Information Agent 💡

```bash
./run.sh cli "O que é um sistema multi-agente?"
./run.sh cli "Explique o que é LangGraph"
./run.sh cli "Como funciona inteligência artificial?"
```

### Query Complexa (Multi-Agente) 🔄

```bash
./run.sh cli "Qual foi o destino mais vendido e como está o clima lá?"
```

## 🎯 Agentes Disponíveis

### 1. Weather Agent 🌤️

**Responsabilidade:** Consultas meteorológicas

**Ferramentas MCP:**
- `get_weather(city, country)` - Obtém clima em tempo real

**Exemplos de queries:**
- "Como está o clima em [cidade]?"
- "Qual a temperatura em [cidade]?"
- "Vai chover em [cidade] hoje?"

### 2. Data Agent 🗄️

**Responsabilidade:** Consultas ao banco de dados

**Ferramentas MCP:**
- `query_database(sql)` - Executa queries SQL SELECT

**Exemplos de queries:**
- "Quantas reservas temos?"
- "Qual o destino mais popular?"
- "Liste as reservas do mês"

### 3. Finance Agent 💰

**Responsabilidade:** Operações financeiras

**Ferramentas MCP:**
- `convert_currency(amount, from, to)` - Conversão de moedas
- `calculate_compound_interest(principal, rate, periods)` - Cálculo de juros

**Exemplos de queries:**
- "Converta X [moeda] para Y"
- "Calcule juros compostos de..."
- "Quanto é X dólares em reais?"

### 4. Information Agent 💡

**Responsabilidade:** Perguntas gerais e conhecimento

**Ferramentas:** LLM direto (sem ferramentas externas)

**Exemplos de queries:**
- "O que é...?"
- "Explique..."
- "Como funciona...?"

## 🔧 Desenvolvimento

### Estrutura do Projeto

```
super_agent/
├── src/
│   ├── agents/              # Agentes especializados
│   │   ├── base.py         # Classe base abstrata
│   │   ├── weather.py      # Weather Agent
│   │   ├── data.py         # Data Agent
│   │   ├── finance.py      # Finance Agent
│   │   └── information.py  # Information Agent
│   ├── mcp/
│   │   └── server.py       # MCP Server com ferramentas
│   ├── orchestrator/
│   │   └── main.py         # Orquestrador LangGraph
│   └── cli.py              # Interface CLI
├── data/
│   └── database.db         # Banco de dados SQLite
├── logs/                   # Logs do sistema
├── run.sh                  # Script principal de execução
├── .env                    # Configurações
└── README.md
```

### Adicionar Novo Agente

1. **Crie o arquivo do agente** em `src/agents/`:

```python
# src/agents/custom.py
from agents.base import BaseAgent, AgentState

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="custom_agent",
            description="Descrição do agente"
        )
    
    async def execute(self, state: AgentState) -> AgentState:
        query = state.get("query")
        # Lógica do agente
        result = "Resultado"
        
        state["result"] = result
        return state
```

2. **Registre no supervisor** (`src/orchestrator/main.py`):

```python
# Adicione na lista de agentes
from agents.custom import CustomAgent

# No create_supervisor_node, adicione:
# - custom_agent: Descrição do que ele faz

# No create_orchestrator, adicione:
custom_agent = CustomAgent()
workflow.add_node("custom_agent", custom_agent.execute)
```

3. **Adicione roteamento condicional**

### Adicionar Nova Ferramenta MCP

No arquivo `src/mcp/server.py`, adicione:

```python
@mcp.tool()
def my_custom_tool(param: str) -> dict:
    """
    Descrição da ferramenta.
    
    Args:
        param: Descrição do parâmetro
    
    Returns:
        Resultado da operação
    """
    try:
        # Lógica da ferramenta
        result = f"Processed {param}"
        return {"result": result}
    except Exception as e:
        logger.error(f"Erro: {e}")
        return {"error": str(e)}
```

## 🧪 Testes

```bash
# Executar testes automáticos
./run.sh test

# Testar agente específico
./run.sh cli "Query específica para testar agente"

# Modo interativo para testes manuais
./run.sh interactive
```

## 📊 Stack Tecnológica

- **Python 3.13**: Linguagem base
- **LangGraph**: Orquestração de agentes
- **LangChain**: Framework LLM
- **FastMCP**: Implementação MCP
- **SQLite**: Banco de dados
- **asyncio**: Programação assíncrona
- **OpenAI/Google/Anthropic**: LLMs

## 🐛 Solução de Problemas

### Erro: "LLM_API_KEY não configurada"

```bash
# Edite o arquivo .env e adicione sua chave de API
nano .env

# Adicione:
LLM_API_KEY=sk-your-key-here
```

### Erro: "No module named 'requests'"

```bash
pip install requests
```

### Erro: "No module named 'langgraph'"

```bash
pip install langgraph langchain langchain-openai
```

### MCP Server não inicia

```bash
# Verifique os logs
cat logs/mcp_server.log

# Reinstale FastMCP
pip install --upgrade fastmcp
```

### Permissão negada ao executar run.sh

```bash
chmod +x run.sh
```

## 📖 Documentação Adicional

- **ARCHITECTURE.md** - Arquitetura detalhada do sistema
- **IMPLEMENTATION_GUIDE.md** - Guia completo de implementação
- **API.md** - Documentação das APIs e ferramentas MCP

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovoAgente`)
3. Commit suas mudanças (`git commit -m 'Add: Novo agente XYZ'`)
4. Push para a branch (`git push origin feature/NovoAgente`)
5. Abra um Pull Request

## 📝 License

MIT License - veja LICENSE para detalhes.

## 👤 Autor

**Edney Oliveira**

- GitHub: [@edneyego](https://github.com/edneyego)
- Email: edneyego@gmail.com
- Location: Brasil - MG / Belo Horizonte

## 🙏 Agradecimentos

- LangChain Team pelo LangGraph
- FastMCP pela implementação MCP
- Open-Meteo pela API de clima gratuita

## 📞 Suporte

- 📫 Issues: [GitHub Issues](https://github.com/edneyego/super_agent/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/edneyego/super_agent/discussions)

---

⭐ **Se este projeto foi útil, considere dar uma estrela!**

**Happy Coding! 🚀**
