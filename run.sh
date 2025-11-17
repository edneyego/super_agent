#!/bin/bash

# Super Agent - Script de Execução (Standalone Mode)
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
mkdir -p logs

# Verifica modo de execução
MODE="${1:-cli}"

case "$MODE" in
    "cli")
        log_info "Modo: CLI - Executando query única"
        if [ -z "$2" ]; then
            log_error "Uso: $0 cli 'Sua pergunta aqui'"
            exit 1
        fi
        
        log_info "Query: $2"
        python src/cli.py "$2"
        ;;
        
    "interactive")
        log_info "Modo: Interativo"
        python src/cli.py --interactive
        ;;
        
    "test")
        log_info "Modo: Teste - Executando queries de exemplo"
        echo ""
        
        log_info "Teste 1: Weather Agent"
        python src/cli.py "Como está o clima em São Paulo?"
        echo ""
        
        log_info "Teste 2: Information Agent"
        python src/cli.py "O que é um sistema multi-agente?"
        echo ""
        
        log_success "Testes concluídos!"
        ;;
        
    "server")
        log_info "Modo: MCP Server - Iniciando servidor standalone"
        log_warning "Servidor MCP em modo STDIO. Use um cliente MCP para conectar."
        python src/mcp/server.py
        ;;
        
    *)
        log_error "Modo desconhecido: $MODE"
        echo ""
        echo "Uso:"
        echo "  $0 cli 'Sua pergunta'    - Executa uma query"
        echo "  $0 interactive           - Modo interativo"
        echo "  $0 test                  - Executa testes"
        echo "  $0 server                - Inicia MCP Server"
        exit 1
        ;;
esac

log_success "Concluído!"
