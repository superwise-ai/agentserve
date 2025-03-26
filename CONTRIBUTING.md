# Contributing to AgentServe

Thank you for your interest in contributing to AgentServe! This document provides guidelines and steps for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/superwise-ai/agentserve.git
   cd agentserve
   ```
3. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
4. Install dependencies:
   ```bash
   poetry install
   ```

## Development Guidelines

### Code Style

- We use `black` for code formatting
- We use `isort` for import sorting
- We use `flake8` for linting
- We use `mypy` for type checking

Before committing, run:
```bash
poetry run black .
poetry run isort .
poetry run flake8
poetry run mypy .
```

### Testing

- Write tests for new features
- Ensure all tests pass before submitting a PR
- Run tests with:
  ```bash
  poetry run pytest
  ```

### Pull Request Process

1. Create a new branch for your feature/fix
2. Make your changes
3. Update documentation if needed
4. Run tests and ensure they pass
5. Submit a pull request

### Commit Messages

- Use clear and descriptive commit messages
- Reference issues and pull requests in commit messages
- Keep commits focused and atomic

## Questions?

Feel free to open an issue if you have any questions about contributing! 