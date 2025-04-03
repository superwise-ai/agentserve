import warnings

from pydantic import BaseModel, ConfigDict, Field

# Suppress FastAPI's internal Pydantic deprecation warning
warnings.filterwarnings("ignore", message=".*general_plain_validator_function.*")


class QuestionRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "properties": {
                "input": {
                    "example": "Can you help me solve this equation: 2x + 5 = 15?"
                },
                "stream": {"example": False},
            }
        }
    )

    input: str = Field(..., description="The input text to send to the agent")
    stream: bool = Field(
        default=False,
        description="Whether to stream the response or return it all at once",
    )


class HealthResponse(BaseModel):
    """Response model for the health check endpoint."""

    model_config = ConfigDict(
        json_schema_extra={
            "properties": {
                "status": {"example": "healthy"},
                "agent": {"example": "Assistant"},
            }
        }
    )

    status: str = Field(..., description="The current health status of the service")
    agent: str = Field(..., description="The name of the currently deployed agent")


class AgentInfoResponse(BaseModel):
    """Response model for the agent information endpoint."""

    model_config = ConfigDict(
        json_schema_extra={
            "properties": {
                "name": {"example": "Assistant"},
                "type": {"example": "Agent"},
            }
        }
    )

    name: str = Field(..., description="The name of the agent")
    type: str = Field(..., description="The type/class of the agent")
