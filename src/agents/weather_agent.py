"""Agente especializado em informações meteorológicas"""

import os
import httpx
from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent


class WeatherAgent(BaseAgent):
    """Agente especializado em consultas de clima e previsão do tempo."""

    def __init__(self):
        super().__init__(
            name="weather_agent",
            description="Especialista em informações meteorológicas e previsão do tempo"
        )
        self.api_base_url = os.getenv(
            "WEATHER_API_BASE_URL",
            "https://api.open-meteo.com/v1/forecast"
        )
        self.city_coordinates = {
            "são paulo": {"lat": -23.5505, "lon": -46.6333},
            "rio de janeiro": {"lat": -22.9068, "lon": -43.1729},
            "belo horizonte": {"lat": -19.9167, "lon": -43.9345},
            "brasília": {"lat": -15.7939, "lon": -47.8828},
            "curitiba": {"lat": -25.4284, "lon": -49.2733},
            "porto alegre": {"lat": -30.0346, "lon": -51.2177},
            "salvador": {"lat": -12.9714, "lon": -38.5014},
            "fortaleza": {"lat": -3.7172, "lon": -38.5433},
            "recife": {"lat": -8.0476, "lon": -34.8770},
            "manaus": {"lat": -3.1190, "lon": -60.0217},
        }

    def get_capabilities(self) -> List[str]:
        return [
            "Consultar clima atual",
            "Obter previsão do tempo",
            "Informar temperatura",
            "Informar condições meteorológicas",
            "Dados de umidade e vento"
        ]

    async def execute(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Executa consulta de clima.
        
        Args:
            query: Query do usuário (ex: "Como está o clima em São Paulo?")
            context: Contexto adicional
            
        Returns:
            Dicionário com dados meteorológicos
        """
        try:
            # Extrai cidade da query
            city = self._extract_city(query)
            
            if not city:
                return {
                    "success": False,
                    "agent": self.name,
                    "error": "Não foi possível identificar a cidade na query"
                }

            # Busca clima
            weather_data = await self._get_weather(city)
            
            return {
                "success": True,
                "agent": self.name,
                "city": city,
                "data": weather_data
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao consultar clima: {str(e)}")
            return {
                "success": False,
                "agent": self.name,
                "error": str(e)
            }

    def _extract_city(self, query: str) -> str:
        """Extrai nome da cidade da query."""
        query_lower = query.lower()
        
        for city in self.city_coordinates.keys():
            if city in query_lower:
                return city.title()
        
        return None

    async def _get_weather(self, city: str) -> Dict[str, Any]:
        """Busca dados meteorológicos da API."""
        city_lower = city.lower()
        
        if city_lower not in self.city_coordinates:
            raise ValueError(f"Cidade {city} não suportada")
        
        coords = self.city_coordinates[city_lower]
        
        params = {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": "America/Sao_Paulo"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.api_base_url, params=params)
            response.raise_for_status()
            data = response.json()
        
        current = data.get("current", {})
        
        return {
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "weather_code": current.get("weather_code"),
            "condition": self._get_weather_condition(current.get("weather_code", 0)),
            "units": {
                "temperature": "°C",
                "humidity": "%",
                "wind_speed": "km/h"
            }
        }

    def _get_weather_condition(self, code: int) -> str:
        """Converte código de clima em descrição."""
        conditions = {
            0: "Céu limpo",
            1: "Principalmente limpo",
            2: "Parcialmente nublado",
            3: "Nublado",
            45: "Nevoeiro",
            48: "Nevoeiro com gelo",
            51: "Chuvisco leve",
            53: "Chuvisco moderado",
            55: "Chuvisco denso",
            61: "Chuva leve",
            63: "Chuva moderada",
            65: "Chuva forte",
            71: "Neve leve",
            73: "Neve moderada",
            75: "Neve forte",
            80: "Pancadas de chuva leves",
            81: "Pancadas de chuva moderadas",
            82: "Pancadas de chuva fortes",
            95: "Tempestade",
            96: "Tempestade com granizo leve",
            99: "Tempestade com granizo forte"
        }
        return conditions.get(code, "Desconhecido")