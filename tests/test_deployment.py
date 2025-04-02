import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from agentserve import serve
from agents import Agent, Runner
from unittest.mock import AsyncMock, MagicMock, patch
from asyncio import TimeoutError
from typing import Any, Dict, List, Optional

# Test Constants
TEST_AGENT_NAME = "TestAgent"
TEST_AGENT_INSTRUCTIONS = "Test agent for processing inputs"
DEFAULT_TEST_INPUT = "test input"
DEFAULT_RESPONSE = {"output": "Test response"}

# Test Utilities
def assert_json_response(response: Any, expected_status: int, expected_data: Optional[Dict] = None) -> None:
    """Utility to assert JSON response status and data"""
    assert response.status_code == expected_status
    if expected_data:
        assert response.json() == expected_data

def assert_stream_response(response: Any, expected_status: int = 200) -> None:
    """Utility to assert stream response basics"""
    assert response.status_code == expected_status
    assert response.headers["content-type"].startswith("text/event-stream")

def make_invoke_request(client: TestClient, input_text: str, stream: bool = False) -> Any:
    """Utility to make an invoke request"""
    return client.post("/invoke", json={"input": input_text, "stream": stream})

# Mock Stream Results
class BaseStreamResult:
    """Base class for stream results with common utilities"""
    @staticmethod
    def create_event(delta: str) -> MagicMock:
        return MagicMock(type="raw_response_event", data=MagicMock(delta=f"data: {delta}\n\n"))

class MockStreamResult(BaseStreamResult):
    """Single chunk stream result"""
    async def stream_events(self):
        yield self.create_event("Test response chunk")

# Fixtures
@pytest.fixture
def mock_run():
    """Fixture for mocking Runner.run"""
    with patch.object(Runner, 'run', new_callable=AsyncMock) as mock:
        mock.return_value = DEFAULT_RESPONSE
        yield mock

@pytest.fixture
def mock_run_streamed():
    """Fixture for mocking Runner.run_streamed"""
    with patch.object(Runner, 'run_streamed') as mock:
        mock.return_value = MockStreamResult()
        yield mock

@pytest.fixture
def test_agent():
    """Fixture for creating a test agent"""
    return Agent(
        name=TEST_AGENT_NAME,
        instructions=TEST_AGENT_INSTRUCTIONS
    )

@pytest.fixture
def test_client(test_agent):
    """Fixture for creating a test client"""
    app = serve(test_agent, run_server=False)
    return TestClient(app)

class TestBasicEndpoints:
    """Tests for basic endpoint functionality"""
    
    def test_health_check(self, test_client):
        """Test the health check endpoint"""
        response = test_client.get("/health")
        expected_data = {
            "status": "healthy",
            "agent": TEST_AGENT_NAME
        }
        assert_json_response(response, 200, expected_data)
        # Additional type checks
        data = response.json()
        assert all(isinstance(data[key], str) for key in ["status", "agent"])

    def test_agent_info(self, test_client):
        """Test the agent info endpoint"""
        response = test_client.get("/info")
        expected_data = {
            "name": TEST_AGENT_NAME,
            "type": "Agent"
        }
        assert_json_response(response, 200, expected_data)

class TestSyncInvoke:
    """Tests for synchronous invocation endpoint"""
    
    def test_invoke_endpoint(self, test_client, mock_run, test_agent):
        """Test basic synchronous invocation"""
        response = make_invoke_request(test_client, DEFAULT_TEST_INPUT)
        assert_json_response(response, 200, DEFAULT_RESPONSE)
        mock_run.assert_called_once_with(test_agent, input=DEFAULT_TEST_INPUT)

    @pytest.mark.parametrize("input_text, description", [
        ("", "empty input"),
        ("test " * 1000, "large input"),
        ("!@#$%^&*()_+<>?:\"{}|", "special characters"),
        ("Hello\nWorld\n\r\t", "whitespace and newlines"),
        ("测试", "unicode characters"),
    ])
    def test_invoke_with_various_inputs(self, test_client, mock_run, test_agent, input_text, description):
        """Test invocation with various input types"""
        response = make_invoke_request(test_client, input_text)
        assert_json_response(response, 200, DEFAULT_RESPONSE)
        mock_run.assert_called_once_with(test_agent, input=input_text)

class TestStreamInvoke:
    """Tests for streaming invocation endpoint"""
    
    def test_basic_stream(self, test_client, mock_run_streamed, test_agent):
        """Test basic streaming functionality"""
        response = make_invoke_request(test_client, DEFAULT_TEST_INPUT, stream=True)
        assert_stream_response(response)
        first_line = next(response.iter_lines())
        assert first_line.startswith("data: ")  # Using string literal for comparison
        mock_run_streamed.assert_called_once_with(test_agent, input=DEFAULT_TEST_INPUT)

class TestInputValidation:
    """Tests for input validation"""
    
    @pytest.mark.parametrize("request_data, expected_status", [
        ({"stream": False}, 422),                    # Missing input
        ("invalid json", 422),                       # Invalid JSON
        ({"input": None, "stream": False}, 422),     # Null input
        ({"input": 123, "stream": False}, 422),      # Wrong input type
    ])
    def test_invalid_requests(self, test_client, request_data, expected_status):
        """Test various invalid request scenarios"""
        if isinstance(request_data, dict):
            response = test_client.post("/invoke", json=request_data)
        else:
            response = test_client.post("/invoke", data=request_data)
        assert response.status_code == expected_status

class TestConcurrency:
    """Tests for concurrent request handling"""
    
    @pytest.mark.parametrize("num_requests", [2, 5, 10])
    def test_concurrent_requests(self, test_client, mock_run, num_requests):
        """Test handling of concurrent requests"""
        import concurrent.futures
        
        def make_request():
            return make_invoke_request(test_client, DEFAULT_TEST_INPUT)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            responses = [future.result() for future in futures]
        
        for response in responses:
            assert_json_response(response, 200, DEFAULT_RESPONSE)
        
        assert mock_run.call_count == num_requests
