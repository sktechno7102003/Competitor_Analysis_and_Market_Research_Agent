# PS -> You are building an agent that scraped competitor pricing pages. However, SaaS companies often hide pricing , 
# say "Contact Sales", or use confusing tiers. How do youdesign an llm schema that safely captures numeric values 
# when present, but doesn't hallucinate or crash when the data is missing

from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from typing import Optional # python me data structre explicitly define nhi krte, typinh apne ko wo feature deta hai

load_dotenv()

# 1. Defining the schema with safe optional fallback -> optional mtlb wo field optional hai like middle name so
# so agar user de rha hai to thik otherwise koi dikkat nhi hai
class PricingTier(BaseModel):
    tier_name : str = Field(description="Name of the plan (eg. Basic, Pro, Enterprise)")
    price_per_month : Optional[float] = Field(description="Monthly Price in USD. Return null if it says 'Contact Sales' or is hidden")
    requires_contact : bool = Field(description="True if the user must contact sales to purchase.")

class CompetitorPricing(BaseModel):
    company : str
    tiers : list[PricingTier]

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0)

structured_model = model.with_structured_output(CompetitorPricing)

System_Prompt = """
You are a precise priceing data extraction agent.
Extract the pricing tiers from the user's provided text.
CRITICAL RULE : If a price is not explicitly listed as a number, you MUST set price_per_month to null. Do not guess.
"""

User_Input = """
AcmeCorp Offers a starter plan for $19 a month. Our Enterprise plan scales with you-contact our sales team for a custome quote.
"""
messages = [
    ("system", System_Prompt),
    ("human", User_Input)
]

ai_msg = structured_model.invoke(messages) 
print(ai_msg) 