import typer 
from rich.console import Console
from utils.config import settings,logger,groq_client
from prompts import SYSTEM_PROMPT

app = typer.Typer()
console = Console()

@app.command()
def start_agent():
    """Start the Autonomous Coding Agent."""
    console.print("[bold green]✅ Agent is ready![/bold green]")
    console.print(f"[cyan]Using model:[/cyan] {settings.GROQ_MODEL}")



@app.command()
def test_groq():
    """Test basic connection to Groq API (no tool-calling yet)."""
    try:
        response = groq_client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "Say 'Connection successful' and nothing else."},
            ],
            max_tokens=50,
        )
        reply = response.choices[0].message.content
        console.print(f"[bold green]Groq Response:[/bold green] {reply}")
    except Exception as e:
        logger.error(f"Groq API test failed: {e}")
        console.print(f"[bold red]❌ Error:[/bold red] {e}")


if __name__ == "__main__":
    app()