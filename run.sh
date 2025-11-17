#!/bin/bash

# Super Agent - Script de Execução
# Autor: Edney Oliveira

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções de log
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Banner
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║         Super Agent - Sistema Multi-Agente             ║
║              LangGraph + MCP Protocol                  ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Verifica se .env existe
if [ ! -f ".env" ]; then
    log_error "Arquivo .env não encontrado!"
    log_info "Copiando .env.example para .env..."
    cp .env.example .env
    log_warning "Configure o arquivo .env com suas credenciais antes de continuar!"
    exit 1
fi

# Carrega variáveis de ambiente
log_info "Carregando variáveis de ambiente..."
source .env

# Verifica se LLM_API_KEY está configurada
if [ -z "$LLM_API_KEY" ] || [ "$LLM_API_KEY" = "your_api_key_here" ]; then
    log_error "LLM_API_KEY não configurada em .env!"
    log_info "Configure sua chave de API do OpenAI/Google/Anthropic em .env"
    exit 1
fi

log_success "Configurações carregadas"

# Cria diretório de logs se não existir
if [ ! -d "logs" ]; then
    log_info "Criando diretório de logs..."
    mkdir -p logs
fi

# Função para cleanup
cleanup() {
    log_info "Encerrando processos..."
    if [ ! -z "$MCP_PID" ]; then
        kill $MCP_PID 2>/dev/null || true
        log_success "MCP Server encerrado"
    fi
    if [ ! -z "$ORCH_PID" ]; then
        kill $ORCH_PID 2>/dev/null || true
        log_success "Orquestrador encerrado"
    fi
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar MCP Server
log_info "Iniciando MCP Server..."
python src/mcp/server.py > logs/mcp_server.log 2>&1 &
MCP_PID=$!
log_success "MCP Server iniciado (PID: $MCP_PID)"

# Aguarda MCP Server estar pronto
log_info "Aguardando MCP Server ficar pronto..."
sleep 3

# Verifica se MCP Server está rodando
if ! ps -p $MCP_PID > /dev/null; then
    log_error "MCP Server falhou ao iniciar!"
    log_info "Veja os logs em: logs/mcp_server.log"
    cat logs/mcp_server.log
    exit 1
fi

log_success "MCP Server pronto"

# Iniciar Orquestrador
log_info "Iniciando Orquestrador..."
python src/orchestrator/main.py > logs/orchestrator.log 2>&1 &
ORCH_PID=$!
log_success "Orquestrador iniciado (PID: $ORCH_PID)"

# Aguarda Orquestrador estar pronto
log_info "Aguardando Orquestrador ficar pronto..."
sleep 3

# Verifica se Orquestrador está rodando
if ! ps -p $ORCH_PID > /dev/null; then
    log_error "Orquestrador falhou ao iniciar!"
    log_info "Veja os logs em: logs/orchestrator.log"
    cat logs/orchestrator.log
    cleanup
    exit 1
fi

log_success "Orquestrador pronto"

echo ""
log_success "✨ Sistema iniciado com sucesso! ✨"
echo ""
log_info "Componentes rodando:"
echo "  - MCP Server (PID: $MCP_PID)"
echo "  - Orquestrador (PID: $ORCH_PID)"
echo ""
log_info "Para interagir com o sistema, use:"
echo "  python src/cli.py 'Sua pergunta aqui'"
echo "  ou"
echo "  python src/cli.py --interactive"
echo ""
log_info "Logs disponíveis em:"
echo "  - MCP Server: logs/mcp_server.log"
echo "  - Orquestrador: logs/orchestrator.log"
echo ""
log_warning "Pressione Ctrl+C para encerrar o sistema"
echo ""

# Exemplos de queries
log_info "Executando queries de teste..."
echo ""

log_info "Teste 1: Weather Agent"
python src/cli.py "Como está o clima em São Paulo?"
echo ""

log_info "Teste 2: Data Agent"
python src/cli.py "Quantas reservas temos no banco de dados?"
echo ""

log_info "Teste 3: Finance Agent"
python src/cli.py "Converta 1000 USD para BRL"
echo ""

log_success "Testes concluídos!"
echo ""

# Mantém script rodando
log_info "Sistema em execução. Pressione Ctrl+C para encerrar."
wait