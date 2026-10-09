import sys
import os
import time
import subprocess
import httpx
import ollama

# Unicode Escape constants for system symbols
SYMBOL_WARN = "\u26a0\ufe0f"   # Warning Sign
SYMBOL_ERROR = "\u274c"        # Cross Mark / X
SYMBOL_SUCCESS = "\u2705"      # White Heavy Check Mark

def ensure_ollama_running() -> bool:
    """Checks if Ollama is awake; if not, attempts to fire it up in the background."""
    try:
        ollama.ps()
        return True
    except (httpx.ConnectError, ConnectionRefusedError):
        print(f"[{SYMBOL_WARN}] Ollama is not running. Attempting to start the background service...")

        try:
            if sys.platform == "win32":
                subprocess.Popen(
                    ["ollama", "serve"],
                    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            elif sys.platform == "darwin":
                subprocess.Popen(
                    ["open", "-a", "Ollama"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                subprocess.Popen(
                    ["ollama", "serve"],
                    preexec_fn=os.setpgrp,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            print("Waiting for Ollama to initialize...")
            for _ in range(6):
                time.sleep(1)
                try:
                    ollama.ps()
                    print(f"[{SYMBOL_SUCCESS}] Ollama successfully started!")
                    return True
                except Exception:
                    continue

        except FileNotFoundError:
            print("\n" + "="*50)
            print(f"[{SYMBOL_ERROR}] ERROR: The 'ollama' executable was not found in your system PATH.")
            print("="*50)
            print("Please download it from https://ollama.com")
            print("="*50 + "\n")
            sys.exit(1)

    except Exception as e:
        print(f"[{SYMBOL_ERROR}] Unexpected initialization error: {e}")
        sys.exit(1)

    print(f"[{SYMBOL_ERROR}] Failed to connect to Ollama. Please launch it manually.")
    sys.exit(1)
