from app.tools.insurence_policy_scanner import scanner_qwen3_embed, scanner_gemini_embed
from langchain.agents import create_agent
from app.llms.ollama_llms import gemma4
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.utils.uuid import uuid7
import os
from typing import AsyncGenerator

async def insurence_chat_ollama(prompt)-> AsyncGenerator[str, None]:

    tools = [scanner_qwen3_embed]

    system_prompt = """
        <|think|>
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
        model=gemma4(),
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=InMemorySaver(),
    )

    config = {"configurable": {"thread_id": str(uuid7())}}

    stream = await agent.astream_events({
        "messages":[
            {"role":"user", "content":prompt}
        ]
    },
    config=config,
    version="v3")

    async for message in stream.messages:
        if hasattr(message, 'reasoning'):
            yield "\n🧠THINKING......\n"
            async for delta in message.reasoning:
                yield delta
            yield "\n"
        if hasattr(message, 'text') and message.text:
            async for delta in message.text:
                yield delta

    async for call in stream.tool_calls:
        async for delta in call.output_deltas:
            yield delta
