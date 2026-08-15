# PS -> When Tracking Competitors, Product Managers need to categorize them. Instead of letting the LLM invent random categories
# (like "Cheap", "Budget", "Inexpensive"), how do we force the LLM to choose only from an approved list of business segments ?

# PS -> You are building an agent that scraped competitor pricing pages. However, SaaS companies often hide pricing , 
# say "Contact Sales", or use confusing tiers. How do youdesign an llm schema that safely captures numeric values 
# when present, but doesn't hallucinate or crash when the data is missing

from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from typing import Optional
from enum import Enum

load_dotenv()


# 1. Defining strict categorical Enums
class MarketSegment(str, Enum):
    LOW_COST = "low_cost"
    MID_MARKET = "mid_market"
    ENTERPRISE = "enterprise_luxury"
# Isse ab ye kisi aur model ka input banta hai to there will be no confusion ki modle ne low cost ko, cheap cost likha
# because there in no option for cheap cost anymore, the llm space is limited by these three options only for segment.

class CompetitorAnalysis(BaseModel):
    competitor_name : str
    segment : MarketSegment = Field(description="Classify the competitor's market segment based on the text.")
    # yaha pe ab segment ke value bas ti hi ho skte hai, jo ki apan ne pahle se define kr rakha tha no confusion or spelling mistake
    confidence_score : int = Field(description="Score from 1-10 on how confident you are in this classification.")

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0)

structured_model = model.with_structured_output(CompetitorAnalysis)

System_Prompt = """
You are a Market Strategist Agent. Classify the competitor based on their marketing copy.
"""

User_Input = """
At Hypertech, We don't do cheap. We build bespoke, high-security infrastructure for Fortune 500 banks.
"""
messages = [
    ("system", System_Prompt),
    ("human", User_Input)
]

ai_msg = structured_model.invoke(messages) 
print(ai_msg.segment.value) 