from typing import Dict, List
import os
import google.generativeai as genai
import asyncio
import json
import re
from .tools import get_weather, search_web, calculate

# Configure Google Gemini
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.0-pro')
except Exception as e:
    print(f"Error configuring Gemini API: {str(e)}")
    raise

def create_agent():
    # Define available tools with their descriptions
    tools = {
        "get_weather": {
            "description": "Get the current weather for a location",
            "parameters": ["location"]
        },
        "search_web": {
            "description": "Search the web for information",
            "parameters": ["query"]
        },
        "calculate": {
            "description": "Perform mathematical calculations",
            "parameters": ["expression"]
        }
    }

    tool_map = {
        "get_weather": get_weather,
        "search_web": search_web,
        "calculate": calculate
    }

    async def process_message_stream(messages: List[Dict], message: str):
        """Handle message processing and tool calls"""
        try:
            # Simple weather pattern matching
            weather_match = re.search(r'(?:weather|temperature|temp|how\'s|how is|what\'s|what is)\s+(?:in|at|for|of)\s+([^?.,!]+)', message.lower())
            if weather_match:
                location = weather_match.group(1).strip()
                # Remove temporal words if present
                location = re.sub(r'\s+(?:now|current|currently|right now|today|tonight|this morning|this evening)\s*$', '', location, flags=re.IGNORECASE)
                
                yield {
                    "type": "tool_start",
                    "tool": "get_weather",
                    "input": {"location": location}
                }
                
                try:
                    result = get_weather(location)
                    yield {
                        "type": "llm",
                        "content": result
                    }
                except Exception as e:
                    yield {
                        "type": "llm",
                        "content": f"I apologize, but I encountered an error while getting the weather: {str(e)}"
                    }
                return  # Return to prevent Gemini from handling
                
            # Handle calculation queries - simplified pattern
            if '*' in message or '+' in message or '-' in message or '/' in message:
                # Extract just the mathematical expression
                expression = message.strip()
                if '=' in expression:
                    expression = expression.split('=')[0].strip()
                yield {
                    "type": "tool_start",
                    "tool": "calculate",
                    "input": {"expression": expression}
                }
                
                try:
                    result = calculate(expression)
                    yield {
                        "type": "llm",
                        "content": f"The calculation result is: {result}"
                    }
                    return
                except Exception as e:
                    yield {
                        "type": "llm",
                        "content": f"I apologize, but I encountered an error with the calculation: {str(e)}"
                    }
                    return

            # Use Gemini API for chat response
            try:
                response = model.generate_content(message)
                if response.text:
                    yield {
                        "type": "llm",
                        "content": response.text
                    }
                else:
                    yield {
                        "type": "llm",
                        "content": "I apologize, but I didn't receive a proper response. Please try again."
                    }
            except Exception as e:
                print(f"Error with Gemini API: {str(e)}")
                yield {
                    "type": "llm",
                    "content": "I apologize, but I encountered an error processing your request. Please try again."
                }
                    
        except Exception as e:
            print(f"Error in process_message_stream: {str(e)}")
            yield {
                "type": "llm",
                "content": f"I apologize, but I encountered an error: {str(e)}. Please try again."
            }

    class ChatWorkflow:
        def __init__(self):
            self.messages = []
            
        async def stream_run(self, message: str):
            async for event in process_message_stream(self.messages, message):
                yield event
                
    return ChatWorkflow()