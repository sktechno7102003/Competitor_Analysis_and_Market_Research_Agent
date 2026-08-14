# PS -> Call llm, but instead of getting chat output, output must be in JSON format

import os # isse hum python ko apne system se baat krne ka access dete hai, like directory load krne ka
from dotenv import load_dotenv # ya bina API KEy hardcode kiye usko import krta hai apne code me
from langchain_groq import ChatGroq # apna model iske andar hai
from pydantic import BaseModel, Field

load_dotenv() # .env file me jo v api key humne likha hai ye usko load kr rha hai code me

# Defining the exact structure of output we want using pydantic
class CompetitorData(BaseModel):
    company_name: str = Field(description="Name of the Competitor")
    has_free_tier : bool = Field(description = "True if they offer a free tier, else false")
    core_features : list[str] = Field(description="List of maximum 3 features mentioned")


# importing the model
model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0)
structured_model = model.with_structured_output(CompetitorData)


# sytem me hm model ko initial set of instruction dete hai before providing user input
# isme hum usko uska identity, role, behviours wagare batate hai
messages = [
    (
        "system",
        "You are a helpful Market Research Analysis Agent. Give competitor Analysis of the company the user tells you.",
    ),
    ("human", "Give me Competitor analysis of Chess.com")
]
ai_msg = structured_model.invoke(messages) # llm ko invoke krke aaye reply ko store kiya
print(ai_msg) #content ko print krne se sirf answer wala part hume dikhega