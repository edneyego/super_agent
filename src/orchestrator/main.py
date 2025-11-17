"""
Orchestrator Main - Orquestrador LangGraph para Sistema Multi-Agente
"""
import asyncio
import logging
import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# Importar agentes
from agents.base import AgentState
from agents.weather import WeatherAgent
from agents.data import DataAgent
from agents.finance import FinanceAgent
from agents.information import InformationAgent


def get_llm():
    """Configura e retorna o LLM baseado nas variáveis de ambiente"""
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    
    if not api_key:
        raise ValueError("LLM_API_KEY não configurada no .env")
    
    logger.info(f"✅ Configurando LLM: {provider} - {model}")
    
    if provider == "openai":
        return ChatOpenAI(api_key=api_key, model=model, temperature=0)
    elif provider == "anthropic":
        return ChatAnthropic(api_key=api_key, model=model, temperature=0)
    elif provider == "google":
        return ChatGoogleGenerativeAI(api_key=api_key, model=model, temperature=0)
    else:
        raise ValueError(f"Provider não suportado: {provider}")


def create_supervisor_node(llm):
    """Cria o nó supervisor que decide qual agente usar"""
    async def supervisor(state: AgentState) -> Dict[str, Any]:
        query = state.get("query", "")
        logger.info(f"🧠 Supervisor analisando query: {query}")
        
        prompt = f"""Você é um supervisor que coordena agentes especializados.

Query do usuário: {query}

Agentes disponíveis:
- weather_agent: Para consultas sobre clima, temperatura, previsão do tempo
- data_agent: Para consultas sobre dados, banco de dados, reservas, estatísticas
- finance_agent: Para conversão de moedas, cálculos financeiros, juros
- information_agent: Para perguntas gerais, explicações, informações diversas

Analise a query e responda APENAS com o nome do agente mais apropriado.
Resposta (apenas o nome do agente):"""

        response = await llm.ainvoke(prompt)
        agent_name = response.content.strip().lower()
        
        valid_agents = ["weather_agent", "data_agent", "finance_agent", "information_agent"]
        if agent_name not in valid_agents:
            agent_name = "information_agent"
        
        logger.info(f"👉 Roteando para: {agent_name}")
        
        return {
            "next_agent": agent_name,
            "messages": state.get("messages", []) + [{"supervisor": f"Roteando para {agent_name}"}]
        }
    
    return supervisor


def create_orchestrator():
    """Cria o grafo de orquestração do LangGraph"""
    logger.info("🏗️  Criando orquestrador LangGraph...")
    
    llm = get_llm()
    
    weather_agent = WeatherAgent()
    data_agent = DataAgent()
    finance_agent = FinanceAgent()
    information_agent = InformationAgent()
    
    supervisor = create_supervisor_node(llm)
    
    workflow = StateGraph(AgentState)
    
    workflow.add_node("supervisor", supervisor)
    workflow.add_node("weather_agent", weather_agent.execute)
    workflow.add_node("data_agent", data_agent.execute)
    workflow.add_node("finance_agent", finance_agent.execute)
    workflow.add_node("information_agent", information_agent.execute)
    
    workflow.set_entry_point("supervisor")
    
    def route_to_agent(state: AgentState) -> str:
        return state.get("next_agent", "information_agent")
    
    workflow.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {
            "weather_agent": "weather_agent",
            "data_agent": "data_agent",
            "finance_agent": "finance_agent",
            "information_agent": "information_agent"
        }
    )
    
    workflow.add_edge("weather_agent", END)
    workflow.add_edge("data_agent", END)
    workflow.add_edge("finance_agent", END)
    workflow.add_edge("information_agent", END)
    
    app = workflow.compile()
    
    logger.info("✅ Orquestrador criado com sucesso!")
    return app


async def process_query(query: str) -> str:
    """Processa uma query através do orquestrador"""
    logger.info(f"📥 Processando query: {query}")
    
    orchestrator = create_orchestrator()
    
    initial_state = {
        "query": query,
        "messages": [],
        "result": None,
        "next_agent": None
    }
    
    result = await orchestrator.ainvoke(initial_state)
    
    final_result = result.get("result", "Sem resultado")
    logger.info(f"✅ Resultado: {final_result}")
    
    return final_result


async def main():
    """Função principal do orquestrador"""
    logger.info("🚀 Orquestrador LangGraph Iniciando...")
    
    try:
        query = os.getenv("TEST_QUERY", "Como está o clima em São Paulo?")
        result = await process_query(query)
        print(f"\n📊 Resultado: {result}\n")
        
    except Exception as e:
        logger.error(f"❌ Erro no orquestrador: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
