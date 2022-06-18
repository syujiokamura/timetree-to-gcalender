from lib.google_calender import GoogleCalender, CalenderEvent as GoogleCalenderEvent
from lib.secrets_manager import get_secrets_values
from lib.timetree import CalenderEvent, Timetree

secrets = get_secrets_values()


def sync_calender(_event, _context):
    timetree = Timetree(secrets['TIMETREE_PERSONAL_TOKEN'])
    calender_list = timetree.get_calender_list()
    main_calender = next(
        filter(lambda x: x['attributes']['name'] == secrets['CALENDER_NAME'], calender_list))

    if main_calender is None:
        raise Exception('calender not found')

    calender_id = main_calender['id']
    event_list = timetree.get_event_list(calender_id)
    print(event_list)
    google_calender = GoogleCalender(calender_id=secrets['GOOGLE_CALENDER_ID'])
    for event in event_list:
        google_calender.create(event=mappings_calender_event(event))


def mappings_calender_event(event: CalenderEvent) -> GoogleCalenderEvent:
    return {
        'summary': event['title'],
        'start_date': event['start_at'].strftime('%Y-%m-%d'),
        'end_date': event['end_at'].strftime('%Y-%m-%d'),
    } if event['all_day'] else {
        'summary': event['title'],
        'start_datetime': event['start_at'].isoformat(timespec='seconds'),
        'start_timezone': event.get('start_timezone'),
        'end_datetime': event['end_at'].isoformat(timespec='seconds'),
        'end_timezone': event.get('end_timezone')
    }
