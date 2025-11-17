"""
MCP Server - Servidor FastMCP puro para Sistema Multi-Agente
"""
import asyncio
import logging
from pathlib import Path
from fastmcp import FastMCP

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializa FastMCP (sem description)
mcp = FastMCP(
    name="Super Agent MCP Server",
    version="1.0.0"
)

# Importar ferramentas
from mcp.tools.weather import weather_tools
from mcp.tools.database import database_tools
from mcp.tools.finance import finance_tools

logger.info("✅ MCP Server configurado com todas as ferramentas")

async def main():
    """
    Função principal que inicia o servidor MCP
    """
    logger.info("🚀 MCP Server Iniciando...")
    
    try:
        # Use run_async() ao invés de run() para evitar conflito de event loop
        await mcp.run_async(transport="stdio")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar MCP Server: {e}")
        raise

if __name__ == "__main__":
    # Use asyncio.run() apenas aqui, não dentro do servidor
    asyncio.run(main())
