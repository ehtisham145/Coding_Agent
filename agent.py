import json
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from rich.syntax import Syntax
from rich.markdown import Markdown

from utils.config import settings, logger, llm_client
from prompts import SYSTEM_PROMPT
from tools import TOOLS_SCHEMA, TOOL_FUNCTIONS

console = Console()

class CodingAgent:
    def __init__(self):
        self.history: List[Dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def _call_gpt(self) -> Optional[Any]:
        try:
            response = llm_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=self.history,
                tools=TOOLS_SCHEMA if TOOLS_SCHEMA else None,
                tool_choice="auto" if TOOLS_SCHEMA else None,
                max_tokens=settings.MAX_TOKENS_RESPONSE,
                temperature=0.2
            )
            return response.choices[0].message
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}", exc_info=True)
            console.print(Panel(f"[bold red]❌ API Error:[/bold red] {e}", title="Error", border_style="red"))
            return None

    def _execute_tool_call(self, tool_call: Any) -> str:
        function_name = tool_call.function.name
        
        try:
            arguments = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError as e:
            return f"Error: Invalid Argument JSON format: {e}"
        
        # ─── BEAUTIFUL TOOL CALL TREE ───
        tool_tree = Tree(f"[bold bright_cyan]🔧 Tool Invoked: [underline]{function_name}[/underline]")
        args_json = json.dumps(arguments, indent=2)
        tool_tree.add(Panel(Syntax(args_json, "json", theme="monokai", background_color="default"), title="Arguments", border_style="cyan"))
        console.print(tool_tree)

        func = TOOL_FUNCTIONS.get(function_name)
        if not func:
            return f"Error: Unknown Tool '{function_name}'"

        try:
            result = str(func(**arguments))
            
            # ─── BEAUTIFUL OBSERVATION PANEL ───
            # JSON format validation for pretty printing observations if applicable
            try:
                parsed_res = json.loads(result)
                formatted_res = json.dumps(parsed_res, indent=2)
                display_node = Syntax(formatted_res, "json", theme="monokai", background_color="default")
            except Exception:
                display_node = Text(result[:500] + "..." if len(result) > 500 else result, style="green")

            console.print(Panel(display_node, title="📋 Observation Output", border_style="magenta", expand=False))
            return result
            
        except Exception as e:
            logger.error(f"Tool execution failure ({function_name}): {e}", exc_info=True)
            return f"ERROR: Tool internal execution failed: {e}"
        
    def run(self, user_input: str) -> str:
        # User input beauty panel
        console.print(Panel(Text(user_input, style="bright_yellow"), title=" User Input", border_style="yellow"))
        
        self.history.append({"role": "user", "content": user_input})
        MAX_ITERATIONS = 12 

        for iteration in range(MAX_ITERATIONS):
            with console.status(f"[bold green]🤖 Agent Thinking (Step {iteration + 1})...[/bold green]", spinner="bouncingBar"):
                message = self._call_gpt()

            if message is None:
                return "⚠️ Agent failed to get a response."

            # Case 1: Tool Execution
            if getattr(message, "tool_calls", None):
                self.history.append(message)
                for tool_call in message.tool_calls:
                    result = self._execute_tool_call(tool_call)
                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": result,
                    })
                continue

            # Case 2: Final Answer
            final_answer = message.content or "(No content returned)"
            self.history.append({"role": "assistant", "content": final_answer})
            
            # ─── BEAUTIFUL FINAL ANSWER PANEL ───
            console.print("\n")
            console.print(Panel(
                Markdown(final_answer), 
                title="✨ Final Agent Response", 
                border_style="bright_green",
                padding=(1, 2),
                expand=False
            ))
            return final_answer

        return "⚠️ Max reasoning steps reached."