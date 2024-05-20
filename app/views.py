from django.shortcuts import render, redirect
from decouple import config, Csv
from .forms import PotatoForm
from django.http import HttpResponse
import requests
from django.conf import settings
import pandas as pd
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    SECRET_POTATO = config('SECRET_POTATO')
    print('views secret potato is: ', SECRET_POTATO)
    information = {"name":"index","secret_potato":SECRET_POTATO}
    print("information is: ",information)
    return render(request, "index.html", information)

def potato_view(request):
    if request.method == 'POST':
        form = PotatoForm(request.POST)
        if form.is_valid():
            return render(request, 'potato.html', {'form': form})
    else:
        form = PotatoForm()

    return render(request, 'potato.html', {'form': form})

def tomato_view(request):
    context = {}
    if request.method == 'POST':
        context['tomato_name'] = request.POST.get('tomato_name', '')
        context['tomato_description'] = request.POST.get('tomato_description', '')
        context['tomato_number'] = request.POST.get('tomato_number', 0)
        context['is_tomato'] = request.POST.get('is_tomato', 'off') == 'on'
    
    return render(request, 'tomato.html', context)

def weather(request):
    weather_data = None
    if 'city' in request.GET and 'country' in request.GET:
        city = request.GET.get('city')
        state = request.GET.get('state', '')
        country = request.GET.get('country')
        api_key = settings.API_KEY

        if state:
            location = f"{city},{state},{country}"
        else:
            location = f"{city},{country}"

        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'name': data.get('name'),
                'description': data['weather'][0]['description'] if data.get('weather') else 'No description',
                'temp': data['main']['temp'] if data.get('main') else 'No data',
                'feels_like': data['main']['feels_like'] if data.get('main') else 'No data',
                'humidity': data['main']['humidity'] if data.get('main') else 'No data'
            }
        else:
            weather_data = {'error': response.status_code}

    context = {
        'weather': weather_data
    }
    return render(request, 'weather.html', context)

def check_ip(request):
    ip = request.GET.get('ip', '')
    data = {}
    if ip:
        url = f'http://ip-api.com/json/{ip}'
        response = requests.get(url)
        data = response.json()
    return render(request, 'ip_check.html', {'data': data})

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        
        # Read the Excel file in memory
        df = pd.read_excel(file, engine='openpyxl')
        
        # Get the list of IP addresses from the first column
        ip_list = df.iloc[:, 0].tolist()
        
        results = []
        for ip in ip_list:
            url = f'http://ip-api.com/json/{ip}'
            response = requests.get(url)
            data = response.json()
            results.append(data)
        
        return render(request, 'upload_results.html', {'results': results})
    
    return render(request, 'upload.html')