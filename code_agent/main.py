# main.py
import typer
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

from code_agent.utils.config import settings, logger
from code_agent.agent import CodingAgent

app = typer.Typer(add_completion=False)
console = Console()



def get_user_input(console: Console) -> str:
    """Supports single-line, inline triple-quotes, and multiline block modes safely."""
    first_line = console.input("\n[bold blue] You ›[/bold blue] ").strip()

    # Edge Case: User pasted a single line wrapped in triple quotes e.g., """my query"""
    if first_line.startswith('"""') and first_line.endswith('"""') and len(first_line) > 6:
        return first_line[3:-3].strip()

    # Block Multiline mode
    if first_line == '"""':
        console.print("[dim]⚡ Multiline Mode Active: Paste text, then type \"\"\" on a new line and press Enter to send.[/dim]")
        lines = []
        while True:
            try:
                line = console.input("")
                if line.strip() == '"""':
                    break
                lines.append(line)
            except (KeyboardInterrupt, EOFError):
                console.print("\n[yellow] Multiline input cancelled.[/yellow]")
                return ""
        return "\n".join(lines).strip()

    return first_line


@app.command()
def chat():
    """Start an interactive chat session with the Coding Agent."""
    console.clear()
    welcome_text = Text.assemble(
        (" Autonomous Coding Agent \n", "bold green"),
        (f"  Engine: {settings.OPENAI_MODEL}\n\n", "cyan"),
        (" System Commands:\n", "bold dim"),
        ("   /clear   - Flush conversation memory\n", "dim"),
        ("   /exit    - Terminate session safely\n", "dim")
    )
    console.print(Panel.fit(
        welcome_text,
        title="[bold space_cadet]System Booted[/bold space_cadet]",
        border_style="green",
        padding=(1, 4)
    ))
    
    agent = CodingAgent()

    while True:
        try:
            user_input = get_user_input(console) 
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold yellow] Session terminated via shortcut. Goodbye![/bold yellow]")
            break
        
        # Input sanitization
        clean_input = user_input.strip()
        if not clean_input:
            continue

        # Intercept System Modifiers
        if clean_input.lower() in ("exit", "quit", "/exit"):
            console.print("[bold yellow] Goodbye![/bold yellow]")
            break

        if clean_input.lower() == "/clear":
            agent = CodingAgent() # Hard reset the memory and context
            logger.info("Agent context flushed by user command.")
            console.print("[bold green]🧹 Memory cleared! Starting a fresh session.[/bold green]")
            continue
        
        try:
            _= agent.run(user_input)
        
        except Exception as e:
            logger.critical(f"Fatal error during agent turn processing: {e}", exc_info=True)
            console.print(Panel(
                f"[bold red] System Error:[/bold red] Internal execution failed.\n[dim]{e}[/dim]",
                title="Runtime Exception",
                border_style="red"
            ))
            console.print("[yellow] Recommendation: Type `/clear` if the agent is acting unstable.[/yellow]")

if __name__ == "__main__":
    app()