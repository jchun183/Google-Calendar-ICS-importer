import os
import sys
from pathlib import Path
from datetime import datetime, timezone

from icalendar import Calendar
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# ---------------- CONFIG ----------------
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = "primary"
# ----------------------------------------


# ✅ Handle PyInstaller paths
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parent / relative_path


# ✅ Store token in a persistent user location
APP_DATA_DIR = Path.home() / "AppData" / "Local" / "CalendarImporter"
APP_DATA_DIR.mkdir(parents=True, exist_ok=True)

CLIENT_SECRET_FILE = resource_path("credentials.json")
TOKEN_FILE = APP_DATA_DIR / "token.json"


def get_calendar_service():
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def to_google_datetime(dt):
    if dt is None:
        return None

    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return {"dateTime": dt.isoformat()}

    return {"date": dt.isoformat()}


def parse_ics_file(file_path: Path):
    with open(file_path, "rb") as f:
        cal = Calendar.from_ical(f.read())

    for component in cal.walk():
        if component.name != "VEVENT":
            continue

        uid = str(component.get("uid", ""))
        summary = str(component.get("summary", "Untitled Event"))

        location = str(component.get("location", "")) if component.get("location") else ""
        description = str(component.get("description", "")) if component.get("description") else ""

        dtstart = component.decoded("dtstart") if component.get("dtstart") else None
        dtend = component.decoded("dtend") if component.get("dtend") else None

        if not dtstart:
            raise ValueError("Missing DTSTART in ICS file")

        event = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": to_google_datetime(dtstart),
            "end": to_google_datetime(dtend) if dtend else None,
            "iCalUID": uid,
        }

        if event["end"] is None:
            if isinstance(dtstart, datetime):
                fallback = dtstart if dtstart.tzinfo else dtstart.replace(tzinfo=timezone.utc)
                event["end"] = {"dateTime": fallback.isoformat()}
            else:
                event["end"] = {"date": dtstart.isoformat()}

        return event

    raise ValueError("No VEVENT found in file")


def event_exists(service, calendar_id, ical_uid):
    if not ical_uid:
        return False

    result = service.events().list(
        calendarId=calendar_id,
        iCalUID=ical_uid
    ).execute()

    return len(result.get("items", [])) > 0


def import_event(service, calendar_id, event_body):
    return service.events().import_(
        calendarId=calendar_id,
        body=event_body
    ).execute()


def show_message(title, message):
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, title, 0)
    except Exception:
        print(f"{title}: {message}")


def process_file(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError("File not found")

    if file_path.suffix.lower() != ".ics":
        raise ValueError("Not an ICS file")

    service = get_calendar_service()
    event_body = parse_ics_file(file_path)

    uid = event_body.get("iCalUID", "")

    if uid and event_exists(service, CALENDAR_ID, uid):
        show_message("Calendar Import", "Event already exists.")
        return

    created = import_event(service, CALENDAR_ID, event_body)
    name = created.get("summary", "Event")

    show_message("Calendar Import", f'Successfully imported: "{name}"')


def main():
    if len(sys.argv) < 2:
        show_message("Calendar Import", "No file selected.")
        return

    file_path = Path(sys.argv[1])

    try:
        process_file(file_path)
    except Exception as e:
        show_message("Error", str(e))


if __name__ == "__main__":
    main()