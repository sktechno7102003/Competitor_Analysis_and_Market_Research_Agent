# PS -> given an input, you Ai agent has to act as feature and sentiment extractor, giving following thing as outpu
# 1. company name, company founding year, list of their distinct product features, target audience(B2B, B2C,both),
# array of identifies weaknesses (inferred from what they don't offer or what they restrict)

import os 
from dotenv import load_dotenv 
from langchain_groq import ChatGroq 
from pydantic import BaseModel, Field
from enum import Enum

load_dotenv() 

User_Prompt = """
Welcome to DataFlow AI, founded in 2021! We are revolutionizing how businesses handle their data pipelines. 
Our platform offers real-time data streaming, one-click AWS integration, 
and an automated data cleaning dashboard. We focus exclusively on enterprise teams and large corporations. 
Pricing starts at our Free Tier, though please note the free tier is severely capped at 100MB of data processing per month and 
does not include customer support. For unlimited processing, upgrade to Pro!"""

System_Prompt = """
You are a feature and Sentiment extractor.
You will extract feautres from the company details that user will give.
STRICTLY : If any detail is not given in the user input then dont assume it, output null in that case.
"""

class TargetAudience(str, Enum):
    B2B = "business to business"
    B2C = "business to customer"
    BOTH = "Both business to customer and Business to business"

class OutputStructure(BaseModel):
    company_name : str = Field(description="Name of the company")
    founding_year : int = Field(description="Founding year of the company")
    product_features : list[str] = Field(description="What different product features do the company have")
    weaknesses : list[str] = Field(description="What company don't offer or restricts")


model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0)

structured_model = model.with_structured_output(OutputStructure)

messages = [
    ("system", System_Prompt),
    ("human", User_Prompt)
]

ai_msg = structured_model.invoke(messages) 

print(ai_msg.model_dump_json(indent=2))

# Output
# {
#   "company_name": "DataFlow AI",
#   "founding_year": 2021,
#   "product_features": [
#     "real-time data streaming",
#     "one-click AWS integration",
#     "automated data cleaning dashboard"
#   ],
#   "weaknesses": [
#     "Free Tier is severely capped at 100MB of data processing per month",
#     "Free Tier does not include customer support"
#   ]
# }