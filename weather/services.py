import requests
from django.conf import settings
from datetime import datetime, timedelta
from decouple import config

class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self):
        self.api_key = config('OPENWEATHER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key is not configured")
        
    def get_current_weather(self, location):
        """Get current weather for a location."""
        params = {
            'q': location,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(f"{self.BASE_URL}/weather", params=params)
            data = response.json()
            
            if response.status_code != 200:
                error_message = data.get('message', 'Unknown error')
                raise Exception(f"API Error: {error_message}")
                
            return data
        except requests.RequestException as e:
            raise Exception(f"Network Error: {str(e)}")
        except ValueError as e:
            raise Exception(f"Invalid Response: {str(e)}")
            
    def get_forecast(self, location, days=5):
        """Get 5-day weather forecast for a location."""
        params = {
            'q': location,
            'appid': self.api_key,
            'units': 'metric',
            'cnt': days * 8  # API returns data in 3-hour intervals
        }
        
        try:
            response = requests.get(f"{self.BASE_URL}/forecast", params=params)
            data = response.json()
            
            if response.status_code != 200:
                error_message = data.get('message', 'Unknown error')
                raise Exception(f"API Error: {error_message}")
                
            return data
        except requests.RequestException as e:
            raise Exception(f"Network Error: {str(e)}")
        except ValueError as e:
            raise Exception(f"Invalid Response: {str(e)}")
            
    def get_historical_weather(self, location, start_date, end_date):
        """Get historical weather data for a location and date range."""
        # Note: This is a placeholder. OpenWeatherMap's historical data
        # requires a paid subscription. You might want to use a different
        # API or implement a different solution for historical data.
        raise NotImplementedError("Historical weather data requires a paid API subscription")
        
    @staticmethod
    def format_weather_data(data):
        """Format weather data for display."""
        if not data or 'main' not in data:
            return None
            
        try:
            return {
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'city': data['name'],
                'country': data['sys']['country']
            }
        except (KeyError, TypeError) as e:
            raise Exception(f"Invalid weather data format: {str(e)}") 