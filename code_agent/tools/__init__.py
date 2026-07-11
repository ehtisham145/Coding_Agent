from .file_ops import read_file, write_file, patch_file,create_directory
from .shell_ops import execute_command, list_dir
from .schemas import TOOLS_SCHEMA

TOOL_FUNCTIONS = {
    "read_file": read_file,
    "write_file": write_file,
    "patch_file": patch_file,
    "create_directory": create_directory,
    "list_dir": list_dir,
    "execute_command": execute_command,
}