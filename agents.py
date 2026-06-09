from google.adk import Agent

MODEL = "ollama/qwen2.5:7b"

moderation_agent = Agent(
    name="moderation_agent",
    model=MODEL,
    instruction="""
    Check whether the request is safe.
    allow coding,angular related queries .

    Return ONLY:
    SAFE
    or
    BLOCKED
    """
)

intent_agent = Agent(
    name="intent_agent",
    model=MODEL,
    instruction="""
    Classify intent.

    Return ONLY one:

    coding
    research
    database
    general
    """
)

planner_agent = Agent(
    name="planner_agent",
    model=MODEL,
    instruction="""
    Create an execution plan.

    Return JSON:

    {
      "agent":"coding",
      "task":"..."
    }
    """
)

coding_agent = Agent(
    name="coding_agent",
    model=MODEL,
    instruction="Expert software engineer."
)

research_agent = Agent(
    name="research_agent",
    model=MODEL,
    instruction="Expert researcher."
)

database_agent = Agent(
    name="database_agent",
    model=MODEL,
    instruction="Expert database engineer."
)