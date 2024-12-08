import random
import math

def get_weather(location: str) -> str:
    """Get real weather information from OpenWeatherMap API"""
    import os
    import requests
    
    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
    if not api_key:
        return "Error: OpenWeatherMap API key not found. Please set up the API key."
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    try:
        # Make API request with metric units
        response = requests.get(
            base_url,
            params={
                'q': location,
                'appid': api_key,
                'units': 'metric'  # Use metric units (Celsius)
            },
            timeout=10
        )
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        # Parse the response
        data = response.json()
        
        # Extract relevant information
        temp = data['main']['temp']
        conditions = data['weather'][0]['description']
        humidity = data['main']['humidity']
        
        return f"Current weather in {location}:\nTemperature: {temp:.1f}°C\nConditions: {conditions}\nHumidity: {humidity}%"
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"
    except (KeyError, IndexError) as e:
        return f"Error parsing weather data: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def search_web(query: str) -> str:
    """Simulate web search"""
    # This is a mock implementation
    return f"Found simulated search results for: {query}"

def calculate(expression: str) -> str:
    """Perform basic calculations safely"""
    try:
        # Clean the expression - keep only numbers and basic operators
        cleaned_expr = ''.join(c for c in expression if c.isdigit() or c in '+-*/.() ')
        cleaned_expr = cleaned_expr.strip()
        
        # Handle empty or invalid expressions
        if not cleaned_expr:
            return "Please provide a valid mathematical expression"
            
        # Evaluate the expression safely without any additional functions
        result = eval(cleaned_expr, {"__builtins__": None}, {})
        
        # Format the result
        if isinstance(result, float):
            # Remove trailing zeros after decimal point
            return f"{result:.10f}".rstrip('0').rstrip('.')
        return str(result)
        
    except Exception as e:
        return f"Could not calculate: {cleaned_expr}. Please provide a valid mathematical expression."
