from langchain.tools import tool
from dotenv import load_dotenv
from sqlalchemy import text, inspect
from database.connection import get_b2b_db
from app.tools.database_tools.database_overall_tools import show_tables, table_details, select_query_executor
from app.llms.google_genai_llms import gemma426b
from app.llms.ollama_llms import gemma4, gemma412b
from langchain.agents import create_agent

load_dotenv()

def database_tables_scann_gemma426b_tool(prompt):
    system_prompt = """
        You helpfull in finding the tables, there descriptions and details present in the database.
        """

    agent = create_agent(
        model=gemma412b(),
        tools=[show_tables,table_details, select_query_executor],
    )

    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": prompt}]},
        stream_mode="messages",
        version="v2",
    ):
        if chunk["type"] == "messages":
            token, metadata = chunk["data"]
            if(len(token.content_blocks)):
                if(token.content_blocks[-1]['type'] == "reasoning"):
                    print(token.content_blocks[-1]['reasoning'], end=" ", flush=True)
                elif(token.content_blocks[-1]['type'] == "tool_call"):
                    print(f"Tool: {token.content_blocks[-1]['name']}", end=" ", flush=True)
                    print(f"Arguments: {token.content_blocks[-1]['args']}", end=" ", flush=True)
                else:
                    print(token.content_blocks[-1]['text'], end=" ", flush=True)
                    
            print("\n") 

def database_tables_scann_gemma4_tool(prompt):
    system_prompt = """
        <|think|>
        You helpfull in finding the tables, there descriptions and details present in the database.
        """

    agent = create_agent(
        model=gemma412b(),
        tools=[show_tables,table_details, select_query_executor],
        system_prompt=system_prompt
    )

    for chunk in agent.stream(
        {"messages": [prompt]},
        stream_mode=["messages", "updates"],
        version="v2",
    ):

        print(chunk)

database_tables_scann_gemma4_tool("find me latest loans and there loan requests")