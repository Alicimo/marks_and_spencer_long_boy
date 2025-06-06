# Python Coding Conventions & Best Practices

- Follow PEP 8 — the official Python style guide.
- Indent using 4 spaces, not tabs.
- Limit lines to 79 characters.
- Use blank lines to separate functions, classes, and logical sections.
- Use meaningful variable and function names:
  - `snake_case` for variables and functions
  - `PascalCase` for classes

## Imports

- Group imports in this order:
  1. Standard library
  2. Third-party packages
  3. Local application imports
- Add a blank line between each group.
- Use absolute imports over relative ones.
- Avoid wildcard imports (`from module import *`).

## Naming Conventions

- `snake_case`: functions, variables, and methods
- `PascalCase`: classes and exceptions
- `UPPER_CASE`: constants
- `_single_leading_underscore`: internal use (non-public)

## Functions and Methods

- Keep functions small and focused on a single task.
- Use type hints for arguments and return types.
- Include docstrings for all public methods and classes.
- Avoid mutable default arguments (like lists or dicts).
- Avoid duplicate code. Instead abstract code into new methods.

## Documentation
- Document public modules, classes, and functions with clear docstrings.
- Use Google docstring formats.
- Keep comments short, relevant, and up to date.

## Code Quality
- Write unit tests for your functions.
- Use ruff for linting and formating.

## Virtual Environment
- Use `uv` for virtual environments and package management.
- Install dependencies using `uv add <package>`.
