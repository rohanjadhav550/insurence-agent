from app.tools.insurence_policy_scanner import scanner_qwen3_embed, scanner_gemini_embed
from langchain.agents import create_agent
from app.llms.google_genai_llms import gemma426b
from app.llms.ollama_llms import gemma4
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

def insurence_chat_ollama(prompt):

    tools = [scanner_qwen3_embed]

    system_prompt = """
        You are a expert Insurence policy scanner agent, your task is to use the tools properly to scan the insurence policy documents.
        The tools will do searching about the policies from vector stores and provide you the documents. Using those information you have 
        to answer to the user question
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
        system_prompt=system_prompt
    )

    stream = agent.stream_events(
        {"messages":[{"role":"user","content": prompt}]},
        version="v3"
    )

    for message in stream.messages:
       for delta in message.text:
           print(delta, end="", flush=True)
    final_state = stream.output

