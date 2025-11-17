"""Testes para os agentes especializados"""

import pytest
import asyncio
from src.agents.weather_agent import WeatherAgent
from src.agents.data_agent import DataAgent
from src.agents.finance_agent import FinanceAgent
from src.agents.info_agent import InformationAgent


class TestWeatherAgent:
    """Testes do Weather Agent."""
    
    @pytest.mark.asyncio
    async def test_weather_query(self):
        agent = WeatherAgent()
        result = await agent.execute("Como está o clima em São Paulo?")
        assert result["success"] == True
        assert "city" in result
    
    def test_capabilities(self):
        agent = WeatherAgent()
        caps = agent.get_capabilities()
        assert len(caps) > 0
        assert "Consultar clima atual" in caps


class TestDataAgent:
    """Testes do Data Agent."""
    
    @pytest.mark.asyncio
    async def test_database_query(self):
        agent = DataAgent()
        result = await agent.execute("Quantas reservas temos?")
        assert "results" in result
    
    def test_capabilities(self):
        agent = DataAgent()
        caps = agent.get_capabilities()
        assert "Executar consultas SQL" in caps


class TestFinanceAgent:
    """Testes do Finance Agent."""
    
    @pytest.mark.asyncio
    async def test_currency_conversion(self):
        agent = FinanceAgent()
        result = await agent.execute("Converta 1000 USD para BRL")
        assert result["success"] == True
        assert "converted_amount" in result
    
    def test_capabilities(self):
        agent = FinanceAgent()
        caps = agent.get_capabilities()
        assert "Conversão de moedas" in caps


class TestInformationAgent:
    """Testes do Information Agent."""
    
    @pytest.mark.asyncio
    async def test_info_query(self):
        agent = InformationAgent()
        result = await agent.execute("O que é MCP?")
        assert result["success"] == True
    
    def test_capabilities(self):
        agent = InformationAgent()
        caps = agent.get_capabilities()
        assert "Responder perguntas gerais" in caps