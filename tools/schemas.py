# tools/schemas.py

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file. Optionally read only a specific line range to save tokens. Use this before editing any file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative or absolute path to the file to read."
                    },
                    "line_start": {
                        "type": "integer",
                        "description": "Optional starting line number (1-indexed). Omit to read from the beginning."
                    },
                    "line_end": {
                        "type": "integer",
                        "description": "Optional ending line number (inclusive). Omit to read till the end."
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create a new file, completely overwrite an existing file, or append content to it. Use append=true to add content without deleting existing data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to write."
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write into the file."
                    },
                    "append": {
                        "type": "boolean",
                        "description": "If true, appends content to the end of the file instead of overwriting it. Defaults to false."
                    },
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "patch_file",
            "description": "Make a precise, targeted edit to an existing file by replacing one unique block of text (search_block) with new text (replace_block). Fails if search_block is not found or appears more than once, so ensure the search_block is unique enough to identify the exact location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to patch."
                    },
                    "search_block": {
                        "type": "string",
                        "description": "The exact, unique block of existing text to find in the file."
                    },
                    "replace_block": {
                        "type": "string",
                        "description": "The new text that will replace the search_block."
                    },
                },
                "required": ["path", "search_block", "replace_block"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "List files and folders inside a directory to understand project structure. Automatically skips hidden files and __pycache__.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path to list. Defaults to the current directory if not provided."
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_command",
            "description": "Run a shell/terminal command (e.g., pip install, pytest, git status, npm run dev) and return its stdout, stderr, and exit code. Dangerous commands are automatically blocked, and the user must confirm before execution.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The exact shell command to execute."
                    },
                },
                "required": ["command"],
            },
        },
    },
]