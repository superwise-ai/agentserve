# AgentServe

AgentServe is a FastAPI-based server for deploying and serving OpenAI agents. It provides a simple way to expose your agents through a REST API with both synchronous and streaming endpoints.

## Features

- 🚀 Easy deployment of OpenAI agents
- 🔄 Support for both synchronous and streaming responses
- 📚 Automatic API documentation with Swagger UI
- 🔍 Health check and agent info endpoints
- ⚡ Built on FastAPI for high performance

## Quick Start

```bash
# Install the package
pip install openai-agentserve

# Create a basic agent server
from agentserve import serve
from agents import Agent  # Your agent implementation

# Create your agent
agent = Agent(name="MyAgent")

# Start the server
serve(agent, host="0.0.0.0", port=8000)
```

Visit `http://localhost:8000/docs` to see the interactive API documentation.

## Installation

You can install AgentServe using pip:

```bash
pip install openai-agentserve
```

Or using poetry:

```bash
poetry add openai-agentserve
```

## Basic Usage

The main function you'll use is `serve()`, which creates and starts a FastAPI application:

```python
from agentserve import serve
from agents import Agent

def create_app():
    # Create your agent
    agent = Agent(name="MyAgent")
    
    # Create the FastAPI app without starting the server
    app = serve(agent, run_server=False)
    return app

# Or start the server directly
if __name__ == "__main__":
    agent = Agent(name="MyAgent")
    serve(agent, host="0.0.0.0", port=8000) 