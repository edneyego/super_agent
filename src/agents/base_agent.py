"""Classe base para todos os agentes do sistema"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging


class BaseAgent(ABC):
    """Classe abstrata base para agentes especializados."""

    def __init__(self, name: str, description: str):
        """Inicializa o agente base.
        
        Args:
            name: Nome identificador do agente
            description: Descrição das capacidades do agente
        """
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"agent.{name}")
        self.logger.info(f"Agente {name} inicializado")

    @abstractmethod
    async def execute(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Executa a query do agente.
        
        Args:
            query: Query/pergunta do usuário
            context: Contexto adicional (opcional)
            
        Returns:
            Dicionário com resultado da execução
        """
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Retorna lista de capacidades do agente.
        
        Returns:
            Lista de strings descrevendo capacidades
        """
        pass

    def __str__(self) -> str:
        return f"Agent({self.name}): {self.description}"

    def __repr__(self) -> str:
        return f"<BaseAgent name={self.name}>"