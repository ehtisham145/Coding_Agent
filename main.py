# main.py
import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from utils.config import settings, logger
from agent import CodingAgent

app = typer.Typer()
console = Console()

def get_user_input(console: Console) -> str:
    """Supports both single-line and multiline (triple-quote) input."""
    first_line = console.input("\n[bold blue]You:[/bold blue] ")

    # If user starts multiline mode with triple quotes
    if first_line.strip() == '"""':
        console.print("[dim](Multiline mode: paste your text, then type \"\"\" on a new line to finish)[/dim]")
        lines = []
        while True:
            line = console.input("")
            if line.strip() == '"""':
                break
            lines.append(line)
        return "\n".join(lines)

    return first_line

@app.command()
def chat():
    """Start an interactive chat session with the Coding Agent."""
    console.print(Panel.fit(
        "[bold green]🤖 Autonomous Coding Agent[/bold green]\n"
        f"[cyan]Model:[/cyan] {settings.OPENAI_MODEL}\n"
        "[dim]Type 'exit' or 'quit' to end the session.[/dim]",
        border_style="green"
    ))

    agent = CodingAgent()

    while True:
        try:
            user_input = get_user_input(console)   
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