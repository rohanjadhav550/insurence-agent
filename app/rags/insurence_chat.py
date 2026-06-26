from app.tools.insurence_policy_scanner import scanner_qwen3_embed, scanner_gemini_embed
from app.tools.loan_request_tool import  index, show, show_by_email_or_phone, show_by_name
from langchain.agents import create_agent
from app.llms.ollama_llms import gemma4
from app.llms.google_genai_llms import gemma426b
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.utils.uuid import uuid7
from typing import AsyncGenerator
from sqlalchemy.orm import Session
from sqlalchemy import text
import json

async def insurence_chat_ollama(prompt: str, thread: str, db: Session)-> AsyncGenerator[str, None]:

    tools = [scanner_qwen3_embed, index, show, show_by_email_or_phone, show_by_name]

    system_prompt = """
        <|think|>
        You are a expert Insurence policy scanner agent, your task is to use the tools properly to scan the insurence policy documents.
        The tools will do searching about the policies from vector stores and provide you the documents. Using those information you have 
        to answer to the user question

        **Rules to follow**
        -> If specific information is asked to retrive (Ex. find policy number, get policy number, get policy holder name etc.,), specifically mention
        tools to get those keys itself, No nearby keys or similer keys data is expected to be retrived.
        -> Always tell the tools to get the search results from the specified policy document only if mentioned. Never deviate from that document.
        -> If user have asked to retrive any data like loan request data or any, use the loan_requet_tool's tools

        **Steps to do**
        1. Take the question and understand the emotion of the question
        2. If there are direct values or data given then carefully tell the tools that there is specific data being asked by the user in the 
        question. If there are generic questions involved then frame the prompt to the tools for the optimal results to be picked
        3. Analyze the documents provided by the tools. It is very important for you to be 200 percent sure that the retrived
        document or the data from the tools answer the user question itself.
        4. If not then improvise the query you made to the tools and get the results. Do the step3 and step 4 till you get the aaccurate results. But 
        never exceed the try count more then 3
        5. After the confirmation, if there are any answers then produce them to the user in easy and readble format. If there are no results retrived
        form the  tools or datasources then straigh away tell user there is no information. You must be very honest about it and scanning or any operation must
        be arround the data we have in our sources it self.
        """
    agent = create_agent(
        model=gemma4(),
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=InMemorySaver(),
    )

    config = {"configurable": {"thread_id": thread}}

    # 1. Save user message BEFORE calling agent
    db.execute(
        text("INSERT INTO messages (thread_id, role, content) VALUES (:thread_id, :role, :content)"),
        {"thread_id": thread, "role": "user", "content": prompt}
    )
    db.commit()

    full_response = ""
    reasoning_started = False

    def sse(type: str, content: str) -> str:
        """Format as SSE JSON event"""
        return f"data: {json.dumps({'type': type, 'content': content})}\n\n"

    async for event in agent.astream_events(
        {"messages": [{"role": "user", "content": prompt}]},
        config=config,
        version="v2"
    ):
        kind = event["event"]
        data = event.get("data", {})

        if kind == "on_chat_model_stream":
            chunk = data.get("chunk")
            if chunk:
                # Reasoning tokens
                reasoning_delta = chunk.additional_kwargs.get("reasoning_content", "")
                if reasoning_delta:
                    if not reasoning_started:
                        yield sse("think_start", "")
                        reasoning_started = True
                    yield sse("thinking", reasoning_delta)

                # Response tokens
                if isinstance(chunk.content, str) and chunk.content:
                    if reasoning_started:
                        yield sse("think_end", "")
                        reasoning_started = False
                    full_response += chunk.content
                    yield sse("text", chunk.content)

        elif kind == "on_tool_start":
            tool_name = event.get("name", "")
            tool_input = data.get("input", {})
            yield sse("tool_start", json.dumps({"name": tool_name, "input": tool_input}))

        elif kind == "on_tool_end":
            yield sse("tool_end", "")

    # Save assistant response
    if full_response:
        db.execute(
            text("INSERT INTO messages (thread_id, role, content) VALUES (:thread_id, :role, :content)"),
            {"thread_id": thread, "role": "assistant", "content": full_response}
        )
        db.execute(
            text("UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE thread_id = :thread_id"),
            {"thread_id": thread}
        )
        db.commit()
    

