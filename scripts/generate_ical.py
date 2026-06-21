#!/usr/bin/env python3
"""
Generate iCalendar (.ics) file from community events JSON.
Enables calendar subscription for Google Calendar, Outlook, Apple Calendar, etc.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import quote


def escape_ical_string(text):
    """Escape special characters in iCalendar format."""
    if not text:
        return ""
    text = str(text)
    text = text.replace("\\", "\\\\")
    text = text.replace(";", "\\;")
    text = text.replace(",", "\\,")
    text = text.replace("\n", "\\n")
    return text


def generate_ical_event(event):
    """Generate VEVENT block for a single event."""
    event_id = escape_ical_string(event.get("id", ""))
    title = escape_ical_string(event.get("title", ""))
    description = escape_ical_string(event.get("description", ""))
    location = escape_ical_string(event.get("location", ""))

    # Parse date and time
    date_str = event.get("date", "")
    time_start = event.get("time_start", "000000Z")
    time_end = event.get("time_end", "010000Z")

    # Convert to iCal datetime format
    if date_str:
        # Format: YYYYMMDDTHHMMSSZ
        dt_start = f"{date_str.replace('-', '')}T{time_start.replace(':', '')}"
        dt_end = f"{date_str.replace('-', '')}T{time_end.replace(':', '')}"
    else:
        dt_start = "20260705T140000Z"
        dt_end = "20260705T150000Z"

    # Recurring rule
    rrule = event.get("recurring", "")
    rrule_line = ""
    if rrule:
        freq_map = {
            "DAILY": "DAILY",
            "WEEKLY": "WEEKLY",
            "BI-WEEKLY": "WEEKLY;INTERVAL=2",
            "MONTHLY": "MONTHLY",
            "BI-MONTHLY": "MONTHLY;INTERVAL=2",
            "QUARTERLY": "QUARTERLY",
            "YEARLY": "YEARLY"
        }
        freq = freq_map.get(rrule, "")
        if freq:
            rrule_line = f"RRULE:FREQ={freq};COUNT=12\n"

    # Build VEVENT
    ical_event = f"""BEGIN:VEVENT
UID:zelex-{event_id}@zelexdoll.com
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
DTSTART:{dt_start}
DTEND:{dt_end}
SUMMARY:{title}
DESCRIPTION:{description}
LOCATION:{location}
{rrule_line}TRANSP:OPAQUE
STATUS:CONFIRMED
SEQUENCE:0
CATEGORIES:ZELEX Community
X-MICROSOFT-CDO-BUSYSTATUS:BUSY
X-MICROSOFT-CATEGORIES:ZELEX
END:VEVENT
"""
    return ical_event


def generate_ical(events_json_path, output_path):
    """Generate iCalendar file from JSON events data."""

    # Load events
    with open(events_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    events = data.get("events", [])

    # Build iCalendar file
    ical_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//ZELEX//Community Events//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:ZELEX Community Events
X-WR-CALDESC:Official ZELEX collector community events calendar
X-WR-TIMEZONE:UTC
X-WR-CALDEL-DISPLAY-NAME:ZELEX Community Events
COLOR:#2a2a2a
"""

    # Add each event
    for event in events:
        ical_content += generate_ical_event(event)

    # Close calendar
    ical_content += "END:VCALENDAR\n"

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ical_content)

    print(f"✓ Generated iCalendar: {output_path}")
    print(f"  Events: {len(events)}")
    print(f"  Size: {len(ical_content)} bytes")

    return True


def main():
    script_dir = Path(__file__).resolve().parent
    project_dir = script_dir.parent

    events_json = project_dir / "db" / "community_events_calendar.json"
    output_ics = project_dir / "community-calendar.ics"

    if not events_json.exists():
        print(f"Error: {events_json} not found")
        return False

    try:
        generate_ical(events_json, output_ics)
        return True
    except Exception as e:
        print(f"Error generating iCal: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
