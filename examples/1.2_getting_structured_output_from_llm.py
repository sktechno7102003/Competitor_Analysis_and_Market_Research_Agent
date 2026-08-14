# PS -> 

import os # isse hum python ko apne system se baat krne ka access dete hai, like directory load krne ka
from dotenv import load_dotenv # ya bina API KEy hardcode kiye usko import krta hai apne code me
from langchain_groq import ChatGroq # apna model iske andar hai

load_dotenv() # .env file me jo v api key humne likha hai ye usko load kr rha hai code. me

# importing the model
model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0)

# sytem me hm model ko initial set of instruction dete hai before providing user input
# isme hum usko uska identity, role, behviours wagare batate hai
messages = [
    (
        "system",
        "You are a helpful Market Research Analysis Agent. Give competitor Analysis of the company the user tells you.",
    ),
    ("human", "Give me Competitor analysis of Microsoft"), # isme hum actual user input de rhe hai
]
ai_msg = model.invoke(messages) # llm ko invoke krke aaye reply ko store kiya
print(ai_msg.content) # .content ko print krne se sirf answer wala part hume dikhega