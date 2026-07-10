# main.py
import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from utils.config import settings, logger
from agent import CodingAgent

app = typer.Typer()
console = Console()


@app.command()
def chat():
    """Start an interactive chat session with the Coding Agent."""
    console.print(Panel.fit(
        "[bold green]🤖 Autonomous Coding Agent[/bold green]\n"
        f"[cyan]Model:[/cyan] {settings.GROQ_MODEL}\n"
        "[dim]Type 'exit' or 'quit' to end the session.[/dim]",
        border_style="green"
    ))

    agent = CodingAgent()

    while True:
        try:
            user_input = console.input("\n[bold blue]You:[/bold blue] ")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Session ended.[/yellow]")
            break

        if user_input.strip().lower() in ("exit", "quit"):
            console.print("[yellow]👋 Goodbye![/yellow]")
            break

        if not user_input.strip():
            continue

        try:
            response = agent.run(user_input)
        except Exception as e:
            logger.error(f"Unexpected error in agent.run: {e}")
            console.print(f"[bold red]❌ Unexpected error:[/bold red] {e}")
            continue

        console.print("\n[bold green]Agent:[/bold green]")
        console.print(Markdown(response))


if __name__ == "__main__":
    app()