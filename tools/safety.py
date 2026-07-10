from utils.config import settings
# ---- Safety: Blacklisted command patterns ----

"""These are dangerous pattern which we cannot allow our agent to execute that's why 
we filter them with the function and does not allow our agent to execute these patterns
"""

DANGEROUS_PATTERNS = [
    "rm -rf /", "rm -rf ~", "mkfs", "format ", ":(){ :|:& };:",
    "shutdown", "reboot", "> /dev/sda", "dd if=", "del /f /s /q",
    "rd /s /q", "diskpart",
]

def truncate(text:str)->str:
    """Truncate large outputs to protect context window. Here we are limiting our Agent your max contxt win is 4000"""
    limit = settings.MAX_TOOL_OUTPUT_CHARS
    if len(text) > limit:
        return text[:limit] + f"\n\n... [TRUNCATED, {len(text) - limit} more chars]"
    return text


def is_dangerous(command:str)->bool:
    """This Fucntion will take the user command and convert it into lower case and then 
    check the command in dangerous pattern or not and returns true or false according to it"""
    cmd_lower = command.lower().strip()
    return any(pattern in cmd_lower for pattern in DANGEROUS_PATTERNS)
