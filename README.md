# SkyCast - Weather Forecast App
Author: Sivakumar

A sleek and modern weather application built with Django and OpenWeatherMap API, featuring interactive weather forecasts and data visualization.

## Features

- Current weather lookup by location (city, zip, or coordinates)
- 5-day weather forecast with detailed hourly data
- Interactive weather graphs using Chart.js
- Save and manage weather queries
- Export functionality for both current and forecast data (CSV)
- Responsive design with Tailwind CSS
- Browser geolocation support
- Delete confirmation modals for better UX
- Collapsible weather forecast sections
- GitHub profile integration in footer

## Tech Stack

- Django 4.2+
- Python 3.10+
- HTML5 + Tailwind CSS
- Chart.js for data visualization
- Vanilla JavaScript
- SQLite
- OpenWeatherMap API

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/skrindra/SkyCast.git
cd SkyCast
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
SkyCast/
├── weather/              # Main app
│   ├── models.py        # Database models
│   ├── views.py         # View logic
│   ├── forms.py         # Form definitions
│   ├── services.py      # Business logic
│   ├── templates/       # HTML templates
│   │   ├── base.html    # Base template
│   │   ├── home.html    # Home page with recent queries
│   │   ├── query_form.html    # Weather search form
│   │   ├── search_results.html # Weather results
│   │   └── query_confirm_delete.html # Delete confirmation
│   └── static/          # Static files
├── weather_project/     # Project settings
├── manage.py
└── requirements.txt
```

## Features in Detail

### Weather Search
- Search by city name, zip code, or coordinates
- Support for future dates in weather queries
- Real-time weather data from OpenWeatherMap API

### Data Visualization
- Interactive temperature graphs using Chart.js
- Collapsible forecast sections for better organization
- Visual representation of weather trends

### User Experience
- Responsive design that works on all devices
- Intuitive navigation and user interface
- Confirmation modals for important actions
- Success/error messages for user feedback

### Data Management
- Save and manage weather queries
- Export functionality for both current and forecast data
- Efficient data storage and retrieval

## Testing

Run tests with:
```bash
python manage.py test
```

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a new branch
3. Making your changes
4. Submitting a pull request

## License

MIT License

## Author

Sivakumar
- GitHub: [skrindra](https://github.com/skrindra)
