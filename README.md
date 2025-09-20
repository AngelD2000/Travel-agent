# Travel Recommendation Bot

A smart travel assistant built with LangGraph and Streamlit that helps you plan your trips, check weather, find flights and hotels, and get personalized travel recommendations.

## Features

- 🌤️ **Weather Information**: Get current weather for any city
- ✈️ **Flight & Hotel Search**: Find travel deals and accommodations using SERP API
- 🗺️ **Travel Planning**: Get personalized recommendations based on your preferences
- 🏛️ **Destination Advice**: Discover new places to visit
- 💬 **Conversational Interface**: Natural chat experience with memory retention

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the `travelchatbot` directory with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
WEATHER_API_KEY=your_openweathermap_api_key_here
SERP_API_KEY=your_serpapi_key_here
```

### 3. Run the Application

#### Option 1: Web UI (Recommended)
```bash
python run_ui.py
```
This will start a Streamlit web interface at `http://localhost:8501`

#### Option 2: Command Line Interface
```bash
python langchain/main.py
```

## Usage

### Web Interface
1. Open your browser and go to `http://localhost:8501`
2. Use the quick action buttons or type your questions
3. The bot will remember your conversation history
4. Clear chat history using the sidebar button

### Command Line
1. Run the script and start chatting
2. Type your travel questions
3. Type 'q' or 'quit' to exit

## Example Questions

- "What's the weather like in Paris?"
- "Help me plan a 5-day trip to Italy"
- "Find hotels in London for next month"
- "What are the best places to visit in Japan?"
- "I have a $2000 budget for a week-long trip, where should I go?"

## Architecture

- **LangGraph**: For agent orchestration and conversation memory
- **Streamlit**: For the web interface
- **OpenAI GPT-4**: For natural language understanding
- **OpenWeatherMap API**: For weather data
- **SERP API**: For flight and hotel search

## Files

- `chat_ui.py`: Main Streamlit web interface
- `langchain/main.py`: Command-line interface
- `run_ui.py`: Simple launcher script
- `requirements.txt`: Python dependencies

## Troubleshooting

- Make sure all API keys are set in your `.env` file
- Check that you have an active internet connection
- If the UI doesn't start, try running `streamlit run chat_ui.py` directly
