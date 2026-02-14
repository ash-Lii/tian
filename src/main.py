import dotenv; dotenv.load_dotenv()
import os
from langchain_openai import ChatOpenAI
from system_prompt import create_system_prompt
from langchain.agents import create_agent
from tools import my_tools


llm_model = ChatOpenAI(model=os.getenv('LLM_MODEL'), temperature=0)
toolbox = my_tools(['database'])
prompt = create_system_prompt()

agent = create_agent(
    llm_model,
    toolbox,
    system_prompt=prompt,
)

query = ('''
武汉大学有几个麦当劳

''')


for event in agent.stream(
    {"messages": [{"role": "user", "content": query}]},
    stream_mode="values",
):
    event["messages"][-1].pretty_print()