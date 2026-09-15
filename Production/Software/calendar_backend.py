from datetime import datetime, timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CREDENTIALS_FILE = "calendar_desktop_credentials.json"
TOKEN_FILE = "token.json"
HOUSE_TOKEN = "house_token.json"

def get_calendar_service(token_searchable):
    credentials = None

    try:
        credentials = Credentials.from_authorized_user_file(
        token_searchable,
        SCOPES)
    except FileNotFoundError:
        pass

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    if not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE,
            SCOPES
        )

        credentials = flow.run_local_server(port=0)

        with open(token_searchable, "w") as token:
            token.write(credentials.to_json())

    return build(
        "calendar",
        "v3",
        credentials=credentials
    )

def get_upcoming_events():
    service = get_calendar_service(TOKEN_FILE)

    now = datetime.now(timezone.utc).isoformat()

    result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=6,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = result.get("items",[])

    formatted_events = []

    for event in events:
        name = event.get("summary", "Untitled event") 
        start = event["start"].get("dateTime")
        end = event["end"].get("dateTime")

        if not start or not end:
            continue

        start_time = datetime.fromisoformat(
            start.replace("Z", "+00:00")
        )

        end_time = datetime.fromisoformat(
            end.replace("Z", "+00:00")
        )

        start_text = start_time.strftime("%-I:%M %p")
        end_text = end_time.strftime("%-I:%M %p")
        date_text = start_time.strftime("%b %-d")

        formatted_events.append(
            f"{name} | {start_text}-{end_text} | {date_text}"
        )

    return formatted_events[:6]

def get_events_for_day(date):
    service = get_calendar_service(TOKEN_FILE)

    time_min = f"{date}T00:00:00Z"
    time_max = f"{date}T23:59:59Z"
    result  = service.events().list(
        calendarId = "primary",
        timeMin = time_min,
        timeMax = time_max,
        singleEvents = True,
        orderBy = "startTime"
    ).execute()

    events = result.get("items", [])

    formatted_events = []

    if not events:
        print("No events for day")

    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            summary = event.get('summary', 'No Title')

            start_time = datetime.fromisoformat(start)
            end_time = datetime.fromisoformat(end)

            start_text = start_time.strftime("%-I:%M %p")
            end_text = end_time.strftime("%-I:%M %p")

            formatted_events.append(f"{summary} | {start_text} to {end_text}")
            print(f"{summary} | {start_text} to {end_text}")

        return formatted_events