import pytest
from fastapi.testclient import TestClient
from agentserve.deployment import serve
from agents import Agent
import json

class DummyTool:
    def run(self, input_text):
        return f"Tool processed: {input_text}"

@pytest.fixture
def test_agent():
    return Agent(tools=[DummyTool()])

@pytest.fixture
def test_client(test_agent):
    app = serve(test_agent)
    return TestClient(app)

def test_invoke_endpoint(test_client):
    response = test_client.post("/invoke", json={"input": "test input"})
    assert response.status_code == 200
    assert response.json() == "Tool processed: test input"

def test_invoke_stream_endpoint(test_client):
    response = test_client.post("/invoke/stream", json={"input": "stream input"}, stream=True)
    assert response.status_code == 200
    for line in response.iter_lines():
        if line:
            data = json.loads(line.split("data: ")[1])
            assert "Tool processed: stream input" in data
            break