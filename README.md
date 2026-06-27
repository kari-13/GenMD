# modelstream 🌊

Tired of heavy local web UIs like Open WebUI eating your RAM? Meet **modelstream**—a lightweight terminal wrapper for Ollama. Get beautiful live markdown streams, code highlighting, and instant copying right in your shell with zero browser bloat.

---

## ✨ Features

* **Zero Web Bloat**: Runs natively in your terminal, saving gigabytes of memory.
* **Rich Markdown**: Renders live streams, clean panels, and tables via `rich`.
* **Code Highlight**: Full syntax coloring for code blocks inside responses.
* **Instant Clipboard**: Automatic code-block extraction with `pyperclip`.

## 📦 Installation

Ensure you have [Ollama](https://ollama.com) running locally, then install the Python dependencies:

```bash
pip install ollama rich pyperclip
```

Clone this repository and run the script:

```bash
git clone https://github.com
cd modelstream
python main.py
```


