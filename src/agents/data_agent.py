"""Agente especializado em consultas ao banco de dados"""

import os
import sqlite3
from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent


class DataAgent(BaseAgent):
    """Agente especializado em consultas e análise de dados."""

    def __init__(self):
        super().__init__(
            name="data_agent",
            description="Especialista em consultas e análise de dados do banco de dados"
        )
        self.db_path = os.getenv("DATABASE_PATH", "travel_agency.db")

    def get_capabilities(self) -> List[str]:
        return [
            "Executar consultas SQL",
            "Analisar dados de reservas",
            "Gerar estatísticas",
            "Criar relatórios",
            "Consultar banco de dados"
        ]

    async def execute(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Executa consulta ao banco de dados.
        
        Args:
            query: Query do usuário
            context: Contexto adicional
            
        Returns:
            Dicionário com resultados da consulta
        """
        try:
            # Determina tipo de consulta
            sql_query = self._generate_sql(query)
            
            if not sql_query:
                return {
                    "success": False,
                    "agent": self.name,
                    "error": "Não foi possível gerar consulta SQL"
                }

            # Executa consulta
            results = self._execute_query(sql_query)
            
            return {
                "success": True,
                "agent": self.name,
                "query": sql_query,
                "results": results
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao consultar banco: {str(e)}")
            return {
                "success": False,
                "agent": self.name,
                "error": str(e)
            }

    def _generate_sql(self, query: str) -> str:
        """Gera SQL baseado na query do usuário."""
        query_lower = query.lower()
        
        # Padrões comuns de consultas
        if "quantas reservas" in query_lower or "total" in query_lower:
            return "SELECT COUNT(*) as total FROM travel_bookings"
        
        elif "destino mais popular" in query_lower or "mais vendido" in query_lower:
            return """
                SELECT destination, COUNT(*) as count 
                FROM travel_bookings 
                GROUP BY destination 
                ORDER BY count DESC 
                LIMIT 1
            """
        
        elif "últimas" in query_lower and "reservas" in query_lower:
            # Extrai número se houver (ex: "últimas 5 reservas")
            import re
            match = re.search(r'(\d+)', query)
            limit = int(match.group(1)) if match else 5
            
            return f"""
                SELECT customer_name, destination, booking_date 
                FROM travel_bookings 
                ORDER BY booking_date DESC 
                LIMIT {limit}
            """
        
        elif "reservas para" in query_lower:
            # Extrai destino
            parts = query_lower.split("para")
            if len(parts) > 1:
                destination = parts[1].strip()
                return f"""
                    SELECT customer_name, booking_date 
                    FROM travel_bookings 
                    WHERE LOWER(destination) LIKE '%{destination}%'
                """
        
        elif "cliente" in query_lower and "mais reservas" in query_lower:
            return """
                SELECT customer_name, COUNT(*) as bookings 
                FROM travel_bookings 
                GROUP BY customer_name 
                ORDER BY bookings DESC 
                LIMIT 1
            """
        
        # Consulta padrão
        return "SELECT * FROM travel_bookings LIMIT 10"

    def _execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """Executa query SQL e retorna resultados."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            # Converte para lista de dicionários
            results = [
                {key: row[key] for key in row.keys()}
                for row in rows
            ]
            
            return results
            
        finally:
            conn.close()