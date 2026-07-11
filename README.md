# 🤖 Autonomous Coding Agent

A production-grade, CLI-based Autonomous Coding Agent that runs directly inside your terminal — installable as a **global command**, so you can enable it in any project, anywhere on your machine. Powered by OpenAI's GPT-4o with native tool-calling, it can read, write, and patch code, manage project directories, and execute shell commands, all through natural language, with built-in safety guardrails at every step.

---

## ✨ Features

- **🧠 ReAct Execution Loop** — A strict Reason → Act → Observe loop for structured, reliable, step-by-step task completion.
- **🔧 Native Tool-Calling** — Direct access to the local filesystem and terminal through a secure, well-defined set of tools.
- **🛡️ Safety Guardrails** — Every file write, patch, and terminal command requires explicit user confirmation (`y/n`) before execution. Dangerous commands (e.g. `rm -rf /`, `mkfs`, `shutdown`) are automatically blocked.
- **📦 Token Optimization** — Large file reads and terminal outputs are automatically truncated to protect the context window.
- **🎨 Rich Terminal UI** — Clean, interactive chat experience with syntax-highlighted Markdown rendering, spinners, and clear separation between the agent's reasoning, tool calls, and observations.
- **📝 Multiline Prompt Support** — Paste large, detailed prompts safely using a `"""` wrapper without breaking terminal input handling.
- **⚛️ Atomic File Writes** — `patch_file` uses atomic write operations (temp file + OS-level replace) to guarantee files are never left in a corrupted state, even on a crash.
- **🌍 Global CLI Command** — Install once, then run `codeagent` from inside *any* project folder on your system.

---

## 🛠️ Tech Stack

| Component        | Technology              |
|-------------------|--------------------------|
| Language           | Python 3.11+             |
| CLI Framework       | Typer                    |
| Terminal UI          | Rich                     |
| Data Validation      | Pydantic v2 / pydantic-settings |
| LLM Provider          | OpenAI (GPT-4o)          |

---

## 📁 Project Structure

```
Coding_Agent/
├── pyproject.toml          # Package config — defines the `codeagent` command
├── venv/                    # Virtual environment (kept outside the package)
└── code_agent/                # The actual installable Python package
    ├── __init__.py
    ├── main.py                  # CLI entrypoint & interactive chat loop
    ├── agent.py                  # Core ReAct orchestration loop
    ├── prompts.py                  # System prompt definition
    ├── requirements.txt
    ├── utils/
    │   ├── __init__.py
    │   └── config.py                  # Settings, logging, and LLM client initialization
    └── tools/
        ├── __init__.py                  # Tool registry (TOOL_FUNCTIONS)
        ├── file_ops.py                     # read_file, write_file, patch_file, create_directory
        ├── shell_ops.py                       # list_dir, execute_command
        ├── safety.py                            # Truncation & dangerous-command detection
        └── schemas.py                              # OpenAI-compatible tool JSON schemas
```

---

## 🧰 Available Tools

| Tool | Description |
|------|--------------|
| `read_file(path, line_start, line_end)` | Reads a file, optionally within a specific line range, to save tokens. |
| `write_file(path, content, append)` | Creates, overwrites, or appends to a file (with confirmation). |
| `patch_file(path, search_block, replace_block)` | Makes a precise, targeted edit to a file using atomic writes (with confirmation). |
| `create_directory(path)` | Creates a new directory, including parent folders. |
| `list_dir(path)` | Lists the contents of a directory, skipping hidden files and `__pycache__`. |
| `execute_command(command)` | Runs a shell command and returns stdout/stderr/exit code (with confirmation and blacklist checks). |

---

## 🚀 One-Time Setup (Install as a Global Command)

You only need to do this **once**. After that, `codeagent` will be available from any folder on your system.

### 1. Clone or download the project
```bash
git clone <your-repo-url>
cd Coding_Agent
```

### 2. Create and activate a virtual environment
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install project dependencies
```powershell
pip install -r code_agent\requirements.txt
```

### 4. Install the agent as a global, editable package
Run this from the project root (where `pyproject.toml` lives):
```powershell
pip install -e .
```

> 💡 If you want `codeagent` available even outside this virtual environment (i.e. truly global, in any terminal), also run the same command using your **global Python's pip**, not the venv's:
> ```powershell
> deactivate
> pip install -e .
> ```

### 5. Set up your global configuration (API key)
Create a folder and `.env` file in your user profile directory:
```powershell
mkdir $env:USERPROFILE\.coding_agent
notepad $env:USERPROFILE\.coding_agent\.env
```
Add the following inside it, then save:
```env
OPENAI_API_KEY=your_actual_openai_api_key_here
OPENAI_MODEL=gpt-4o
```

That's it — setup is complete. ✅

---

## 💬 How to Use It (Every Time After Setup)

No need to reinstall or reconfigure anything again. Just:

### 1. Open a terminal in **any** project folder
```powershell
cd D:\Path\To\Any\Project
```

### 2. Run the agent
```powershell
codeagent
```

### 3. Start chatting in plain English
```
You: list the files in this directory
You: read main.py and explain what it does
You: create a login page with HTML, CSS, and JS
```

The agent will treat your **current folder** as the working directory — so all file reads, writes, and commands happen right there in that project.

### Pasting long or multi-line prompts
Wrap your prompt in triple quotes to paste multi-line text safely:
```
You: """
Create a simple, professional frontend-only website with 5 pages...
...
"""
```

### Ending a session
Type `exit` or `quit` at any time, or press `Ctrl+C`.

---

## 🔐 Safety by Design

- Every destructive or state-changing action (writing files, patching files, running shell commands) **requires explicit user confirmation**.
- A blacklist blocks known dangerous command patterns before they ever reach the confirmation prompt.
- A hard iteration cap prevents the agent from looping indefinitely on a single task.
- All actions are logged for auditability.

---

## 🧯 Troubleshooting

| Problem | Likely Cause | Fix |
|---------|----------------|-----|
| `codeagent` not recognized | Global Python's `Scripts` folder isn't in PATH, or install was only done inside the venv | Re-run `pip install -e .` using the global (non-venv) `pip` |
| `ModuleNotFoundError: No module named 'code_agent...'` | `pyproject.toml`'s entry point doesn't match the actual folder name | Ensure `codeagent = "code_agent.main:app"` matches your package folder name exactly |
| Confirmation prompts get skipped or misfire | Pasting a multi-line prompt without the `"""` wrapper | Always wrap multi-line input in `"""` on its own line, both start and end |
| `Failed to Load Settings` on startup | Global `.env` file missing or misconfigured | Recheck `%USERPROFILE%\.coding_agent\.env` exists and has a valid `OPENAI_API_KEY` |

---

## 🗺️ Roadmap

- [ ] Git-aware context (auto-detect staged/modified files)
- [ ] Support for multiple LLM providers (Groq, Anthropic, local models)
- [ ] Persistent conversation history across sessions
- [ ] Configurable command whitelist per project

---

## 📄 License

This project is open for personal and educational use. Add your preferred license here (MIT, Apache 2.0, etc.).

---

## 🙋 Author

Built as a hands-on deep dive into agentic AI systems — tool-calling architectures, context management, and the safety considerations of giving an LLM real access to a file system and terminal.