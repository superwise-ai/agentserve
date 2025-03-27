from agents import Agent
from agentserve import serve

agent = Agent(name="Assistant", instructions="You are a helpful assistant")
serve(agent)