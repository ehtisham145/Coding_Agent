from pathlib import Path
from code_agent.tools.safety import truncate,is_dangerous
from rich.console import Console
from rich.prompt import Confirm
from code_agent.utils.config import logger
import subprocess

console = Console()

# ---- Tool 4: list_dir ----
def list_dir(path:str = ".")->str:
    """
    Lists the contents of a directory safely with emojis, file sizes, and memory protection.
    Production-ready: Prevents crashes on massive directories (like node_modules or .git).
    """
    try:
        dir_path = Path(path)
        if not dir_path.exists():
            return "Error : Directory not Found at this Path"
        
        if not dir_path.is_dir():
            return "Error : The Specified Path is not a Directory "
        
        items = []
        for item in sorted(dir_path.iterdir()):
            if item.name.startswith(".") or item.name == "__pycache__":
                continue
            marker = "📁" if item.is_dir() else "📄"
            items.append(f"{marker} {item.name}")

        return truncate("\n".join(items) if items else "(empty directory)")
    except Exception as e:
        logger.error(f"list_dir error: {e}")
        return f"ERROR: {e}"



#----------Tool 5------------------------------------
def execute_command(command: str) -> str:
    if is_dangerous(command):
        logger.warning(f"Blocked dangerous command: {command}")
        return f"BLOCKED: Command '{command}' matches a dangerous pattern and was refused."

    console.print(f"\n[bold yellow]⚠ Agent wants to RUN command:[/bold yellow] {command}")
    if not Confirm.ask("Allow execution?", default=False):
        return "ACTION DENIED by user."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\nEXIT CODE: {result.returncode}"
        logger.info(f"Command executed: {command} (exit={result.returncode})")
        return truncate(output)
    except subprocess.TimeoutExpired:
        return "ERROR: Command timed out after 60 seconds."
    except Exception as e:
        logger.error(f"execute_command error: {e}")
        return f"ERROR: {e}"


