# PS -> Limit the token input so that llm ka token limit hit na ho, cost and latency bache
# Show it in the code by passing a text of 1000 tokens but limit 500 tokens to check error

import os 
from dotenv import load_dotenv 
from langchain_groq import ChatGroq 
import tiktoken # ye standard library for couting tokens but for OpenAI so we will use langchain .get_num_tokens to count

load_dotenv()

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0)

user_input = "i am the boss"*10000;
num_tokens = model.get_num_tokens(user_input)

# Safety protocol for token limit
if num_tokens>5000:
    print("Warning : Input too long, Will have to truncate for cost/safety")