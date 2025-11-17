"""Supervisor LangGraph para orquestração de agentes"""

import os
import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

logger = logging.getLogger(__name__)


class Supervisor:
    """Supervisor que roteia queries para agentes apropriados."""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai")
        self.model_name = os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.api_key = os.getenv("LLM_API_KEY")
        
        if not self.api_key:
            raise ValueError("LLM_API_KEY não configurada")
        
        self.llm = self._initialize_llm()
        logger.info(f"Supervisor inicializado com {self.provider}/{self.model_name}")

    def _initialize_llm(self):
        """Inicializa LLM baseado no provider."""
        if self.provider == "openai":
            return ChatOpenAI(
                model=self.model_name,
                api_key=self.api_key,
                temperature=0
            )
        elif self.provider == "google":
            return ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=self.api_key,
                temperature=0
            )
        elif self.provider == "anthropic":
            return ChatAnthropic(
                model=self.model_name,
                anthropic_api_key=self.api_key,
                temperature=0
            )
        else:
            raise ValueError(f"Provider não suportado: {self.provider}")

    async def route_query(self, query: str) -> str:
        """Roteia query para agente apropriado."""
        query_lower = query.lower()
        
        # Roteamento baseado em keywords
        if any(word in query_lower for word in ["clima", "tempo", "temperatura", "weather", "previsão"]):
            return "weather_agent"
        
        elif any(word in query_lower for word in ["banco", "database", "reserva", "dados", "query"]):
            return "data_agent"
        
        elif any(word in query_lower for word in ["moeda", "currency", "convert", "juros", "câmbio"]):
            return "finance_agent"
        
        else:
            return "info_agent"

    async def synthesize_response(self, results: list) -> str:
        """Sintetiza resposta final a partir dos resultados dos agentes."""
        if not results:
            return "Não foi possível processar a query."
        
        # Formata resposta baseada nos resultados
        response_parts = []
        
        for result in results:
            if result.get("success"):
                agent = result.get("agent", "unknown")
                
                if agent == "weather_agent":
                    data = result.get("data", {})
                    city = result.get("city", "")
                    response_parts.append(
                        f"🌤️ Clima em {city}: {data.get('temperature')}°C, "
                        f"{data.get('condition')}, Umidade: {data.get('humidity')}%"
                    )
                
                elif agent == "data_agent":
                    results_data = result.get("results", [])
                    if results_data:
                        response_parts.append(f"📊 Dados: {results_data}")
                
                elif agent == "finance_agent":
                    operation = result.get("operation", "")
                    if operation == "currency_conversion":
                        response_parts.append(
                            f"💰 {result.get('original_amount')} {result.get('from_currency')} = "
                            f"{result.get('converted_amount')} {result.get('to_currency')}"
                        )
                    elif operation == "interest_calculation":
                        response_parts.append(
                            f"💵 Juros: {result.get('interest')}, "
                            f"Total: {result.get('final_amount')}"
                        )
                
                elif agent == "info_agent":
                    info = result.get("information", {})
                    response_parts.append(f"📖 {info.get('definition', 'Info')}")
            else:
                error = result.get("error", "Erro desconhecido")
                response_parts.append(f"❌ Erro: {error}")
        
        return "\n\n".join(response_parts) if response_parts else "Sem resultados."