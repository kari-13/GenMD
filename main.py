import re
import sys
import time

import pyperclip
from ollama import chat
from rich.console import Console, Group
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

animation = [".", "..", "..."]


def extract_and_copy_code(text: str):
    """Extracts the first Python code block and copies it to the clipboard."""
    code_blocks = re.findall(r"```python\n(.*?)\n```", text, re.DOTALL)
    if code_blocks:
        pyperclip.copy(code_blocks[0].strip())
        console.print(
            "\n[bold green]✔ First Python code snippet automatically copied to clipboard![/bold green]"
        )
    else:
        generic_blocks = re.findall(r"```\n?(.*?)\n```", text, re.DOTALL)
        if generic_blocks:
            pyperclip.copy(generic_blocks[0].strip())
            console.print(
                "\n[bold green]✔ Code snippet automatically copied to clipboard![/bold green]"
            )


def ask_ai(prompt: str):
    stream = chat(
        model="qwen3.5:9b",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    full_response = ""
    index = 0  # Track frame index across iterations

    print("\n" + "═" * 60)

    with Live(
        Panel("Clustering billions of vectors for you...", title="Ollama"),
        refresh_per_second=15,
        console=console,
    ) as live:
        for chunk in stream:
            content = chunk.message.content or ""

            # 1. Animate while stream is completely empty
            if not content and not full_response:
                current_dots = animation[index % len(animation)]
                animated_text = (
                    f"Clustering billions of vectors for you{current_dots:<3}"
                )
                live.update(Panel(animated_text, title="Ollama"))
                index += 1
                time.sleep(0.5)
                continue

            # 2. Append incoming tokens sequentially for instant streaming
            full_response += content

            # Separate thinking process and actual response
            thinking_text = ""
            response_text = full_response

            if "thinking process:" in full_response.lower():
                parts = re.split(
                    r"thinking process:", full_response, flags=re.IGNORECASE
                )
                thinking_text = parts[0].strip()
                if len(parts) > 1:
                    content_match = re.search(r"(\n# .*|\n```.*)", parts[1], re.DOTALL)
                    response_text = (
                        content_match.group(1).strip()
                        if content_match
                        else parts[1].strip()
                    )
            elif "<thinking>" in full_response.lower():
                parts = re.split(r"</thinking>", full_response, flags=re.IGNORECASE)
                thinking_text = parts[0].replace("<thinking>", "").strip()
                if len(parts) > 1:
                    response_text = parts[1].strip()

            # Build our layout pieces
            ui_components = []

            if thinking_text:
                ui_components.append(
                    Panel(
                        thinking_text,
                        title="[yellow]Thinking Process[/yellow]",
                        border_style="yellow",
                    )
                )

            if response_text:
                ui_components.append(
                    Panel(
                        Markdown(response_text),
                        title="[magenta]AI Response[/magenta]",
                        border_style="magenta",
                    )
                )

            # 3. Stream layout updates straight to the screen
            if ui_components:
                live.update(Group(*ui_components))
            else:
                live.update(Panel(full_response, title="Streaming..."))

    # Extract code from the final processed response block
    extract_and_copy_code(
        response_text if "response_text" in locals() else full_response
    )


if __name__ == "__main__":
    console.print(
        "[bold green]Ollama Chat Initialized. Type 'quit' or 'bye' to exit.[/bold green]\n"
    )

    try:
        while True:
            user_prompt = input("\033[1;34mYou:\033[0m ")

            if user_prompt.strip().lower() in ["quit", "bye"]:
                console.print("\n[bold yellow]Goodbye![/bold yellow]")
                break

            if not user_prompt.strip():
                continue

            ask_ai(user_prompt)
            print("\n" + "─" * 60 + "\n")

    except KeyboardInterrupt, EOFError:
        console.print("\n\n[bold red]Session ended.[/bold red]")
        sys.exit(0)
