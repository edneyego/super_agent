"""Testes do Orquestrador"""

import pytest
from src.orchestrator.supervisor import Supervisor
from src.orchestrator.mcp_client import MCPClient


class TestSupervisor:
    """Testes do Supervisor."""
    
    @pytest.mark.asyncio
    async def test_route_weather(self):
        supervisor = Supervisor()
        agent = await supervisor.route_query("Como está o clima?")
        assert agent == "weather_agent"
    
    @pytest.mark.asyncio
    async def test_route_data(self):
        supervisor = Supervisor()
        agent = await supervisor.route_query("Quantas reservas?")
        assert agent == "data_agent"
    
    @pytest.mark.asyncio
    async def test_route_finance(self):
        supervisor = Supervisor()
        agent = await supervisor.route_query("Converta moeda")
        assert agent == "finance_agent"


class TestMCPClient:
    """Testes do MCP Client."""
    
    @pytest.mark.asyncio
    async def test_connection(self):
        client = MCPClient()
        await client.connect()
        assert client.connected == True
    
    @pytest.mark.asyncio
    async def test_list_tools(self):
        client = MCPClient()
        tools = await client.list_tools()
        assert len(tools) > 0