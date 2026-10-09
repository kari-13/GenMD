

Contributing Guide
==================

Thank you for contributing to this terminal Markdown renderer built around [Ollama](https://ollama.com).

This project focuses on fast, readable, and predictable Markdown rendering in terminal environments, especially for AI-generated and streamed output.

* * *

🎯 Project Goals
----------------

*   Render Markdown cleanly in terminal environments
*   Handle streaming AI output gracefully (especially from Ollama)
*   Stay lightweight and dependency-minimal
*   Prioritize readability over perfect spec compliance
*   Maintain predictable CLI behavior

**Non-goals:**

*   GUI applications
*   Heavy web frameworks
*   Cloud-only AI integrations
*   Complex editor-like features

* * *

🧱 How to Contribute
--------------------

### 1\. Fork and Clone

    git clone https://github.com/your-username/your-repo.git
    cd your-repo

### 2\. Create a Branch

    git checkout -b feature/your-change-name

Examples:

*   feature/improve-list-rendering
*   fix/streaming-bug
*   docs/update-readme

### 3\. Make Focused Changes

*   Small and isolated changes
*   One feature or fix per PR
*   No unrelated refactoring

### 4\. Test Your Changes

*   Raw Markdown input
*   Streamed output from Ollama
*   Edge cases (lists, code blocks, broken Markdown)

### 5\. Commit Style

    feat: improve code block rendering
    fix: handle nested lists correctly
    docs: update contributing guide

Avoid:

    update stuff
    fix bug

### 6\. Open a Pull Request

*   What changed
*   Why it changed
*   How it was tested
*   Screenshots if output changed

* * *

🐛 Reporting Issues
-------------------

*   Operating system and terminal
*   Steps to reproduce
*   Example input
*   Expected vs actual output
*   Whether Ollama was used

* * *

💡 Feature Requests
-------------------

*   Better Markdown rendering
*   Streaming improvements
*   Performance optimizations
*   Theme support
*   CLI usability improvements

* * *

🧠 Code Philosophy
------------------

*   Terminal output must be predictable
*   Simplicity over complexity
*   Minimal dependencies
*   Optimized for streaming AI output
*   Readable code preferred over clever code

* * *

🚫 What Not to Do
-----------------

*   Large unrelated refactors
*   Breaking CLI behavior without discussion
*   Heavy frameworks or dependencies
*   Multiple features in one PR

* * *

🤝 Community Expectations
-------------------------

*   Be respectful
*   Be constructive
*   Keep discussions focused
*   Prefer small incremental improvements

* * *

📜 License
----------

By contributing, you agree your code will be licensed under the same license as this project.
