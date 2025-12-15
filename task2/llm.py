import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq  
from langchain_core.prompts import PromptTemplate

from prompts import (
    USER_RESPONSE_PROMPT,
    SUMMARY_PROMPT,
    ACTIONS_PROMPT
)

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

def generate_ai_outputs(rating, review):
    response_chain = PromptTemplate(
        input_variables=["rating", "review"],
        template=USER_RESPONSE_PROMPT
    ) | llm

    summary_chain = PromptTemplate(
        input_variables=["review"],
        template=SUMMARY_PROMPT
    ) | llm

    actions_chain = PromptTemplate(
        input_variables=["review"],
        template=ACTIONS_PROMPT
    ) | llm

    ai_response = response_chain.invoke({
        "rating": rating,
        "review": review
    }).content

    ai_summary = summary_chain.invoke({
        "review": review
    }).content

    ai_actions = actions_chain.invoke({
        "review": review
    }).content

    return ai_response, ai_summary, ai_actions
