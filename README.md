Simple AI
=========

> This project is inspired by [necarlson97/codex-ai-sublime](https://github.com/necarlson97/codex-ai-sublime) but refactored with the help of AI

Simple AI is a powerful Sublime Text plugin that integrates AI directly into your editor (but only when you want it), enhancing your coding workflow with intelligent assistance. From generating code snippets to refactoring and answering programming questions, Simple AI brings the power of AI to your fingertips.

### Features

**Intelligent Code Completion**: Get context-aware suggestions for your code.

**Code Generation**: Generate functions, classes, or entire code blocks based on your natural language prompts.

**Code Refactoring**: Ask Simple AI to refactor selected code for improved readability, performance, or adherence to best practices.

**Contextual Q&A**: Ask questions about your code, programming concepts, or general knowledge, and get instant answers within Sublime Text.

**Error Explanation & Debugging Help**: Understand and resolve errors faster with AI-driven explanations and suggestions.

**Custom Prompts**: Provide custom prompts for instruction and completion commands.

### Commands

#### `completion_simple_ai`

Write an incomplete part of text and have Simple AI try and complete it. Useful for completing functions or code. **Requires some code to be selected**.

#### `instruct_simple_ai`

Select some code and then provide an additional prompt for it. Useful for asking questions about code or wanting to ask for a rewrite of the selected code. If no code is selected, **the entire file content is sent**.

### Installation

1. Navigate to your Sublime Text Packages directory. You can find this by going to Preferences > Browse Packages... in Sublime Text.
1. Run `git clone https://github.com/james2doyle/sublime-simpleai SimpleAI` in that folder


```sh
# change to the directory found with "Preference: Browse Packages", then clone
git clone https://github.com/james2doyle/sublime-simpleai.git SimpleAI
```

### Configuration

Before using Simple AI, you need to configure your AI API key.

Simple AI can use any OpenAI API compatible service. The easiest way to get access to the most models, in my experience, is using [OpenRouter](https://openrouter.ai/).

The default settings assume you want to use OpenRouter.

In Sublime Text, go to Preferences > Package Settings > Simple AI > Settings.

Add your API key to the `simple_ai.sublime-settings` file:

```jsonc
{
    "api_token": "YOUR_API_KEY_HERE"
}
```

Important: Replace `"YOUR_API_KEY_HERE"` with your actual API key.

#### Project Configuration

You can also configure the `api_token` on the project level.

In your `sublime-project` file:

```jsonc
{
    // ... folders array with paths, etc.
    "settings": {
        "SimpleAI": {
            "api_token": "YOUR_API_KEY_HERE",
            // optionally, select specific settings
            "hostname": "openrouter.ai",
            "model_name": "openai/gpt-5.2",
            "api_path": "/api/v1/chat/completions",
        }
        // ... the rest of your settings
    }
}
```

The settings code will check your local `sublime-project` first and then the global User `simple_ai.sublime-settings` file. So the project settings take priority.

#### Reasoning Effort Control

Simple AI supports controlling the reasoning effort for AI responses. The `reasoning_effort` parameter allows you to specify how much effort the AI should put into reasoning about your request.

Available options:
- `"auto"`: Let the AI automatically determine the appropriate reasoning effort
- `"low"`: Use minimal reasoning effort (faster responses)
- `"medium"`: Use moderate reasoning effort (balanced approach)
- `"high"`: Use maximum reasoning effort (more thorough analysis)

You can set this parameter for both completion and instruct commands:

```jsonc
{
    "api_token": "YOUR_API_KEY_HERE",
    "completions": {
        "reasoning_effort": "auto"
    },
    "instruct": {
        "reasoning_effort": "high"
    }
}
```

#### Custom Prompts

You can also provide custom snippets for the prompts that are used during `instruct` and `completion` commands:

```jsonc
{
    // ... folders array with paths, etc.
    "settings": {
        "SimpleAI": {
            "api_token": "YOUR_API_KEY_HERE",
            "completions": {
                "prompt_snippet": "Packages/User/my_completion_prompt.sublime-snippet"
            },
            "instruct": {
                "prompt_snippet": "Packages/User/my_instruct_prompt.sublime-snippet"
            }
        }
        // ... the rest of your settings
    }
}
```

There are some additional vars set for the snippet:

```
$OS              Platform OS (osx, windows, linux)
$SHELL           The shell that is currently set in the ENV
$PROJECT_PATH    The path to the project, if applicable
$FILE_NAME       The full path to the file being edited
$SYNTAX          The syntax of the file, extracted from the views syntax
$SOURCE_CODE     The code that was selected
```

You can view the current snippets that are using in the `snippets` directory.

### Usage

Simple AI provides several commands accessible via the Command Palette or custom key bindings.

#### Command Palette

1. Open Tools > Command Palette... (Ctrl+Shift+P / Cmd+Shift+P).
1. Type Simple AI to see available commands:
  - Simple AI: Complete Code: Generates the rest of the code that has been selected.
  - Simple AI: Instruct Code: Add an additional prompt to the selected code.

#### Key Bindings

You can set up custom key bindings for frequently used commands. Go to Preferences > Key Bindings and add entries like this:

```jsonc
[
    { "keys": ["ctrl+alt+g", "ctrl+alt+c"], "command": "completion_simple_ai" },
    { "keys": ["ctrl+alt+g", "ctrl+alt+g"], "command": "instruct_simple_ai" }
]
```

### Development

#### Project Structure

- `simple_ai.py`: Main plugin entry point and core logic.
- `plugin/api_client.py`: Handles communication with the AI API.
- `plugin/commands.py`: Defines the Sublime Text commands for AI interactions.
- `plugin/listeners.py`: Contains event listeners for various Sublime Text events (e.g., selection changes).
- `plugin/settings.py`: Manages plugin settings and API key storage.
- `pyproject.toml`: Project configuration for dependency management and build tools.
