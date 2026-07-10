from langchain.tools import tool
from dotenv import load_dotenv
from sqlalchemy import text, inspect
from database.connection import get_b2b_db
from app.tools.database_tools.database_overall_tools import show_tables, table_details, select_query_executor
from app.llms.ollama_llms import gemma4, qwen354b, qwen354b_no_think
from langchain.agents import create_agent
from typing import AsyncGenerator
import json

load_dotenv()

@tool
def database_tables_scann_agent_tool(prompt: str):
    """Sub agent to look up raw facts about the database (table names, schema details, query rows).
    It only gathers and reports data - it never answers the user's question or adds analysis/recommendations.
    Args:
        prompt (str): What data to look up in the database.
    Returns:
        str: The raw data found, to be interpreted and answered by the calling agent."""

    system_prompt = """
        You are a data-retrieval worker for a database. Your only job is to call the available tools
        (show_tables, table_details, select_query_executor) to gather the exact facts requested and
        report them back.

        **Rules**
        -> Do NOT answer the user's underlying question, draw conclusions, give recommendations, or add
        commentary. You are not talking to the end user.
        -> Only call the tools needed to satisfy the request, then respond with the raw data you found
        (table names, column/key/index details, or query rows) in a clear structured form.
        -> If a tool returns no data or an error, report that fact plainly instead of guessing or
        filling gaps with assumptions.
        """

    agent = create_agent(
        model=qwen354b_no_think(),
        tools=[show_tables,table_details, select_query_executor],
        system_prompt=system_prompt
    )

    # config={"callbacks": []} cuts inheritance of the parent agent's callback manager
    # (LangChain propagates it via a contextvar by default), so this subagent's own
    # token stream and internal tool calls don't leak into the parent's astream_events feed.
    result = agent.invoke(
        {"messages": [{"role": "user", "content": prompt}]},
        config={"callbacks": [], "run_name": "database_tables_scann_agent_tool"},
    )
    return result["messages"][-1].content

