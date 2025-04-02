# Examples

## Basic Example

Here's a basic example of creating and serving an agent:

```python
from agentserve import serve
from agents import Agent

# Create a simple agent
agent = Agent(
    name="EchoAgent",
    description="A simple agent that echoes back the input",
    capabilities=["echo"]
)

# Start the server
serve(agent, host="0.0.0.0", port=8000)
```

## Using with FastAPI

You can integrate AgentServe with an existing FastAPI application:

```python
from fastapi import FastAPI
from agentserve import serve
from agents import Agent

# Create your FastAPI app
app = FastAPI()

# Add some custom routes
@app.get("/custom")
async def custom_endpoint():
    return {"message": "Custom endpoint"}

# Create your agent
agent = Agent(name="MyAgent")

# Add AgentServe routes to your app
serve(agent, app=app, run_server=False)

# Start the server using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Making Requests

### Synchronous Request

Using Python requests:

```python
import requests

response = requests.post(
    "http://localhost:8000/agent/invoke",
    json={
        "question": "What is 2+2?",
        "stream": False
    }
)
print(response.json())
```

Using curl:

```bash
curl -X POST http://localhost:8000/agent/invoke \
    -H "Content-Type: application/json" \
    -d '{"question": "What is 2+2?", "stream": false}'
```

### Streaming Request

Using Python requests:

```python
import requests

response = requests.post(
    "http://localhost:8000/agent/invoke",
    json={
        "question": "Tell me a story",
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        print(line.decode())
```

Using curl:

```bash
curl -X POST http://localhost:8000/agent/invoke \
    -H "Content-Type: application/json" \
    -H "Accept: text/event-stream" \
    -d '{"question": "Tell me a story", "stream": true}'
```

## Advanced Configuration

You can customize the server behavior with additional parameters:

```python
from agentserve import serve
from agents import Agent

agent = Agent(name="MyAgent")

serve(
    agent,
    host="0.0.0.0",
    port=8000,
    workers=4,              # Number of worker processes
    log_level="debug",      # Logging level
    cors_origins=["*"],     # CORS origins
    timeout=30,             # Request timeout in seconds
)
``` 