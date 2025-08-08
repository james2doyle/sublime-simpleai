<general_rules>
When creating new functions related to API client interactions, commands, event listeners, or settings, always first search within the `plugin/` directory to see if an existing file or module is appropriate. If not, create a new file within the `plugin/` directory to house the new functionality.

For code quality, ensure that `pyright` for type checking and `ruff` for linting and formatting are used. These tools are configured via `pyproject.toml`.
</general_rules>
<repository_structure>
The repository is structured as a Sublime Text plugin. The core logic resides in `gemini_ai.py`. The `plugin/` directory contains modular components for API communication (`api_client.py`), Sublime Text commands (`commands.py`), event listeners (`listeners.py`), and plugin settings (`settings.py`). Configuration for dependencies and build tools is managed in `pyproject.toml`. Prompt snippets used by the plugin are located in the `snippets/` directory.
</repository_structure>
<dependencies_and_installation>
Dependencies are managed via `pyproject.toml`. The project requires Python 3.8 or higher. Development dependencies include `pyright`, `pyrefly`, and `ruff`. It is recommended to use a package manager like `pip` or `poetry` to install dependencies.

For plugin installation within Sublime Text, the recommended method is via Package Control by searching for "Sublime Gemini". Manual installation involves cloning the repository into the Sublime Text Packages directory.
</dependencies_and_installation>
<testing_instructions>
No explicit testing framework or instructions were found within the repository.
</testing_instructions>
<pull_request_formatting>
</pull_request_formatting>
