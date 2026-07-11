# 🤖 Autonomous Coding Agent

A production-grade, CLI-based Autonomous Coding Agent that runs directly inside your terminal. Powered by OpenAI's GPT-4o with native tool-calling, it can read, write, and patch code, manage project directories, and execute shell commands — all through natural language, with built-in safety guardrails at every step.

---

## ✨ Features

- **🧠 ReAct Execution Loop** — A strict Reason → Act → Observe loop for structured, reliable, step-by-step task completion.
- **🔧 Native Tool-Calling** — Direct access to the local filesystem and terminal through a secure, well-defined set of tools.
- **🛡️ Safety Guardrails** — Every file write, patch, and terminal command requires explicit user confirmation (`y/n`) before execution. Dangerous commands (e.g. `rm -rf /`, `mkfs`, `shutdown`) are automatically blocked.
- **📦 Token Optimization** — Large file reads and terminal outputs are automatically truncated to protect the context window.
- **🎨 Rich Terminal UI** — Clean, interactive chat experience with syntax-highlighted Markdown rendering, spinners, and clear separation between the agent's reasoning, tool calls, and observations.
- **📝 Multiline Prompt Support** — Paste large, detailed prompts safely using a `"""` wrapper without breaking terminal input handling.
- **⚛️ Atomic File Writes** — `patch_file` uses atomic write operations (temp file + OS-level replace) to guarantee files are never left in a corrupted state, even on a crash.

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
├── main.py              # CLI entrypoint & interactive chat loop
├── agent.py              # Core ReAct orchestration loop
├── prompts.py             # System prompt definition
├── requirements.txt        # Python dependencies
├── .env                     # Environment variables (not committed)
├── utils/
│   └── config.py              # Settings, logging, and LLM client initialization
└── tools/
    ├── __init__.py              # Tool registry (TOOL_FUNCTIONS)
    ├── file_ops.py                # read_file, write_file, patch_file, create_directory
    ├── shell_ops.py                 # list_dir, execute_command
    ├── safety.py                      # Truncation & dangerous-command detection
    └── schemas.py                       # OpenAI-compatible tool JSON schemas
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

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd Coding_Agent
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
MAX_TOKENS_RESPONSE=4096
MAX_TOOL_OUTPUT_CHARS=4000
```

### 5. Run the agent
```bash
python main.py
```

---

## 💬 Usage

Once running, simply chat with the agent in plain English:

```
You: list the files in this directory
You: read main.py and explain what it does
You: create a login page with HTML, CSS, and JS
```

### Pasting long or multi-line prompts

Wrap your prompt in triple quotes to paste multi-line text safely:

```
You: """
Create a simple, professional frontend-only website with 5 pages...
...
"""
```

Type `exit` or `quit` at any time to end the session.

---

## 🔐 Safety by Design

- Every destructive or state-changing action (writing files, patching files, running shell commands) **requires explicit user confirmation**.
- A blacklist blocks known dangerous command patterns before they ever reach the confirmation prompt.
- A hard iteration cap prevents the agent from looping indefinitely on a single task.
- All actions are logged for auditability.

---

## 🗺️ Roadmap

- [ ] Git-aware context (auto-detect staged/modified files)
- [ ] Support for multiple LLM providers (Groq, Anthropic, local models)
- [ ] Persistent conversation history across sessions
- [ ] Configurable command whitelist per project

---

## 📄 License

This project is open for personal and educational use.

---

## 🙋 Author

Built as a hands-on deep dive into agentic AI systems — tool-calling architectures, context management, and the safety considerations of giving an LLM real access to a file system and terminal.