from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
import csv
from datetime import datetime, date
from io import StringIO
import requests
import json
from django.conf import settings

from .models import WeatherQuery
from .forms import WeatherQueryForm, WeatherSearchForm
from .services import WeatherService

class WeatherHomeView(ListView):
    model = WeatherQuery
    template_name = 'weather/home.html'
    context_object_name = 'queries'
    ordering = ['-created_at']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = WeatherSearchForm()
        return context

class WeatherSearchView(ListView):
    template_name = 'weather/search_results.html'
    context_object_name = 'weather_data'
    
    def get(self, request, *args, **kwargs):
        form = WeatherSearchForm(request.GET)
        if form.is_valid():
            location = form.cleaned_data['location']
            weather_service = WeatherService()
            
            try:
                current_weather = weather_service.get_current_weather(location)
                forecast = weather_service.get_forecast(location)
                
                formatted_weather = weather_service.format_weather_data(current_weather)
                if not formatted_weather:
                    messages.error(request, "Unable to format weather data")
                    return redirect('weather:home')
                
                context = {
                    'current_weather': formatted_weather,
                    'forecast': forecast,
                    'location': location,
                    'search_form': form,
                    'queries': WeatherQuery.objects.all().order_by('-created_at')[:5]
                }
                return render(request, self.template_name, context)
            except ValueError as e:
                messages.error(request, "Invalid API key configuration. Please check your settings.")
                return redirect('weather:home')
            except Exception as e:
                messages.error(request, str(e))
                return redirect('weather:home')
                
        messages.error(request, "Please enter a valid location")
        return redirect('weather:home')

class WeatherQueryCreateView(CreateView):
    model = WeatherQuery
    form_class = WeatherQueryForm
    template_name = 'weather/query_form.html'
    success_url = reverse_lazy('weather:home')
    
    def form_valid(self, form):
        try:
            weather_service = WeatherService()
            location = form.cleaned_data['location']
            
            # Get weather data
            current_weather = weather_service.get_current_weather(location)
            forecast = weather_service.get_forecast(location)
            
            # Store the response data
            form.instance.response_data = {
                'current': current_weather,
                'forecast': forecast
            }
            
            # Save the form
            self.object = form.save()
            
            # Add success message
            messages.success(
                self.request,
                f'Weather query for {location} saved successfully! You can now view it in Recent Queries.',
                extra_tags='success'
            )
            
            # Force message to be displayed
            self.request.session.modified = True
            
            # Return redirect response
            return redirect('weather:home')
        except Exception as e:
            print(f"Error saving query: {str(e)}")  # Debug logging
            messages.error(
                self.request,
                f"Error saving query: {str(e)}. Please try again.",
                extra_tags='error'
            )
            # Force error message to be displayed
            self.request.session.modified = True
            return self.form_invalid(form)
            
    def form_invalid(self, form):
        print("Form validation failed")  # Debug logging
        for field, errors in form.errors.items():
            print(f"Field {field} errors: {errors}")  # Debug logging
        return super().form_invalid(form)
            
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Set default dates
        today = date.today()
        form.fields['start_date'].initial = today
        form.fields['end_date'].initial = today
        return form
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Weather Query'
        return context

class WeatherQueryUpdateView(UpdateView):
    model = WeatherQuery
    form_class = WeatherQueryForm
    template_name = 'weather/query_form.html'
    success_url = reverse_lazy('weather:home')
    
    def form_valid(self, form):
        try:
            weather_service = WeatherService()
            location = form.cleaned_data['location']
            
            # Update weather data
            current_weather = weather_service.get_current_weather(location)
            forecast = weather_service.get_forecast(location)
            
            form.instance.response_data = {
                'current': current_weather,
                'forecast': forecast
            }
            
            messages.success(self.request, f'Weather query for {location} updated successfully!')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

class WeatherQueryDeleteView(DeleteView):
    model = WeatherQuery
    success_url = reverse_lazy('weather:home')
    template_name = 'weather/query_confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        location = self.object.location
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(
            self.request,
            f'Weather query for {location} has been deleted.',
            extra_tags='success'
        )
        return redirect(success_url)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Weather Query'
        return context

def export_weather_data(request, pk):
    try:
        query = get_object_or_404(WeatherQuery, pk=pk)
        response_data = query.response_data
        
        # Create CSV content
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Location', 'Date', 'Time', 'Temperature (°C)', 'Description', 'Humidity (%)', 'Wind Speed (m/s)', 'Data Type'])
        
        # Write current weather data
        if 'current' in response_data:
            current = response_data['current']
            writer.writerow([
                query.location,
                datetime.fromtimestamp(current['dt']).strftime('%Y-%m-%d'),
                datetime.fromtimestamp(current['dt']).strftime('%H:%M:%S'),
                current['main']['temp'],
                current['weather'][0]['description'],
                current['main']['humidity'],
                current['wind']['speed'],
                'Current'
            ])
        
        # Write forecast data
        if 'forecast' in response_data:
            for item in response_data['forecast']['list']:
                writer.writerow([
                    query.location,
                    datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d'),
                    datetime.fromtimestamp(item['dt']).strftime('%H:%M:%S'),
                    item['main']['temp'],
                    item['weather'][0]['description'],
                    item['main']['humidity'],
                    item['wind']['speed'],
                    'Forecast'
                ])
        
        # Create the response
        output.seek(0)
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="weather_data_{query.location}_{date.today()}.csv"'
        
        messages.success(
            request,
            f'Weather data for {query.location} has been exported successfully.',
            extra_tags='success'
        )
        
        return response
        
    except Exception as e:
        messages.error(
            request,
            f"Error exporting data: {str(e)}. Please try again.",
            extra_tags='error'
        )
        return redirect('weather:home')

def get_query_data(request, pk):
    """API endpoint to get weather query data"""
    try:
        query = get_object_or_404(WeatherQuery, pk=pk)
        if not query.response_data:
            print(f"No response data found for query {pk}")  # Debug log
            return JsonResponse({'error': 'No weather data available'}, status=404)
        
        # Ensure response_data is properly formatted
        if not isinstance(query.response_data, dict):
            print(f"Invalid response data format for query {pk}: {type(query.response_data)}")  # Debug log
            return JsonResponse({'error': 'Invalid data format'}, status=500)
            
        # Check if required data is present
        if 'forecast' not in query.response_data or 'list' not in query.response_data['forecast']:
            print(f"Missing forecast data for query {pk}")  # Debug log
            return JsonResponse({'error': 'Missing forecast data'}, status=500)
            
        return JsonResponse(query.response_data)
    except WeatherQuery.DoesNotExist:
        print(f"Query {pk} not found")  # Debug log
        return JsonResponse({'error': 'Query not found'}, status=404)
    except Exception as e:
        print(f"Error processing query {pk}: {str(e)}")  # Debug log
        return JsonResponse({'error': str(e)}, status=500)
