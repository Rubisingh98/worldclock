from django.shortcuts import render
from datetime import datetime
import pytz

def index(request):
   
    indian_city_to_timezone = {
        "Delhi": "Asia/Kolkata",
        "Mumbai": "Asia/Kolkata",
        "Bangalore": "Asia/Kolkata",
        "Chennai": "Asia/Kolkata",
        "Kolkata": "Asia/Kolkata",
        "Hyderabad": "Asia/Kolkata",
        "Bhopal": "Asia/Kolkata",
        "Pune": "Asia/Kolkata",
        "Ahmedabad": "Asia/Kolkata",
        "Indore": "Asia/Kolkata"
    }

    
    boston_related_cities = {
        "Boston": "America/New_York",
        "Cambridge": "America/New_York",
        "Quincy": "America/New_York",
        "Worcester": "America/New_York",
        "Lowell": "America/New_York",
        "Springfield (MA)": "America/New_York",
        "Newton": "America/New_York",
        "Salem (MA)": "America/New_York",
        "Brockton": "America/New_York",
        "Somerville": "America/New_York"
    }
    all_world_timezones = set(pytz.all_timezones)
    for city_tz in boston_related_cities.values():
        all_world_timezones.add(city_tz)

    converted_time = ""
    error = ""

    if request.method == "POST":
        try:
           
            source_city = request.POST.get("indian_city")
            target_city = request.POST.get("target_city")
            input_time_str = request.POST.get("time_input")

            
            input_time = datetime.strptime(input_time_str, "%Y-%m-%d %H:%M")

            source_tz_name = indian_city_to_timezone.get(source_city, "Asia/Kolkata")

           
            if target_city in boston_related_cities:
                target_tz_name = boston_related_cities[target_city]
            elif target_city in pytz.all_timezones:
                target_tz_name = target_city
            else:
                error = "Invalid city or timezone selected."
                target_tz_name = None

            if target_tz_name:
                source_tz = pytz.timezone(source_tz_name)
                target_tz = pytz.timezone(target_tz_name)

                localized_time = source_tz.localize(input_time)
                converted = localized_time.astimezone(target_tz)

                converted_time = converted.strftime("%Y-%m-%d %H:%M:%S")

        except Exception as e:
            error = f"Error: {e}"

 
    world_timezones_list = list(boston_related_cities.keys()) + sorted(pytz.all_timezones)

    context = {
        "indian_cities": list(indian_city_to_timezone.keys()),
        "world_timezones": world_timezones_list,
        "converted_time": converted_time,
        "error": error,
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    return render(request, "index.html", context)
