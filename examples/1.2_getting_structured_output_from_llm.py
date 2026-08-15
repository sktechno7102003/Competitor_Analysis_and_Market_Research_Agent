# PS -> Call llm, but instead of getting chat output, output must be in JSON format

import os 
from dotenv import load_dotenv 
from langchain_groq import ChatGroq 
from pydantic import BaseModel, Field

load_dotenv() 

# Defining the exact structure of output we want using pydantic
class CompetitorData(BaseModel):
    company_name: str = Field(description="Name of the Competitor")
    has_free_tier : bool = Field(description = "True if they offer a free tier, else false")
    core_features : list[str] = Field(description="List of maximum 3 features mentioned")


model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0)
structured_model = model.with_structured_output(CompetitorData)


messages = [
    (
        "system",
        "You are a helpful Market Research Analysis Agent. Give competitor Analysis of the company the user tells you.",
    ),
    ("human", "Give me Competitor analysis of Chess.com")
]
ai_msg = structured_model.invoke(messages) 
print(ai_msg) 