async def insurence_chat_gemini(prompt: str, thread: str, db: Session) -> AsyncGenerator[str, None]:

    tools = [scanner_gemini_embed, index, show, show_by_email_or_phone, show_by_name]

    system_prompt = """
        You are a expert Insurence policy scanner agent, your task is to use the tools properly to scan the insurence policy documents.
        The tools will do searching about the policies from vector stores and provide you the documents. Using those information you have 
        to answer to the user question

        **Rules to follow**
        -> If specific information is asked to retrive (Ex. find policy number, get policy number, get policy holder name etc.,), specifically mention
        tools to get those keys itself, No nearby keys or similer keys data is expected to be retrived.
        -> Always tell the tools to get the search results from the specified policy document only if mentioned. Never deviate from that document.

        **Steps to do**
        1. Take the question and understand the emotion of the question
        2. If there are direct values or data given then carefully tell the tools that there is specific data being asked by the user in the 
        question. If there are generic questions involved then frame the prompt to the tools for the optimal results to be picked
        3. Analyze the documents provided by the tools. It is very important for you to be 200 percent sure that the retrived
        document or the data from the tools answer the user question itself.
        4. If not then improvise the query you made to the tools and get the results. Do the step3 and step 4 till you get the aaccurate results. But 
        never exceed the try count more then 3
        5. After the confirmation, if there are any answers then produce them to the user in easy and readble format. If there are no results retrived
        form the  tools or datasources then straigh away tell user there is no information. You must be very honest about it and scanning or any operation must
        be arround the data we have in our sources it self.
        """

    agent = create_agent(
        model=gemma426b(),
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=InMemorySaver(),
    )

    config = {"configurable": {"thread_id": thread}}

    # Save user message BEFORE calling agent
    db.execute(
        text("INSERT INTO messages (thread_id, role, content) VALUES (:thread_id, :role, :content)"),
        {"thread_id": thread, "role": "user", "content": prompt}
    )
    db.commit()

    full_response = ""
    reasoning_started = False

    def sse(type: str, content: str) -> str:
        """Format as SSE JSON event"""
        return f"data: {json.dumps({'type': type, 'content': content})}\n\n"

    async for event in agent.astream_events(
        {"messages": [{"role": "user", "content": prompt}]},
        config=config,
        version="v2"
    ):
        kind = event["event"]
        data = event.get("data", {})

        if kind == "on_chat_model_stream":
            chunk = data.get("chunk")
            if not chunk:
                continue

            content = chunk.content

            # ── Gemini thinking models: content is a list of parts ──
            if isinstance(content, list):
                for part in content:
                    if not isinstance(part, dict):
                        continue

                    if part.get("type") == "thinking":
                        thinking_text = part.get("thinking", "")
                        if thinking_text:
                            if not reasoning_started:
                                yield sse("think_start", "")
                                reasoning_started = True
                            yield sse("thinking", thinking_text)

                    elif part.get("type") == "text":
                        text_delta = part.get("text", "")
                        if text_delta:
                            if reasoning_started:
                                yield sse("think_end", "")
                                reasoning_started = False
                            full_response += text_delta
                            yield sse("text", text_delta)

            # ── Plain string: check additional_kwargs first for reasoning ──
            elif isinstance(content, str):
                reasoning_delta = chunk.additional_kwargs.get("reasoning_content", "")
                if reasoning_delta:
                    if not reasoning_started:
                        yield sse("think_start", "")
                        reasoning_started = True
                    yield sse("thinking", reasoning_delta)

                if content:
                    if reasoning_started:
                        yield sse("think_end", "")
                        reasoning_started = False
                    full_response += content
                    yield sse("text", content)

        elif kind == "on_tool_start":
            tool_name = event.get("name", "")
            tool_input = data.get("input", {})
            yield sse("tool_start", json.dumps({"name": tool_name, "input": tool_input}))

        elif kind == "on_tool_end":
            yield sse("tool_end", "")

    # Close thinking block if model stopped mid-thought
    if reasoning_started:
        yield sse("think_end", "")

    # Save assistant response
    if full_response:
        db.execute(
            text("INSERT INTO messages (thread_id, role, content) VALUES (:thread_id, :role, :content)"),
            {"thread_id": thread, "role": "assistant", "content": full_response}
        )
        db.execute(
            text("UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE thread_id = :thread_id"),
            {"thread_id": thread}
        )
        db.commit()
