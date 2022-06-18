from typing import Optional, TypedDict
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from lib.secrets_manager import get_gcp_service_role_json

service_role_json = get_gcp_service_role_json()


class CalenderEvent(TypedDict):
    summary: str
    start_date: Optional[str]
    start_datetime: Optional[str]
    start_timezone: Optional[str]
    end_date: Optional[str]
    end_datetime: Optional[str]
    end_timezone: Optional[str]


class GoogleCalender:
    def __init__(self, calender_id: str) -> None:
        self.credentials = Credentials.from_service_account_info(
            service_role_json)
        self.service = build('calendar', 'v3', credentials=self.credentials)
        self.calender_id = calender_id

    def create(self, event: CalenderEvent):
        self.service.events().insert(
            calendarId=self.calender_id,
            body={
                'summary': event['summary'],
                'start': {
                    'date': event.get('start_date'),
                    'dateTime': event.get('start_datetime'),
                    'timeZone': event.get('start_timezone')
                },
                'end': {
                    'date': event.get('end_date'),
                    'dateTime': event.get('end_datetime'),
                    'timeZone': event.get('end_timezone')
                }
            }).execute()
