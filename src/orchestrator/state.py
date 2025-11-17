"""Gerenciamento de estado para LangGraph"""

from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    """Estado do sistema multi-agente."""
    query: str
    messages: List[Dict[str, Any]]
    current_agent: str
    context: Dict[str, Any]
    results: List[Dict[str, Any]]
    final_answer: str
    error: str