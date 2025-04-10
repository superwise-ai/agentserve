import importlib.util
import sys
from pathlib import Path
from typing import Any

import typer
from agents import Agent
from rich import print

from agentserve import serve


def load_agent_module(path: str) -> Any:
    """Load an agent module from a Python file."""
    path = Path(path)
    if not path.exists():
        raise typer.BadParameter(f"Agent file not found: {path}")

    if not path.is_file() or path.suffix != ".py":
        raise typer.BadParameter(f"Agent path must be a Python file: {path}")

    spec = importlib.util.spec_from_file_location("agent_module", path)
    if not spec or not spec.loader:
        raise typer.BadParameter(f"Could not load agent module: {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["agent_module"] = module
    spec.loader.exec_module(module)
    return module


def validate_agent(obj: Any) -> Agent:
    """Validate that an object is an OpenAI Agent instance."""
    if not isinstance(obj, Agent):
        raise typer.BadParameter(
            f"Object '{obj}' is not an OpenAI Agent instance. "
            f"Got type: {type(obj).__name__}"
        )
    return obj


app = typer.Typer(
    name="agentserve",
    help="Deploy OpenAI Agents as web services.",
    add_completion=False,
)


@app.command()
def api(
    agent_path: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        help="Path to the Python file containing the agent definition",
    ),
    agent_name: str = typer.Argument(
        ...,
        help="Name of the agent variable in the Python file",
    ),
    host: str = typer.Option(
        "127.0.0.1",
        "--host",
        "-h",
        help="Host to bind to",
    ),
    port: int = typer.Option(
        8000,
        "--port",
        "-p",
        help="Port to bind to",
    ),
) -> None:
    """
    Serve an OpenAI agent as a web service.

    The agent must be defined and instantiated in the specified Python file.
    """
    try:
        module = load_agent_module(str(agent_path))

        if not hasattr(module, agent_name):
            available_attrs = [attr for attr in dir(module) if not attr.startswith("_")]
            attrs_str = ", ".join(available_attrs) or "none"
            msg = (
                f"Agent '{agent_name}' not found in {agent_path}. "
                f"Available non-private attributes: {attrs_str}"
            )
            raise typer.BadParameter(msg)

        agent = validate_agent(getattr(module, agent_name))

        print(f"[green]Starting agent server on http://{host}:{port}[/green]")
        serve(agent, host=host, port=port)

    except Exception as e:
        raise typer.BadParameter(str(e))


@app.callback()
def callback():
    """
    Deploy OpenAI Agents as web services.
    """
    pass


def main() -> None:
    app()
