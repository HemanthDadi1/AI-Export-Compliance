"""The CImEx Review Agent, built with Google's Agent Development Kit. Needs google-adk (Python 3.10+)."""
import os
from pathlib import Path

from google.adk.agents import Agent

from agent import tools

MODEL = os.environ.get("AGENT_MODEL", "gemini-3.8-flash")  # 2.5 Flash is closed to new API users; set AGENT_MODEL to try others

root_agent = Agent(
    name="cimex_review_agent",
    model=MODEL,
    description="Reviews a plant's CBAM files like a verifier, ranks what to fix, asks the clerk, and drafts the mill request.",
    instruction=Path(__file__).with_name("skill.md").read_text(),
    tools=tools.ALL,
)
