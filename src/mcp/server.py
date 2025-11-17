"""
MCP Server - Servidor FastMCP puro para Sistema Multi-Agente
"""
import asyncio
import logging
import sys
from pathlib import Path
from fastmcp import FastMCP

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializa FastMCP (sem description)
mcp = FastMCP(
    name="Super Agent MCP Server",
    version="1.0.0"
)

logger.info("✅ MCP Server configurado")

# ============================================================================
# FERRAMENTAS MCP - Definidas diretamente aqui
# ============================================================================

@mcp.tool()
def get_weather(city: str, country: str = "BR") -> dict:
    """
    Obtém informações de clima para uma cidade.
    
    Args:
        city: Nome da cidade
        country: Código do país (padrão: BR)
    
    Returns:
        Dicionário com informações do clima
    """
    import requests
    
    try:
        # Geocoding para obter coordenadas
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=pt&format=json"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            return {"error": f"Cidade {city} não encontrada"}
        
        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]
        
        # Obter clima
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=America/Sao_Paulo"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        return {
            "city": city,
            "temperature": weather_data["current"]["temperature_2m"],
            "humidity": weather_data["current"]["relative_humidity_2m"],
            "wind_speed": weather_data["current"]["wind_speed_10m"],
            "unit": "°C"
        }
    except Exception as e:
        logger.error(f"Erro ao obter clima: {e}")
        return {"error": str(e)}


@mcp.tool()
def query_database(sql: str) -> dict:
    """
    Executa uma query SQL no banco de dados.
    
    Args:
        sql: Query SQL a ser executada (apenas SELECT)
    
    Returns:
        Resultado da query
    """
    import sqlite3
    
    try:
        # Validar que é apenas SELECT
        if not sql.strip().upper().startswith("SELECT"):
            return {"error": "Apenas queries SELECT são permitidas"}
        
        # Conectar ao banco
        db_path = Path(__file__).parent.parent.parent / "data" / "database.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Executar query
        cursor.execute(sql)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        conn.close()
        
        return {
            "columns": columns,
            "rows": results,
            "count": len(results)
        }
    except Exception as e:
        logger.error(f"Erro ao executar query: {e}")
        return {"error": str(e)}


@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """
    Converte valores entre moedas.
    
    Args:
        amount: Valor a ser convertido
        from_currency: Moeda de origem (ex: USD)
        to_currency: Moeda de destino (ex: BRL)
    
    Returns:
        Resultado da conversão
    """
    import requests
    
    try:
        # API de taxas de câmbio
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
        response = requests.get(url)
        data = response.json()
        
        if to_currency.upper() not in data["rates"]:
            return {"error": f"Moeda {to_currency} não encontrada"}
        
        rate = data["rates"][to_currency.upper()]
        converted_amount = amount * rate
        
        return {
            "amount": amount,
            "from_currency": from_currency.upper(),
            "to_currency": to_currency.upper(),
            "rate": rate,
            "converted_amount": round(converted_amount, 2)
        }
    except Exception as e:
        logger.error(f"Erro ao converter moeda: {e}")
        return {"error": str(e)}


@mcp.tool()
def calculate_compound_interest(
    principal: float,
    rate: float,
    periods: int
) -> dict:
    """
    Calcula juros compostos.
    
    Args:
        principal: Valor principal/inicial
        rate: Taxa de juros por período (em decimal, ex: 0.05 para 5%)
        periods: Número de períodos
    
    Returns:
        Resultado do cálculo
    """
    try:
        final_amount = principal * ((1 + rate) ** periods)
        interest_earned = final_amount - principal
        
        return {
            "principal": principal,
            "rate": rate,
            "periods": periods,
            "final_amount": round(final_amount, 2),
            "interest_earned": round(interest_earned, 2)
        }
    except Exception as e:
        logger.error(f"Erro ao calcular juros: {e}")
        return {"error": str(e)}


logger.info("✅ Ferramentas MCP registradas")

# ============================================================================
# SERVIDOR MCP
# ============================================================================

async def main():
    """
    Função principal que inicia o servidor MCP
    """
    logger.info("🚀 MCP Server Iniciando...")
    
    try:
        # Use run_async() ao invés de run() para evitar conflito de event loop
        await mcp.run_async(transport="stdio")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar MCP Server: {e}")
        raise


if __name__ == "__main__":
    # Use asyncio.run() apenas aqui, não dentro do servidor
    asyncio.run(main())
