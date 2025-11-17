#!/usr/bin/env python3
"""Interface CLI para o Sistema Multi-Agente"""

import asyncio
import sys
import os
from typing import Optional
import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.orchestrator.main import Orchestrator

console = Console()


async def process_single_query(orchestrator: Orchestrator, query: str):
    """Processa uma única query."""
    console.print(f"\n[bold blue]🤖 Processando:[/bold blue] {query}")
    
    result = await orchestrator.process_query(query)
    
    if result.get("success"):
        answer = result.get("answer", "Sem resposta")
        console.print(Panel(
            Markdown(answer),
            title="[bold green]✅ Resposta[/bold green]",
            border_style="green"
        ))
    else:
        error = result.get("error", "Erro desconhecido")
        console.print(Panel(
            f"[bold red]{error}[/bold red]",
            title="[bold red]❌ Erro[/bold red]",
            border_style="red"
        ))


async def interactive_mode(orchestrator: Orchestrator):
    """Modo interativo."""
    console.print(Panel(
        "[bold cyan]Super Agent - Sistema Multi-Agente[/bold cyan]\n\n"
        "Digite suas queries ou 'sair' para encerrar.",
        title="💬 Modo Interativo",
        border_style="cyan"
    ))
    
    while True:
        try:
            console.print("\n[bold yellow]>[/bold yellow]", end=" ")
            query = input().strip()
            
            if not query:
                continue
            
            if query.lower() in ["sair", "exit", "quit", "q"]:
                console.print("[bold green]👋 Até logo![/bold green]")
                break
            
            await process_single_query(orchestrator, query)
            
        except KeyboardInterrupt:
            console.print("\n[bold green]👋 Até logo![/bold green]")
            break
        except Exception as e:
            console.print(f"[bold red]❌ Erro: {str(e)}[/bold red]")


@click.command()
@click.argument('query', required=False)
@click.option('--interactive', '-i', is_flag=True, help='Modo interativo')
@click.option('--verbose', '-v', is_flag=True, help='Modo verbose')
def main(query: Optional[str], interactive: bool, verbose: bool):
    """Super Agent - Sistema Multi-Agente CLI
    
    Exemplos:
    
        # Query única
        python src/cli.py "Como está o clima em São Paulo?"
        
        # Modo interativo
        python src/cli.py --interactive
    """
    # Banner
    console.print(Panel(
        "[bold cyan]🤖 Super Agent[/bold cyan]\n"
        "Sistema Multi-Agente com LangGraph + MCP",
        border_style="blue"
    ))
    
    if verbose:
        os.environ["LOG_LEVEL"] = "DEBUG"
    
    async def run():
        orchestrator = Orchestrator()
        
        try:
            await orchestrator.start()
            
            if interactive:
                await interactive_mode(orchestrator)
            elif query:
                await process_single_query(orchestrator, query)
            else:
                console.print("[bold red]❌ Erro: Forneça uma query ou use --interactive[/bold red]")
                console.print("\nUso: python src/cli.py [QUERY] ou --interactive")
        
        finally:
            await orchestrator.stop()
    
    asyncio.run(run())


if __name__ == "__main__":
    main()