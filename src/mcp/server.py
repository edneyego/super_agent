"""MCP Server - FastMCP Implementation"""

import asyncio
import os
import logging
from typing import Dict, Any
from fastmcp import FastMCP

# Configura logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializa FastMCP
mcp = FastMCP(
    name="Super Agent MCP Server",
    version="1.0.0"
)


# ===== WEATHER TOOLS =====

@mcp.tool(name="get_weather", description="Obtém informações meteorológicas atuais")
async def get_weather(city: str) -> Dict[str, Any]:
    """Busca dados de clima."""
    from src.agents.weather_agent import WeatherAgent
    agent = WeatherAgent()
    return await agent.execute(f"Como está o clima em {city}?")


@mcp.tool(name="get_forecast", description="Obtém previsão do tempo")
async def get_forecast(city: str, days: int = 3) -> Dict[str, Any]:
    """Busca previsão."""
    from src.agents.weather_agent import WeatherAgent
    agent = WeatherAgent()
    result = await agent.execute(f"Previsão para {city}")
    result["days"] = days
    return result


# ===== DATABASE TOOLS =====

@mcp.tool(name="query_database", description="Executa consulta no banco de dados")
async def query_database(query_text: str) -> Dict[str, Any]:
    """Consulta o banco."""
    from src.agents.data_agent import DataAgent
    agent = DataAgent()
    return await agent.execute(query_text)


@mcp.tool(name="get_statistics", description="Obtém estatísticas do banco")
async def get_statistics() -> Dict[str, Any]:
    """Retorna estatísticas."""
    from src.agents.data_agent import DataAgent
    agent = DataAgent()
    total = await agent.execute("Quantas reservas temos?")
    popular = await agent.execute("Qual o destino mais popular?")
    return {
        "success": True,
        "total_bookings": total.get("results", []),
        "most_popular": popular.get("results", [])
    }


# ===== FINANCE TOOLS =====

@mcp.tool(name="convert_currency", description="Converte valores entre moedas")
async def convert_currency(amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
    """Converte moeda."""
    from src.agents.finance_agent import FinanceAgent
    agent = FinanceAgent()
    return await agent.execute(f"Converta {amount} {from_currency} para {to_currency}")


@mcp.tool(name="calculate_interest", description="Calcula juros")
async def calculate_interest(principal: float, rate: float, periods: int, compound: bool = True) -> Dict[str, Any]:
    """Calcula juros."""
    from src.agents.finance_agent import FinanceAgent
    agent = FinanceAgent()
    itype = "compostos" if compound else "simples"
    rpct = rate * 100
    return await agent.execute(f"Calcule juros {itype} de {principal} a {rpct}% por {periods} meses")


@mcp.tool(name="get_exchange_rate", description="Obtém taxa de câmbio")
async def get_exchange_rate(from_currency: str, to_currency: str) -> Dict[str, Any]:
    """Taxa de câmbio."""
    from src.agents.finance_agent import FinanceAgent
    agent = FinanceAgent()
    return await agent.execute(f"Qual a taxa de câmbio de {from_currency} para {to_currency}?")


# ===== RESOURCES =====

@mcp.resource(uri="prompts://system")
async def get_system_prompt() -> str:
    return """Assistente multi-agente com Weather, Data, Finance e Information agents."""


@mcp.resource(uri="prompts://routing")
async def get_routing_prompt() -> str:
    return """Roteia queries: clima->Weather, dados->Data, finanças->Finance, geral->Info."""


# ===== MAIN =====

async def main():
    logger.info("🚀 MCP Server Iniciando...")
    await mcp.run()


# USAR ISTO:
if __name__ == "__main__":
    mcp.run()

