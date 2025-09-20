import streamlit as st
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AIMessage
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the page
st.set_page_config(
    page_title="Travel Assistant Bot",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .feature-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .user-message {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .assistant-message {
        background: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "travel_conversation"

# Initialize the agent
@st.cache_resource
def initialize_agent():
    """Initialize the travel agent with caching"""
    # Set environment variable if not already set
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = openai_key
    
    model = init_chat_model("gpt-4o-mini", temperature=0)
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
        
        if weather_api_key is None:
            return "Error: Weather API key is not set"
        
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": weather_api_key,
            "units": "metric"
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}"

    def get_flight_and_hotel_information(query: str) -> str:
        """Get serp api"""
        serp_api_key = os.getenv("SERP_API_KEY")
        
        if serp_api_key is None:
            return "Error: SERP API key is not set"
        
        base_url = "https://serpapi.com/search"
        search_params = {
            "engine": "google",
            "google_domain": "google.com",
            "hl": "en",
            "gl": "us",
            "q": query,
            "api_key": serp_api_key
        }
        
        response = requests.get(base_url, params=search_params)
        
        if response.status_code == 200:
            return response.content
        else:
            return f"Error, response: {response}"
    
    agent = create_react_agent(
        model=model,
        tools=[get_weather, get_flight_and_hotel_information],
        prompt=system_prompt,
        checkpointer=memory
    )
    
    return agent

def get_final_ai_message(result):
    """Extract the final AI message from the result"""
    final_ai = next(
        m for m in reversed(result["messages"])
        if isinstance(m, AIMessage) and m.content.strip()
    )
    return final_ai.content

def get_agent_response(user_input, thread_id):
    """Get response from the travel agent"""
    try:
        response = st.session_state.agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]}, 
            config={"configurable": {"thread_id": thread_id}}
        )
        return get_final_ai_message(response)
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Main UI
def main():
    # Header with custom styling
    st.markdown("""
    <div class="main-header">
        <h1>✈️ Travel Assistant Bot</h1>
        <p>Your personal travel planning companion! Ask me about destinations, weather, flights, hotels, and more.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🤖 Bot Features")
        
        st.markdown("""
        <div class="feature-card">
            <strong>🌤️ Weather Information</strong><br>
            Get current weather for any city
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <strong>✈️ Flight & Hotel Search</strong><br>
            Find travel deals and accommodations
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <strong>🗺️ Travel Planning</strong><br>
            Get personalized recommendations
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <strong>🏛️ Destination Advice</strong><br>
            Discover new places to visit
        </div>
        """, unsafe_allow_html=True)
        
        st.header("💡 Tips")
        st.markdown("""
        - Be specific about your travel preferences
        - Mention your budget and group size
        - Ask about activities you enjoy
        - Request weather information for your destination
        """)
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Chat History", key="clear_chat"):
            st.session_state.messages = []
            st.rerun()
        
        # Show conversation stats
        if st.session_state.messages:
            st.markdown(f"**Messages in conversation:** {len(st.session_state.messages)}")
    
    # Initialize agent
    if st.session_state.agent is None:
        with st.spinner("Initializing travel agent..."):
            st.session_state.agent = initialize_agent()
    
    # Quick action buttons
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🌤️ Check Weather", key="weather_btn"):
            st.session_state.messages.append({"role": "user", "content": "What's the weather like in Paris?"})
            st.rerun()
    
    with col2:
        if st.button("✈️ Find Flights", key="flights_btn"):
            st.session_state.messages.append({"role": "user", "content": "Help me find flights from New York to Tokyo"})
            st.rerun()
    
    with col3:
        if st.button("🏨 Search Hotels", key="hotels_btn"):
            st.session_state.messages.append({"role": "user", "content": "Find hotels in London for next month"})
            st.rerun()
    
    with col4:
        if st.button("🗺️ Plan Trip", key="plan_btn"):
            st.session_state.messages.append({"role": "user", "content": "Help me plan a 5-day trip to Italy"})
            st.rerun()
    
    st.markdown("---")
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me about your travel plans..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking about your travel needs..."):
                    response = get_agent_response(prompt, st.session_state.thread_id)
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit and LangGraph")

if __name__ == "__main__":
    main()
