"""Agente especializado em informações gerais"""

from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent


class InformationAgent(BaseAgent):
    """Agente especializado em informações gerais e explicações conceituais."""

    def __init__(self):
        super().__init__(
            name="info_agent",
            description="Especialista em informações gerais e explicações conceituais"
        )
        
        # Base de conhecimento simples
        self.knowledge_base = {
            "arquitetura hexagonal": {
                "definition": "Arquitetura Hexagonal (ou Ports and Adapters) é um padrão arquitetural que promove o isolamento do domínio da aplicação das dependências externas.",
                "key_concepts": [
                    "Core da aplicação isolado",
                    "Portas (interfaces) para comunicação",
                    "Adaptadores implementam as portas",
                    "Fácil teste e manutenção"
                ],
                "benefits": [
                    "Testabilidade",
                    "Manutenção simplificada",
                    "Independência de frameworks",
                    "Flexibilidade"
                ]
            },
            "mcp": {
                "definition": "Model Context Protocol (MCP) é um protocolo aberto que padroniza como as aplicações fornecem contexto para LLMs.",
                "key_concepts": [
                    "Protocolo padronizado",
                    "Integração LLM-aplicação",
                    "Ferramentas e recursos",
                    "Cliente-servidor"
                ],
                "benefits": [
                    "Interoperabilidade",
                    "Reusabilidade",
                    "Segurança",
                    "Escalabilidade"
                ]
            },
            "langgraph": {
                "definition": "LangGraph é uma biblioteca para construir aplicações multi-agente com grafos de estados usando LLMs.",
                "key_concepts": [
                    "Grafos de estados",
                    "Nós (agentes)",
                    "Arestas (transições)",
                    "Orquestração de agentes"
                ],
                "benefits": [
                    "Workflows complexos",
                    "Coordenação de agentes",
                    "Estado persistente",
                    "Flexível e extensível"
                ]
            },
            "multi-agente": {
                "definition": "Sistema multi-agente é uma arquitetura onde múltiplos agentes autônomos colaboram para resolver problemas complexos.",
                "key_concepts": [
                    "Agentes especializados",
                    "Comunicação entre agentes",
                    "Orquestrador central",
                    "Especialização de domínio"
                ],
                "benefits": [
                    "Modularidade",
                    "Especialização",
                    "Escalabilidade",
                    "Manutenção facilitada"
                ]
            }
        }

    def get_capabilities(self) -> List[str]:
        return [
            "Responder perguntas gerais",
            "Explicar conceitos",
            "Fornecer informações contextuais",
            "Definir termos técnicos",
            "Educar sobre tópicos diversos"
        ]

    async def execute(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fornece informações sobre tópicos diversos.
        
        Args:
            query: Query do usuário
            context: Contexto adicional
            
        Returns:
            Dicionário com informações
        """
        try:
            query_lower = query.lower()
            
            # Busca no knowledge base
            for topic, info in self.knowledge_base.items():
                if topic in query_lower:
                    return {
                        "success": True,
                        "agent": self.name,
                        "topic": topic,
                        "information": info
                    }
            
            # Resposta genérica se não encontrar
            return {
                "success": True,
                "agent": self.name,
                "topic": "general",
                "information": {
                    "definition": "Sou o Information Agent, especializado em fornecer informações sobre diversos tópicos.",
                    "available_topics": list(self.knowledge_base.keys()),
                    "suggestion": "Pergunte sobre algum dos tópicos disponíveis para obter informações detalhadas."
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar informações: {str(e)}")
            return {
                "success": False,
                "agent": self.name,
                "error": str(e)
            }