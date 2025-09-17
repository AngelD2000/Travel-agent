from email import message
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AIMessage
import os


load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

model = init_chat_model(
    "gpt-4o-mini",
    temperature=0
)

def get_final_ai_message(result):
    final_ai = next(
        m for m in reversed(result["messages"])
        if isinstance(m, AIMessage) and m.content.strip()
    )

    return final_ai.content

system_prompt = """ You're a helpful travel assistant that handles 
                the resarch and provides the best experience. 
                Don't halucinate, if you don't know say you don't know
                """

def get_weather(city: str) -> str:  
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"
    

agent = create_react_agent(
    model=model,  
    tools=[get_weather],  
    prompt=system_prompt,
)

# Run the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)


print(get_final_ai_message(result))