"""Orquestrador Principal do Sistema Multi-Agente"""

import asyncio
import logging
import os
from typing import Dict, Any

from src.agents.weather_agent import WeatherAgent
from src.agents.data_agent import DataAgent
from src.agents.finance_agent import FinanceAgent
from src.agents.info_agent import InformationAgent
from src.orchestrator.supervisor import Supervisor
from src.orchestrator.mcp_client import MCPClient

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Orchestrator:
    """Orquestrador central que coordena todos os agentes."""

    def __init__(self):
        logger.info("🎯 Inicializando Orquestrador...")
        
        # Inicializa supervisor
        self.supervisor = Supervisor()
        
        # Inicializa agentes
        self.agents = {
            "weather_agent": WeatherAgent(),
            "data_agent": DataAgent(),
            "finance_agent": FinanceAgent(),
            "info_agent": InformationAgent(),
        }
        
        # Inicializa MCP Client
        self.mcp_client = MCPClient(
            host=os.getenv("MCP_HOST", "127.0.0.1"),
            port=int(os.getenv("MCP_PORT", "8000"))
        )
        
        logger.info(f"✅ {len(self.agents)} agentes registrados")
        logger.info("✨ Orquestrador pronto")

    async def process_query(self, query: str) -> Dict[str, Any]:
        """Processa uma query do usuário.
        
        Args:
            query: Query/pergunta do usuário
            
        Returns:
            Resposta processada
        """
        logger.info(f"💬 Query recebida: {query}")
        
        try:
            # Roteia para agente apropriado
            agent_name = await self.supervisor.route_query(query)
            logger.info(f"🎯 Roteado para: {agent_name}")
            
            # Executa agente
            agent = self.agents.get(agent_name)
            if not agent:
                return {
                    "success": False,
                    "error": f"Agente {agent_name} não encontrado"
                }
            
            result = await agent.execute(query)
            logger.info(f"✅ Agente executado: {result.get('success')}")
            
            # Sintetiza resposta
            final_answer = await self.supervisor.synthesize_response([result])
            
            return {
                "success": True,
                "query": query,
                "agent": agent_name,
                "result": result,
                "answer": final_answer
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar query: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def start(self):
        """Inicia o orquestrador."""
        logger.info("🚀 Orquestrador iniciando...")
        try:
            await self.mcp_client.connect()
            logger.info("✅ Sistema pronto para receber queries")
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar: {e}")
            raise

    async def stop(self):
        """Para o orquestrador."""
        logger.info("🛑 Encerrando orquestrador...")
        await self.mcp_client.disconnect()


async def main():
    """Função principal."""
    orchestrator = Orchestrator()
    await orchestrator.start()
    
    # Exemplos de queries
    queries = [
        "Como está o clima em São Paulo?",
        "Quantas reservas temos no banco?",
        "Converta 1000 USD para BRL",
    ]
    
    for query in queries:
        print(f"\n{'='*60}")
        result = await orchestrator.process_query(query)
        print(f"Query: {query}")
        print(f"Resposta: {result.get('answer')}")
        print(f"{'='*60}")
    
    await orchestrator.stop()


if __name__ == "__main__":
    asyncio.run(main())