import re
import sys

import pyperclip
from ollama import chat
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


def extract_and_copy_code(text: str):
    """Extracts the first Python code block and copies it to the clipboard."""
    # Find markdown code blocks tagged with python
    code_blocks = re.findall(r"```python\n(.*?)\n```", text, re.DOTALL)
    if code_blocks:
        pyperclip.copy(code_blocks[0].strip())
        console.print(
            "\n[bold green]✔ First Python code snippet automatically copied to clipboard![/bold green]"
        )
    else:
        # Fallback to any generic code block if no python tag is found
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
    is_thinking = False
    has_shown_thinking_header = False

    # Track line content for dynamic terminal updates
    for chunk in stream:
        content = chunk.message.content or ""
        if not content:
            continue

        full_response += content

        # Catch when the model is in its "Thinking" phase
        if "thinking" in full_response.lower() and not has_shown_thinking_header:
            if "thinking process:" in full_response.lower():
                console.print("\n[bold yellow]── Thinking Process ──[/bold yellow]")
                has_shown_thinking_header = True
                is_thinking = True
                continue

        # Print the stream text raw so you can watch it type out
        sys.stdout.write(content)
        sys.stdout.flush()

    # --- Stream Finished: Time to format cleanly ---

    # Split final answer from the thinking block
    clean_response = full_response
    if "thinking process:" in full_response.lower():
        parts = re.split(r"thinking process:", full_response, flags=re.IGNORECASE)
        if len(parts) > 1:
            # Look for the actual Markdown content start (usually code blocks or headings)
            # We strip out the thinking bullet points from the final rendered output
            content_match = re.search(r"(\n# .*|\n```.*)", parts[1], re.DOTALL)
            if content_match:
                clean_response = content_match.group(1).strip()
            else:
                clean_response = parts[1]

    # Clear terminal lines or print a clean break before showing beautiful markdown
    print("\n" + "═" * 60)
    console.print("[bold magenta]✨ Formatted AI Response:[/bold magenta]\n")

    # Render syntax-highlighted Markdown code snippets perfectly
    console.print(Markdown(clean_response))

    # Automatically extract code and copy it to clipboard
    extract_and_copy_code(clean_response)


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
