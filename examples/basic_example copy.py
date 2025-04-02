from agents import Agent

from agentserve import DockerDeployment, LambdaDeployment


class BaseDeployment(BaseModel):
    agent_name: str
    handler: str
    openai_api_key: str
    openai_base_url: str


deployment = DockerDeployment(
    agent_name="Agent",
    handler="basic_example.py",
    image_tag="docker.io/agent-serve/basic-example:latest",
    docker_host="localhost:2375",
    openai_api_key="sk-proj-1234567890",
    openai_base_url="https://api.openai.com/v1",
)
deployment.deploy()


lambda_deployment = LambdaDeployment(
    agent_name="Agent",
    handler="basic_example.py",
    aws_access_key_id="AKIAIOSFODNN7EXAMPLE",
    aws_secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    aws_region="us-east-1",
    openai_api_key="sk-proj-1234567890",
    openai_base_url="https://api.openai.com/v1",
)
lambda_deployment.deploy()
