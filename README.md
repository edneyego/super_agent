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
│                    CLI / User Interface                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Orquestrador LangGraph                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │           Supervisor (LLM)                       │  │
│  │  - Analisa query                                 │  │
│  │  - Roteia para agente apropriado                 │  │
│  │  - Coordena multi-agente                         │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │ MCP Protocol
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    MCP Server (FastMCP)                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐        │
│  │  Weather   │  │  Database  │  │  Finance   │        │
│  │   Tools    │  │   Tools    │  │   Tools    │        │
│  └────────────┘  └────────────┘  └────────────┘        │
└─────────────────────────────────────────────────────────┘
                     ▲
                     │ MCP Protocol
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼────────┐   ┌─────▼──────┐   ┌──────▼───┐
│ Weather │   │   Data   │   │ Finance │
│  Agent  │   │  Agent   │   │  Agent  │
└─────────┘   └──────────┘   └─────────┘
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
.venv\Scripts\activate  # Windows

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

### Execução

#### Método 1: Script Automatizado

```bash
chmod +x run.sh
./run.sh
```

#### Método 2: Manual

**Terminal 1 - MCP Server:**
```bash
python src/mcp/server.py
```

**Terminal 2 - Orquestrador:**
```bash
python src/orchestrator/main.py
```

**Terminal 3 - Queries:**
```bash
python src/cli.py "Como está o clima em São Paulo?"
```

#### Método 3: Modo Interativo

```bash
python src/cli.py --interactive
```

## 📚 Exemplos de Uso

### Weather Agent

```bash
python src/cli.py "Como está o clima em São Paulo?"
python src/cli.py "Qual a temperatura no Rio de Janeiro?"
```

### Data Agent

```bash
python src/cli.py "Quantas reservas temos no banco?"
python src/cli.py "Qual o destino mais popular?"
```

### Finance Agent

```bash
python src/cli.py "Converta 1000 USD para BRL"
python src/cli.py "Calcule juros compostos de 10000 a 0.5% por 12 meses"
```

### Query Complexa (Multi-Agente)

```bash
python src/cli.py "Qual foi o destino mais vendido e como está o clima lá?"
```

## 🎯 Agentes Disponíveis

### 1. Weather Agent
- Consulta clima em tempo real
- Previsão do tempo
- Dados meteorológicos

### 2. Data Agent
- Consultas SQL no banco de dados
- Análise de dados de reservas
- Estatísticas e relatórios

### 3. Finance Agent
- Conversão de moedas
- Cálculo de juros
- Operações financeiras

### 4. Information Agent
- Responde perguntas gerais
- Explica conceitos
- Fornece informações contextuais

## 🔧 Desenvolvimento

### Adicionar Novo Agente

1. Crie o arquivo do agente em `src/agents/`
2. Implemente a classe base `BaseAgent`
3. Crie o agent card em `agent_cards/`
4. Registre no supervisor
5. Adicione ferramentas MCP se necessário

Veja [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) para detalhes.

### Adicionar Nova Ferramenta MCP

```python
# src/mcp/tools/custom.py
from fastmcp import FastMCP

mcp = FastMCP("Custom Tools")

@mcp.tool(name='my_tool', description='Minha ferramenta')
def my_tool(param: str) -> dict:
    return {'result': f'Processed {param}'}
```

## 📖 Documentação

- [README.md](README.md) - Este arquivo
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura detalhada
- [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) - Guia de implementação completo

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Testes com coverage
pytest --cov=src

# Teste específico
pytest tests/test_agents.py -v
```

## 📊 Stack Tecnológica

- **Python 3.13**: Linguagem base
- **LangGraph**: Orquestração de agentes
- **LangChain**: Framework LLM
- **FastMCP**: Implementação MCP pura
- **SQLite**: Banco de dados
- **asyncio**: Programação assíncrona
- **OpenAI/Google/Anthropic**: LLMs

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovoAgente`)
3. Commit suas mudanças (`git commit -m 'Add: Novo agente XYZ'`)
4. Push para a branch (`git push origin feature/NovoAgente`)
5. Abra um Pull Request

## 📝 License

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 👤 Autor

**Edney Oliveira**
- GitHub: [@edneyego](https://github.com/edneyego)
- Email: edneyego@gmail.com
- Location: Brasil - MG / Belo Horizonte

## 🙏 Agradecimentos

- LangChain Team pelo LangGraph
- FastMCP pela implementação MCP
- Open-Meteo pela API de clima

## 📞 Suporte

- 📫 Issues: [GitHub Issues](https://github.com/edneyego/super_agent/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/edneyego/super_agent/discussions)

---

⭐ Se este projeto foi útil, considere dar uma estrela!

**Happy Coding! 🚀**