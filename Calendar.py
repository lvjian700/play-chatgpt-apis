from Google import Create_Service

CLIENT_SECRET_FILE = "data/client_secret_calendar.json"
APP_NAME = "calendar"
APP_VERSION = "v3"
SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

service = Create_Service(CLIENT_SECRET_FILE, APP_NAME, APP_VERSION, SCOPES)
calendar_id = "lvjian700@gmail.com"
current_calendar = service.calendars().get(calendarId=calendar_id).execute()
current_timezone = current_calendar['timeZone']

print(f"Calendar: {calendar_id}");
print(f"Timezone: {current_timezone}");

from datetime import datetime, timedelta
import pytz

def tz_now():
    return pytz.timezone(current_timezone).localize(datetime.now())

def get_time_range(period):
    now = tz_now()
    if period == 'today':
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        return start_of_day, end_of_day
    elif period == 'week':
        start_of_week = now - timedelta(days=now.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday
        return start_of_week, end_of_week
    else:
        raise ValueError(f"Period must be 'today' or 'week', but got {period}")

# Consider timezone
def time_to_iso_str(date_time):
    return date_time.isoformat()

# def time_to_datetime(time_of_today):
#     # Get the current date
#     now = pytz.timezone(current_timezone).localize(datetime.now())
#     combined_str = f"{now.strftime('%Y-%m-%d')} {time_of_today}"
#     return pytz.timezone(current_timezone).localize(datetime.strptime(combined_str, "%Y-%m-%d %H:%M"))

def get_events(period):
    # Set time range based on the period
    range = get_time_range(period)
    time_min = time_to_iso_str(range[0])
    time_max = time_to_iso_str(range[1])

    # Fetch the events
    events_result = service.events().list(calendarId=calendar_id,
                                          timeMin=time_min,
                                          timeMax=time_max,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result.get('items', [])

def insert_event(event_body):
    return service.events().insert(
        calendarId=calendar_id,
        body=event_body
    ).execute()

