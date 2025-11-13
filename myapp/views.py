from django.shortcuts import render
from datetime import datetime
import pytz

def index(request):
    indian_cities = [
        "Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata",
        "Hyderabad", "Bhopal", "Pune", "Ahmedabad", "Indore"
    ]

    city_to_timezone = {
        "Boston": "America/New_York",
        "New York": "America/New_York",
        "London": "Europe/London",
        "Tokyo": "Asia/Tokyo",
        "Sydney": "Australia/Sydney",
        "Dubai": "Asia/Dubai",
        "Paris": "Europe/Paris",
        "UTC": "UTC"
    }

    target_cities = list(city_to_timezone.keys()) + sorted(pytz.all_timezones)

    result_time = None
    error_message = None
    selected_from = None
    selected_to = None
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")  # datetime-local format

    if request.method == "POST":
        selected_from = request.POST.get("from_city")
        selected_to = request.POST.get("to_city")
        input_time_str = request.POST.get("input_time")

        try:
            # Fix for datetime-local input
            input_time_str = input_time_str.replace("T", " ")

            india_tz = pytz.timezone("Asia/Kolkata")
            input_time = datetime.strptime(input_time_str, "%Y-%m-%d %H:%M")
            localized_time = india_tz.localize(input_time)

            if selected_to in city_to_timezone:
                target_tz_name = city_to_timezone[selected_to]
            elif selected_to in pytz.all_timezones:
                target_tz_name = selected_to
            else:
                raise ValueError("Invalid city or timezone selected.")

            target_tz = pytz.timezone(target_tz_name)
            converted_time = localized_time.astimezone(target_tz)
            result_time = f"Converted Time in {selected_to} (from {selected_from}):\n{converted_time.strftime('%Y-%m-%d %H:%M:%S')}"

        except Exception as e:
            error_message = f"Error: {e}"

    context = {
        "indian_cities": indian_cities,
        "target_cities": target_cities,
        "result_time": result_time,
        "error_message": error_message,
        "current_time": current_time,
        "selected_from": selected_from,
        "selected_to": selected_to,
    }

    return render(request, "index.html", context)
