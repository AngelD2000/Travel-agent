import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
from langchain_core.tools import tool
import json

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

client = OpenAI()

travel_agent_prompt = """You're a helpful travel assistant that can answer questions about travel destinations and provide information about the best places to visit.
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


def get_travel_agent_response(user_input, conversation_history):

    conversation_history.append({
        "role": "user",
        "content": user_input
    })
    
    # First API call to get LLM response (potentially with tool calls)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history,
        tools=get_tools()
    )

    message = response.choices[0].message
    
    # Add the assistant's message to conversation history
    conversation_history.append({
        "role": "assistant",
        "content": message.content,
        "tool_calls": message.tool_calls
    })

    # Check if the LLM wants to call tools
    if message.tool_calls:
        print("Assistant is calling tools...")
        
        # Add tool results to conversation
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"Calling {function_name} with args: {function_args}")
            
            # Execute the appropriate tool
            if function_name == "get_weather":
                tool_result = get_weather.invoke(function_args)
            elif function_name == "get_flight_and_hotel_information":
                tool_result = get_flight_and_hotel_information.invoke(function_args)
            else:
                tool_result = f"Unknown function: {function_name}"
            
            print(f"Tool result: {tool_result}")
            
            # Add tool result to conversation
            conversation_history.append({
                "role": "tool",
                "content": str(tool_result),
                "tool_call_id": tool_call.id
            })
        
        # Make a second API call with the tool results
        second_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            tools=get_tools()
        )
        
        final_message = second_response.choices[0].message.content
        conversation_history.append({
            "role": "assistant",
            "content": final_message
        })
        
        print("Assistant: ", final_message)
    else:
        # No tool calls, just regular response
        print("Assistant: ", message.content)

    return conversation_history

def get_tools():
    tools = [
            {
            "type": "function",
            "function":{
                "name": "get_weather",
                "description": "Get the weather of a city",
                    "parameters":{
                        "type": "object",
                        "properties": {
                            "city":{
                                "type": "string",
                                "description": "The city to get the weather of"
                            }
                        },
                        "required": ["city"]

                    }
                }
            },
            {
            "type": "function",
            "function":{
                "name": "get_flight_and_hotel_information",
                "description": "Google search api to get flight and hotel information",
                    "parameters":{
                        "type": "object",
                        "properties": {
                            "query":{
                                "type": "string",
                                "description": "Search query for google"
                            }
                        },
                        "required": ["query"]

                    }
                }
            }
        ]
    
    return tools

@tool
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

@tool
def get_flight_and_hotel_information(query: str) -> str:

    """Get serp api"""
    serp_api_key = os.getenv("SERP_API_KEY")

    if(serp_api_key is None):
        return "Error: SERP API key is not set"
    else:
        print("SERP API key: ", serp_api_key)
    
    base_url = "https://serpapi.com/search"

    search_params = {
        "engine":"google",
        "google_domain":"google.com",
        "hl":"en",
        "gl":"us",
        "q": query,
        "api_key": serp_api_key
    }

    response = requests.get(base_url, params=search_params)

    if(response.status_code == 200):
        return response.content
    else:
        return f"Error, response: {response}"
    

def main():
    conversation_history = [
        {
            "role":"system",
            "content": travel_agent_prompt
        }
    ]
    print("You've entered the travel bot experience! :) Ask away!")
    while True:
        user_input = input("User: ")
        if(user_input == "q" or user_input=="quit" ):
            break 
        conversation_history = get_travel_agent_response(user_input, conversation_history)


if __name__ == "__main__":
    main()

"""
#TODO: 
* Try Langgraph 
* Add a UI 
"""