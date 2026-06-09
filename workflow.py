from google.adk import Workflow

from agents import (
    moderation_agent,
    intent_agent,
    planner_agent
)

root_agent = Workflow(
    name="root_workflow",
    edges=[
        (
            "START",
            moderation_agent,
            intent_agent,
            planner_agent
        )
    ]
)