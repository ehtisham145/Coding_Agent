# agent.py
import json
from rich.console import Console
from rich.markdown import Markdown
from rich.spinner import Spinner
from rich.live import Live

from utils.config import settings, logger,llm_client
from prompts import SYSTEM_PROMPT
from tools import TOOL_FUNCTIONS, TOOLS_SCHEMA

console = Console()


class CodingAgent:
    def __init__(self):
        # Conversation memory: system prompt is always first
        self.history = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def _call_groq(self):
        """Send current history + tools to Open AI and get a response."""
        try:
            response = llm_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=self.history,
                tools=TOOLS_SCHEMA,
                tool_choice="auto",
                max_tokens=settings.MAX_TOKENS_RESPONSE,
            )
            return response.choices[0].message
        except Exception as e:
            logger.error(f"Groq API call failed: {e}")
            console.print(f"[bold red]❌ API Error:[/bold red] {e}")
            return None

    def _execute_tool_call(self, tool_call):
        """Run the actual Python function that corresponds to a tool call."""
        function_name = tool_call.function.name
        try:
            arguments = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError as e:
            return f"ERROR: Invalid arguments JSON from model: {e}"

        console.print(f"\n[bold cyan]🔧 Tool Call:[/bold cyan] {function_name}({arguments})")

        func = TOOL_FUNCTIONS.get(function_name)
        if not func:
            return f"ERROR: Unknown tool '{function_name}'."

        try:
            result = func(**arguments)
            return result
        except Exception as e:
            logger.error(f"Tool execution error ({function_name}): {e}")
            return f"ERROR: Tool execution failed: {e}"

    def run(self, user_input: str):
        """Main ReAct loop for a single user turn."""
        self.history.append({"role": "user", "content": user_input})

        # Safety cap: prevent infinite tool-calling loops
        MAX_ITERATIONS = 30

        for iteration in range(MAX_ITERATIONS):
            with console.status("[bold green]Agent is thinking...[/bold green]", spinner="dots"):
                message = self._call_groq()

            if message is None:
                return "Agent failed to get a response. Check logs."

            # Case 1: Model wants to call tool(s)
            if message.tool_calls:
                # Add assistant's tool-call request to history
                self.history.append({
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in message.tool_calls
                    ],
                })

                # Execute each tool call and add observation
                for tool_call in message.tool_calls:
                    result = self._execute_tool_call(tool_call)
                    console.print(f"[bold magenta]📋 Observation:[/bold magenta] {str(result)[:300]}")

                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    })

                # Loop continues — send updated history back to Groq
                continue

            # Case 2: Model gives final answer (no more tools needed)
            final_answer = message.content or "(No response)"
            self.history.append({"role": "assistant", "content": final_answer})
            return final_answer

        return "⚠️ Max iterations reached. Task may be incomplete."