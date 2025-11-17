"""Agente especializado em operações financeiras"""

from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent


class FinanceAgent(BaseAgent):
    """Agente especializado em operações financeiras e cálculos monetários."""

    def __init__(self):
        super().__init__(
            name="finance_agent",
            description="Especialista em operações financeiras e cálculos monetários"
        )
        # Taxas de câmbio simples (em produção, usar API real)
        self.exchange_rates = {
            "USD": {"BRL": 5.0, "EUR": 0.92},
            "BRL": {"USD": 0.20, "EUR": 0.18},
            "EUR": {"USD": 1.09, "BRL": 5.45}
        }

    def get_capabilities(self) -> List[str]:
        return [
            "Conversão de moedas",
            "Cálculo de juros compostos",
            "Cálculo de juros simples",
            "Operações financeiras",
            "Taxas de câmbio"
        ]

    async def execute(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Executa operação financeira.
        
        Args:
            query: Query do usuário
            context: Contexto adicional
            
        Returns:
            Dicionário com resultado da operação
        """
        try:
            query_lower = query.lower()
            
            # Conversão de moeda
            if "convert" in query_lower or "converta" in query_lower or "converter" in query_lower:
                return await self._handle_currency_conversion(query)
            
            # Taxa de câmbio
            elif "taxa" in query_lower and "câmbio" in query_lower:
                return await self._handle_exchange_rate(query)
            
            # Juros
            elif "juros" in query_lower or "interest" in query_lower:
                return await self._handle_interest_calculation(query)
            
            else:
                return {
                    "success": False,
                    "agent": self.name,
                    "error": "Operação financeira não reconhecida"
                }
            
        except Exception as e:
            self.logger.error(f"Erro em operação financeira: {str(e)}")
            return {
                "success": False,
                "agent": self.name,
                "error": str(e)
            }

    async def _handle_currency_conversion(self, query: str) -> Dict[str, Any]:
        """Converte valores entre moedas."""
        import re
        
        # Extrai valor e moedas da query
        # Exemplo: "Converta 1000 USD para BRL"
        match = re.search(r'(\d+(?:\.\d+)?)\s*(USD|BRL|EUR)\s*para\s*(USD|BRL|EUR)', query, re.IGNORECASE)
        
        if not match:
            return {
                "success": False,
                "agent": self.name,
                "error": "Não foi possível extrair valor e moedas da query"
            }
        
        amount = float(match.group(1))
        from_currency = match.group(2).upper()
        to_currency = match.group(3).upper()
        
        # Busca taxa de câmbio
        if from_currency == to_currency:
            converted = amount
            rate = 1.0
        else:
            rate = self.exchange_rates.get(from_currency, {}).get(to_currency, 1.0)
            converted = amount * rate
        
        return {
            "success": True,
            "agent": self.name,
            "operation": "currency_conversion",
            "original_amount": amount,
            "converted_amount": round(converted, 2),
            "from_currency": from_currency,
            "to_currency": to_currency,
            "exchange_rate": rate
        }

    async def _handle_exchange_rate(self, query: str) -> Dict[str, Any]:
        """Retorna taxa de câmbio."""
        query_upper = query.upper()
        
        # Detecta moedas mencionadas
        currencies = []
        for currency in ["USD", "BRL", "EUR"]:
            if currency in query_upper:
                currencies.append(currency)
        
        if len(currencies) < 2:
            currencies = ["USD", "BRL"]  # Padrão
        
        from_curr = currencies[0]
        to_curr = currencies[1]
        
        rate = self.exchange_rates.get(from_curr, {}).get(to_curr, 1.0)
        
        return {
            "success": True,
            "agent": self.name,
            "operation": "exchange_rate",
            "from_currency": from_curr,
            "to_currency": to_curr,
            "rate": rate,
            "info": f"1 {from_curr} = {rate} {to_curr}"
        }

    async def _handle_interest_calculation(self, query: str) -> Dict[str, Any]:
        """Calcula juros simples ou compostos."""
        import re
        
        # Extrai valores da query
        # Exemplo: "Calcule juros compostos de 10000 a 0.5% por 12 meses"
        
        # Busca principal
        principal_match = re.search(r'(\d+(?:\.\d+)?)', query)
        principal = float(principal_match.group(1)) if principal_match else 1000.0
        
        # Busca taxa
        rate_match = re.search(r'(\d+(?:\.\d+)?)%', query)
        rate = float(rate_match.group(1)) / 100 if rate_match else 0.01
        
        # Busca período
        period_match = re.search(r'(\d+)\s*(meses|anos|mes|ano)', query)
        if period_match:
            periods = int(period_match.group(1))
            unit = period_match.group(2)
            if "ano" in unit:
                periods = periods * 12  # Converte para meses
        else:
            periods = 12
        
        # Determina se é juros compostos ou simples
        is_compound = "compostos" in query.lower() or "compound" in query.lower()
        
        if is_compound:
            # Fórmula juros compostos: M = C * (1 + i)^n
            final_amount = principal * ((1 + rate) ** periods)
            interest = final_amount - principal
        else:
            # Fórmula juros simples: J = C * i * n
            interest = principal * rate * periods
            final_amount = principal + interest
        
        return {
            "success": True,
            "agent": self.name,
            "operation": "interest_calculation",
            "type": "compound" if is_compound else "simple",
            "principal": round(principal, 2),
            "rate": rate,
            "periods": periods,
            "interest": round(interest, 2),
            "final_amount": round(final_amount, 2)
        }