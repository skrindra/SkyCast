# Weather App
Author: Sivakumar

A full-featured weather application built with Django and OpenWeatherMap API.

## Features

- Current weather lookup by location (city, zip, or coordinates)
- 5-day weather forecast
- CRUD operations for weather queries
- Export functionality (CSV)
- Responsive design with Tailwind CSS
- Browser geolocation support

## Tech Stack

- Django 4.2+
- Python 3.10+
- HTML5 + Tailwind CSS
- Vanilla JavaScript
- SQLite
- OpenWeatherMap API

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd weather-app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your OpenWeatherMap API key:
```
OPENWEATHER_API_KEY=your_api_key_here
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Visit http://localhost:8000 in your browser

## Environment Variables

Create a `.env` file with the following variables:
- `OPENWEATHER_API_KEY`: Your OpenWeatherMap API key
- `DEBUG`: Set to True for development, False for production
- `SECRET_KEY`: Django secret key

## Project Structure

```
weather_project/
├── weather/              # Main app
│   ├── models.py        # Database models
│   ├── views.py         # View logic
│   ├── forms.py         # Form definitions
│   ├── services.py      # Business logic
│   ├── templates/       # HTML templates
│   └── static/          # Static files
├── weather_project/     # Project settings
├── manage.py
└── requirements.txt
```

## Testing

Run tests with:
```bash
python manage.py test
```

## License

MIT License
