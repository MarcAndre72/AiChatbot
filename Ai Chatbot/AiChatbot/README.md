# AI Assistant with Tool Calling

A functional AI chatbot that demonstrates real-world tool integration capabilities. The system combines a Streamlit frontend for user interaction with a FastAPI backend, featuring real-time streaming responses and practical tool-calling functionality.

## Features

- 🤖 Powered by Google's Gemini AI model for natural language understanding
- 💬 Real-time streaming chat interface with instant responses
- 🛠️ Integrated tools:
  - Mathematical calculator with support for basic operations
  - Real-time weather information via OpenWeatherMap API
  - Contextual understanding for natural queries
- 📱 Clean, responsive Streamlit interface with chat history
- ⚡ High-performance FastAPI backend with streaming support

## Tech Stack

- **Frontend**: Streamlit
  - SSE-based real-time message streaming
  - Dedicated tool call visualization sidebar
  - Persistent chat history management
  - Error handling and recovery

- **Backend**: FastAPI
  - Asynchronous API endpoints with streaming
  - Server-Sent Events (SSE) implementation
  - CORS middleware for secure communication
  - Robust error handling

- **AI Model**: Google Gemini
  - Advanced natural language understanding
  - Pattern recognition for tool selection
  - Context-aware conversation handling
  - Streaming response generation

- **Tools Integration**:
  - OpenWeatherMap API for real-time weather data
  - Safe mathematical expression evaluator
  - Extensible tool integration framework

## Important note before setting in "other" environnement:
The code is already set up to read from Replit's Secrets system using os.environ.get(). That's why you don't need a .env file. The environment variables are automatically loaded from Replit's Secrets.

After setting up both secrets correctly:

Run the backend: python -m backend.main
In a second terminal: streamlit run frontend/app.py --server.port 5000

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   # Create a .env file with the following:
   GOOGLE_API_KEY=your_gemini_api_key
   OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
   ```

4. Start the backend server:
   ```bash
   python -m backend.main
   ```

5. Launch the Streamlit frontend:
   ```bash
   streamlit run frontend/app.py
   ```

6. Open your browser and navigate to `http://localhost:5000`

Note: You'll need to obtain API keys from:
- [Google AI Studio](https://makersuite.google.com/app/apikey) for Gemini
- [OpenWeatherMap](https://openweathermap.org/api) for weather data

## Project Structure

```
.
├── frontend/
│   └── app.py           # Streamlit interface with SSE streaming
├── backend/
│   ├── main.py         # FastAPI server with streaming endpoints
│   ├── agent.py        # AI agent with tool routing logic
│   └── tools.py        # Tool implementations (Weather, Calculator)
└── .streamlit/
    └── config.toml     # Streamlit server configuration
```

## Features in Detail

### Chat Interface
- Real-time message streaming using Server-Sent Events
- Persistent chat history with session management
- Dedicated sidebar for tool execution visualization
- Responsive design with error handling

### Tool Integration
- **Calculator**:
  - Supports basic arithmetic operations (+, -, *, /)
  - Safe expression evaluation
  - Natural language query understanding (e.g., "What is 3*3?")

- **Weather Service**:
  - Real-time weather data via OpenWeatherMap API
  - Temperature, conditions, and humidity information
  - Natural language query support (e.g., "How's the weather in Montreal?")
  - Global location support with error handling

### AI Capabilities
- Pattern recognition for tool selection
- Natural language understanding for query parsing
- Context-aware conversation handling
- Robust error handling and recovery
- Streaming responses for real-time interaction

## Environment Variables

Required environment variables:
- `GOOGLE_API_KEY`: Google Gemini API key for AI model access

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details
