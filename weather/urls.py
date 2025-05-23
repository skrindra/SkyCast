from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.WeatherHomeView.as_view(), name='home'),
    path('search/', views.WeatherSearchView.as_view(), name='search'),
    path('query/new/', views.WeatherQueryCreateView.as_view(), name='query_create'),
    path('query/<int:pk>/update/', views.WeatherQueryUpdateView.as_view(), name='query_update'),
    path('query/<int:pk>/delete/', views.WeatherQueryDeleteView.as_view(), name='query_delete'),
    path('query/<int:pk>/export/', views.export_weather_data, name='export_weather_data'),
    path('api/query/<int:pk>/', views.get_query_data, name='query_data'),  # API endpoint for query data
] 