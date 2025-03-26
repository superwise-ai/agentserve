# AgentServe

A simple and efficient tool to deploy OpenAI Agents as FastAPI web services.

## Overview

AgentServe is a lightweight wrapper that allows you to easily serve OpenAI Agents as web services. It provides a simple API for interacting with agents, supporting both synchronous and streaming responses.

## Installation

```bash
pip install agentserve
```

Or with Poetry:

```bash
poetry add agentserve
```

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- OpenAI Agents SDK

## Quick Start

```python
from agents import Agent
from agentserve import serve

# Initialize your agent
math_instructor = Agent(name="Assistant", instructions="You are a helpful assistant")

# Serve the agent on port 8000
serve(agent=math_instructor, port=8000)
```

## API Documentation

AgentServe provides interactive API documentation through two interfaces:

### ReDoc Documentation
Access the ReDoc documentation at `/redoc` when your server is running:
```
http://localhost:8000/redoc
```

ReDoc provides a clean, organized interface with:
- Detailed endpoint descriptions
- Request/response examples
- Interactive API testing
- Schema documentation
- Endpoint grouping by tags

### Swagger UI Documentation
Access the Swagger UI documentation at `/docs`:
```
http://localhost:8000/docs
```

Swagger UI provides:
- Interactive API testing
- Request/response visualization
- Schema exploration
- Try-it-out functionality

### OpenAPI Schema
The OpenAPI schema is available at `/openapi.json`:
```
http://localhost:8000/openapi.json
```

This can be used with any OpenAPI-compatible tools or documentation generators.

## Development

### CI/CD Pipeline

AgentServe uses GitHub Actions for continuous integration and deployment. The pipeline includes:

#### Continuous Integration (`ci.yml`)
- Runs on every push and pull request
- Tests the package with pytest
- Checks code coverage and uploads to Codecov
- Runs code quality checks:
  - Black (code formatting)
  - isort (import sorting)
  - flake8 (linting)
  - mypy (type checking)

#### Release Pipeline (`release.yml`)
- Triggers on version tag pushes (e.g., v1.0.0)
- Builds the package
- Publishes to PyPI

#### Documentation Pipeline (`docs.yml`)
- Builds documentation using MkDocs
- Deploys to GitHub Pages on main branch

### Development Workflow

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Run local checks:
   ```bash
   poetry install
   poetry run pytest
   poetry run black .
   poetry run isort .
   poetry run flake8
   poetry run mypy .
   ```
5. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```
6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. Create a Pull Request

### Release Process

1. Update version in `pyproject.toml`
2. Create and push a new tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. The release pipeline will automatically:
   - Build the package
   - Run all tests
   - Publish to PyPI

### Required Secrets

The following secrets need to be set in your GitHub repository:

- `PYPI_API_TOKEN`: Your PyPI API token for package publishing
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 

