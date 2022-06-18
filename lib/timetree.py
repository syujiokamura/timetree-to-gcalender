import requests

from datetime import datetime
from typing import List, Optional, TypedDict

base_url = 'https://timetreeapis.com'


class CalenderEvnAtattributes(TypedDict):
    title: str
    all_day: str
    start_at: str
    start_timezone: str
    end_at: str
    end_timezone: str
    updated_at: str
    created_at: str
    category: str


class CalenderEventResponse(TypedDict):
    id: str
    attributes: CalenderEvnAtattributes


class CalenderEvent(TypedDict):
    id: str
    title: Optional[str]
    all_day: bool
    start_at: datetime
    start_timezone: Optional[str]
    end_at: datetime
    end_timezone: Optional[str]
    updated_at: datetime
    created_at: datetime
    category: Optional[str]


class Timetree:
    def __init__(self, personal_token) -> None:
        self.personal_token = personal_token
        self.request_header = {
            'Accept': 'application/vnd.timetree.v1+json',
            'Authorization': f'Bearer {personal_token}',
        }

    def get_calender_list(self) -> dict:
        res = requests.get(f'{base_url}/calendars',
                           headers=self.request_header)
        data = res.json()['data']
        print(data)
        return data

    def get_event_list(self, calender_id: str) -> List[CalenderEvent]:
        # daysパラメータから最大日数の7日分のイベントを取得している
        res = requests.get(
            url=f'{base_url}/calendars/{calender_id}/upcoming_events?days=7',
            headers=self.request_header
        )
        data = res.json()['data']
        print(data)

        return [dict(
            id=event['id'],
            title=event['attributes'].get('title'),
            all_day=event['attributes'].get('all_day'),
            start_at=datetime.fromisoformat(
                event['attributes']['start_at'].replace('Z', '+00:00')),
            start_timezone=event['attributes'].get('start_timezone'),
            end_at=datetime.fromisoformat(
                event['attributes']['end_at'].replace('Z', '+00:00')),
            end_timezone=event['attributes'].get('end_timezone'),
            updated_at=datetime.fromisoformat(
                event['attributes']['updated_at'].replace('Z', '+00:00')),
            created_at=datetime.fromisoformat(
                event['attributes']['created_at'].replace('Z', '+00:00')),
            category=event['attributes'].get('category'),
        ) for event in data]
