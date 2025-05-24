# SkyCast - Weather Application

SkyCast is a Django-based web application that provides real-time weather information and forecasts using the OpenWeatherMap API. The application features a modern, responsive design and allows users to search for weather conditions, view forecasts, and save their queries.

## Features

- 🌤️ Real-time weather information
- 📅 5-day weather forecast
- 📊 Interactive weather graphs using Chart.js
- 💾 Save and view weather queries
- 📱 Responsive design for all devices
- 📤 Export weather data to CSV
- 🔍 Search by city name
- 📈 Historical query tracking

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or higher
- Git
- pip (Python package installer)
- Virtual environment tool (venv)
- OpenWeatherMap API Key (Get one [here](https://openweathermap.org/api))

## Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/skrindra/SkyCast.git
   cd SkyCast
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root with:
   ```env
   SECRET_KEY=your_django_secret_key
   OPENWEATHER_API_KEY=your_openweathermap_api_key
   DEBUG=True
   ```

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   The application will be available at `http://127.0.0.1:8000/weather/`

## Project Structure

```
SkyCast/
├── manage.py
├── weather_project/         # Django project settings
│   ├── settings.py         # Project settings and configurations
│   ├── urls.py            # Main URL routing
│   ├── wsgi.py           # WSGI configuration
│   └── asgi.py           # ASGI configuration
├── weather/               # Main application
│   ├── migrations/       # Database migrations
│   ├── static/          # Static files (CSS, JS, images)
│   ├── templates/       # HTML templates
│   ├── models.py        # Database models
│   ├── views.py         # View logic
│   ├── urls.py          # App URL routing
│   └── services.py      # Weather API service
├── staticfiles/         # Collected static files
├── templates/           # Project-level templates
├── requirements.txt     # Project dependencies
└── .env                # Environment variables
```

## Dependencies

Key dependencies include:
- Django 4.2.7
- requests 2.31.0
- python-dotenv 1.0.0
- gunicorn 21.2.0
- psycopg2-binary 2.9.9
- dj-database-url 2.1.0

## Deployment

The project is configured for deployment on Render. The following files are included for deployment:

- `render.yaml`: Infrastructure as Code configuration # for CLI based deployment
- `build.sh`: Custom build script

### Deployment Steps

1. Push your code to GitHub
2. Connect your repository to Render
3. Create a new Web Service
4. Configure environment variables in Render dashboard:
   - `SECRET_KEY`
   - `OPENWEATHER_API_KEY`
   - `DEBUG=False`
   - `DATABASE_URL` (automatically set if using Render PostgreSQL - Internal DB URL)

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

---

Made with ❤️ by Sivakumar
