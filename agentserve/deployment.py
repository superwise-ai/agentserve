import warnings
from typing import AsyncGenerator

import uvicorn
from agents import Agent, Runner
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.responses import StreamingResponse

from agentserve.logging_config import get_logger
from agentserve.models import AgentInfoResponse, HealthResponse, QuestionRequest

# Suppress the Pydantic deprecation warning from FastAPI
warnings.filterwarnings("ignore", message=".*general_plain_validator_function.*")

logger = get_logger(__name__)


def serve(
    agent: Agent, host: str = "0.0.0.0", port: int = 8000, run_server: bool = True
):
    """
    Create and serve a FastAPI application that wraps the provided agent.

    Args:
        agent: The OpenAI agent to serve
        host: Host to bind the server to
        port: Port to bind the server to
        run_server: Whether to start the server (True) or just return the app (False)
    """
    logger.info(f"Starting server for agent '{agent.name}' on {host}:{port}")

    app = FastAPI(
        title=f"{agent.name} API",
        description=f"""
        API for invoking the {agent.name} OpenAI agent.

        This API provides endpoints to interact with the agent in both synchronous
        and streaming modes.

        ## Features
        - Synchronous request/response
        - Server-sent events streaming
        - Health check endpoint
        - Agent information endpoint

        ## Authentication
        Currently, this API does not require authentication.

        ## Rate Limiting
        No rate limiting is implemented at this time.
        """,
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    async def stream_generator(
        agent: Agent, question: str
    ) -> AsyncGenerator[str, None]:
        """Generate streaming responses from the agent."""
        logger.debug(f"Starting stream generation for question: {question[:50]}...")
        result = Runner.run_streamed(agent, input=question)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, "delta"):
                yield event.data.delta
        logger.debug("Stream generation completed")

    @app.post(
        "/invoke",
        response_description="The agent's response to the input query",
        summary="Invoke the agent",
        description="""
        Send a query to the agent and receive a response.

        This endpoint can process the input either synchronously or as a stream.
        Set stream=true to receive the response as it's being generated.
        """,
        tags=["Agent Operations"],
    )
    async def invoke_agent(request: QuestionRequest):
        logger.info(
            f"Received invoke request: {request.input[:50]}... "
            f"(stream={request.stream})"
        )
        try:
            if request.stream:
                logger.debug("Starting streaming response")
                return StreamingResponse(
                    stream_generator(agent, request.input),
                    media_type="text/event-stream",
                )
            else:
                result = await Runner.run(agent, input=request.input)
                logger.info("Successfully processed invoke request")
                return result
        except Exception as e:
            logger.error(f"Error processing invoke request: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

    @app.get(
        "/health",
        response_model=HealthResponse,
        response_description="The health status of the service",
        summary="Check service health",
        description="Returns the current health status of the service and the agent.",
        tags=["System"],
    )
    def health_check():
        logger.debug("Health check requested")
        return HealthResponse(status="healthy", agent=agent.name)

    @app.get(
        "/info",
        response_model=AgentInfoResponse,
        response_description="Information about the agent",
        summary="Get agent information",
        description="Returns basic information about the deployed agent.",
        tags=["System"],
    )
    def agent_info():
        logger.debug("Agent info requested")
        return AgentInfoResponse(name=agent.name, type=type(agent).__name__)

    # Customize OpenAPI schema
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        # Add custom tags
        openapi_schema["tags"] = [
            {
                "name": "Agent Operations",
                "description": "Endpoints for interacting with the agent",
            },
            {"name": "System", "description": "System-related endpoints"},
        ]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    if run_server:
        logger.info("Starting uvicorn server")
        uvicorn.run(app, host=host, port=port)
    else:
        return app
