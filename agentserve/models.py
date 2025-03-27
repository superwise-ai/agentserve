from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    input: str = Field(
        ...,
        description="The input text to send to the agent",
        example="Can you help me solve this equation: 2x + 5 = 15?"
    )
    stream: bool = Field(
        default=False,
        description="Whether to stream the response or return it all at once",
        example=False
    )

    class Config:
        json_schema_extra = {
            "example": {
                "input": "Can you help me solve this equation: 2x + 5 = 15?",
                "stream": False
            }
        }


class HealthResponse(BaseModel):
    """Response model for the health check endpoint."""
    status: str = Field(
        ...,
        description="The current health status of the service",
        example="healthy"
    )
    agent: str = Field(
        ...,
        description="The name of the currently deployed agent",
        example="Assistant"
    )


class AgentInfoResponse(BaseModel):
    """Response model for the agent information endpoint."""
    name: str = Field(
        ...,
        description="The name of the agent",
        example="Assistant"
    )
    type: str = Field(
        ...,
        description="The type/class of the agent",
        example="Agent"
    ) 