from pathlib import Path
from code_agent.utils.config import settings,logger
from rich.console import Console
from rich.prompt import Confirm
import tempfile
from code_agent.tools.safety import truncate

console = Console()


"""
For prinitng some content in terminal we use rich library Console Module
and for getting input from user we use Confirm Module of rich library
We will use the subprocess module for automation
"""


#-----------------------------Tool 1----------------------------------
def read_file(path:str , line_start:int=None, line_end:int=None)->str:
    """Here in this function we will read the content of file and if file content is larger
    than context window we will raise an error"""
    try:
        file_path = Path(path)
        if not file_path.is_file():
            return f"ERROR: '{path}' is not a valid file or does not exist."

        lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()

        if line_start is not None and line_end is not None:
            selected = lines[max(0, line_start - 1):line_end]
        else:
            selected = lines

        content = "\n".join(selected)
        return truncate(content)
    
    except Exception as e:
        logger.error(f"read_file error: {e}")
        return f"Error : {e}"




# ---- Tool 2: write_file ------------
def write_file(path: str, content: str,append: bool = False) -> str:
    """This Function will write the content in the file by taking permission from the user"""
    try:
        file_path = Path(path)
        
        if file_path.is_dir():
            return f"ERROR: '{path}' is a directory, cannot write a file here."

        # UI Warning message mode 
        mode_str = "APPEND to" if append else "WRITE (Overwrite)"
        console.print(f"\n[bold yellow]⚠ Agent wants to {mode_str} file:[/bold yellow] {path}")
        
        if not Confirm.ask("Allow this action?", default=False):
            return "ACTION DENIED by user."

        file_path.parent.mkdir(parents=True, exist_ok=True)
        if append:
            with file_path.open("a", encoding="utf-8") as f:
                f.write(content)
            action = "appended"
        else:
            file_path.write_text(content, encoding="utf-8")
            action = "written"

        logger.info(f"File {action}: {path}")
        return f"SUCCESS: File '{path}' {action} ({len(content)} chars)."
        
    except Exception as e:
        logger.error(f"write_file error: {e}")
        return f"ERROR: {e}"
   

# ---- Tool 3: Patch File ------------

def patch_file(path: str, search_block: str, replace_block: str) -> str:
    """
    Updates a specific block of text in a file safely with user confirmation.
    Production-ready with atomic writes, strict error messages, and duplicate detection.
    """
    try:
        file_path = Path(path)
        
        # 1. Strict Existence and Type Checks
        if not file_path.exists():
            return f"ERROR: File '{path}' does not exist."
        if file_path.is_dir():
            return f"ERROR: '{path}' is a directory, cannot patch it."
        
        # 2. Empty Search Block Guard
        if not search_block:
            return "ERROR: search_block cannot be empty."
    
        # Read file safely
        read_file_content = file_path.read_text(encoding="utf-8", errors="replace")
        
        # 4. Duplicate Check (Ambiguity Guard)
        occurrences = read_file_content.count(search_block)
        if occurrences == 0:
            return "ERROR: search_block not found in file. No changes made."
        elif occurrences > 1:
            return f"ERROR: Found {occurrences} occurrences of search_block. Patching is ambiguous. Please provide a more unique search_block."

        # 5. UI Preview & User Confirmation
        console.print(f"\n[bold yellow]⚠ Agent wants to PATCH file:[/bold yellow] {path}")
        console.print(f"[red]- {search_block[:200]}[/red]")
        console.print(f"[green]+ {replace_block[:200]}[/green]")
        if not Confirm.ask("Allow this patch?", default=False):
            return "ACTION DENIED by user."

        # 6. Apply Patch
        updated = read_file_content.replace(search_block, replace_block, 1)
        
        # 7. Atomic Write (Safest way to write in production)
        temp_dir = file_path.parent
        with tempfile.NamedTemporaryFile("w", dir=temp_dir, delete=False, encoding="utf-8") as tf:
            tf.write(updated)
            temp_file_path = Path(tf.name)

            """We implemented Atomic Writing. The code first creates a temporary file in the same directory and 
            writes all the modified data into it. Once the write operation completes successfully, it swaps
            the temporary file with the original file using an OS-level replace() function. This ensures that
            even if a system crash or power failure
            occurs mid-write, your original file remains 100% safe and uncorrupted."""
        
        # Safely replace the original file with the temp file
        temp_file_path.replace(file_path)
        
        logger.info(f"File patched successfully: {path}")
        return f"SUCCESS: File '{path}' patched."
        
    except Exception as e:
        logger.error(f"patch_file error: {e}")
        # Cleanup temp file if it was created but not swapped
        if 'temp_file_path' in locals() and temp_file_path.exists():
            try:
                temp_file_path.unlink()
            except Exception:
                pass
        return f"ERROR: {e}"
    


def create_directory(path: str) -> str:
    """Creates a directory (and parent directories if needed)."""
    try:
        dir_path = Path(path)
        if dir_path.exists() and dir_path.is_file():
            return f"ERROR: '{path}' already exists as a file, not a directory."
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory created: {path}")
        return f"SUCCESS: Directory '{path}' created."
    except Exception as e:
        logger.error(f"create_directory error: {e}")
        return f"ERROR: {e}"