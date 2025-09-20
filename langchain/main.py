from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AIMessage
import os
import requests


load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

model = init_chat_model(
    "gpt-4o-mini",
    temperature=0
)

memory = InMemorySaver()

system_prompt = """You're a helpful travel assistant that can answer questions about travel destinations and provide information about the best places to visit.
                The goal is to help the user plan their trip by providing a list of destinations, activities, hotels, restaurants, and things to do.


                Information you should seek to get; total budget, number of people, duration of trip, and any other relevant information.
                Then you should ask about the weather, where they want to go, what they like to do, and how much intense they want their trip to be.
                Intensity like, chill trip or trip with full itenary.

                If you're not given any information, ask the user for the information you need.

                Make sure to be consistent in your responses.

                If the user doesn't know asks for recommendations for locations start by asking about 
                specific continent, country, or city.
                And if they are open for international travel 

                You're helpful, intelligent, and systematic travel planner agent. 

                Rules to follow:
                - Do **not** fabricate information.
                - If you don't know the answer, say you don't know.
                - If you are unsure about the information, ask the user to provide more information.

                Be cheerful and bubbly.
                """


def get_weather(city: str) -> str:


    """Get the weather of a city"""
    weather_api_key = os.getenv("WEATHER_API_KEY")

    if(weather_api_key is None):
        return "Error: Weather API key is not set"
    else:
        print("Weather API key: ", "***")

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": weather_api_key,
        "units": "metric"
    }
    
    response = requests.get(base_url, params=params)
    
    if(response.status_code == 200):
        return response.json()
    else:
        return f"Error: {response.status_code}"

agent = create_react_agent(
    model=model,  
    tools=[get_weather],  
    prompt=system_prompt,
    checkpointer=memory
)

def get_travel_agent(user_input, thread_id):
   
    response = agent.invoke({"messages": [{"role": "user", "content": user_input}]}, config={"configurable": {"thread_id": thread_id}})

    print(f"Bot: {get_final_ai_message(response)} ")


    
def get_final_ai_message(result):
    final_ai = next(
        m for m in reversed(result["messages"])
        if isinstance(m, AIMessage) and m.content.strip()
    )

    return final_ai.content


def main():
    while True: 
        user_input = input("User: ")
        if(user_input == 'q' or user_input == 'quit'): 
            break
        get_travel_agent(user_input, "default")

if __name__ == "__main__":
    main()