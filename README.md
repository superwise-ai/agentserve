# AgentServe

A simple and efficient tool to deploy OpenAI Agents as FastAPI web services.

## Overview

AgentServe is a lightweight wrapper that allows you to easily serve OpenAI Agents as web services. It provides a simple API for interacting with agents, supporting both synchronous and streaming responses.

## Installation

```bash
pip install openai-agentserve
```

Or with Poetry:

```bash
poetry add openai-agentserve
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
my_agent = Agent(name="Assistant", instructions="You are a helpful assistant")

# Serve the agent on port 8000
serve(agent=my_agent, port=8000)
```

## Usage Examples

### Invoking the API

The API supports both streaming and non-streaming responses.

#### Streaming Response

```python
import requests

url = "http://localhost:8000/invoke"

response = requests.post(url, json={
    "input": "please tell me a about the history of the world",
    "stream": True
    }, stream=True)
for i, line in enumerate(response.iter_lines()):
    if line:
        decoded_line = line.decode('utf-8').strip()
        print(decoded_line)
```

#### Non-Streaming Response

```python
import requests

url = "http://localhost:8000/invoke"

response = requests.post(url, json={
    "input": "please tell me about the history of the world",
    "stream": False
})
result = response.json()
print(result)
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

For information about CI/CD pipelines and GitHub Actions workflows, see [.github/workflows/README.md](.github/workflows/README.md).

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 

