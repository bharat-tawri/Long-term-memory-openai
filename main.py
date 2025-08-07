# main.py
from langgraph.graph import StateGraph, END
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.prompts import PromptTemplate

import os
from typing import Dict, List
import uuid

# Load environment
from dotenv import load_dotenv
load_dotenv()

embedding = OpenAIEmbeddings()
vectorstore = Chroma(collection_name="dynamic-memory", embedding_function=embedding)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Prompts
intent_prompt = PromptTemplate.from_template("""
Decide the intent behind the user message.

Message: "{input}"

Respond with one of: "store", "update", "delete", or "query"
""")

fact_extractor = PromptTemplate.from_template("""
Extract a concise fact or any other important information from this message.
Example -
- "My name is Bharat" → "User's name is Bharat"
- "I like icecream" → "User likes icecream"
- "I wish to be a Data scientist at Shram"
Message: "{input}"
Fact:
""")

improved_intent_prompt = PromptTemplate.from_template("""
Classify the user's intent behind this message.

Message: "{input}"

Respond with only one word: "store", "update" or "query"

Examples:
- "I use Notion and Trello for productivity" → store
- "What tools do I use?" → query
- "I like chocolates and ice cream" → store
- "Do I like chocolate?" → query
- "I am using Figma instead of Photoshop" → update
- "Tell me my name" → query
""")

def store_or_update_fact(state: Dict[str, str]) -> Dict[str, str]:
    user_input = state["user_input"]

    intent = llm.invoke(improved_intent_prompt.format(input=user_input)).content.strip().lower()
    print(f"[🧠 Memory Action Detected: \"{intent}\"]")

    if intent in ["store", "update"]:
        fact = llm.invoke(fact_extractor.format(input=user_input)).content.strip()
        memory_id = str(uuid.uuid4())
        vectorstore.add_texts([fact], metadatas=[], ids=[memory_id])
        
    return state

def retrieve_and_respond(state: Dict[str, str]) -> Dict[str, str]:
    user_input = state["user_input"]
    print("[🔍 Retrieving memory]")
    relevant = vectorstore.similarity_search(user_input, k=5)
    history = "\n".join([doc.page_content for doc in relevant]) if relevant else "None"

    prompt = PromptTemplate.from_template("""
Use the following memory to answer the user if the memory seems relevant to the input otherwise ignore it:

Memory:
{memory}

User:
{input}

Answer:
""")

    response = llm.invoke(prompt.format(input=user_input, memory=history))
    state["response"] = response.content.strip()
    return state

# Build LangGraph
State = Dict[str, str]

graph_builder = StateGraph(State)
graph_builder.add_node("store_or_update", store_or_update_fact)
graph_builder.add_node("respond", retrieve_and_respond)
graph_builder.set_entry_point("store_or_update")
graph_builder.add_edge("store_or_update", "respond")
graph_builder.add_edge("respond", END)

graph = graph_builder.compile()

# Entry point for API
def process_input(user_input: str) -> str:
    result = graph.invoke({"user_input": user_input})
    return result["response"]
