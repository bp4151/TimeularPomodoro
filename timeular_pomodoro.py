import json
import os
import sys
import time
import datetime
from datetime import timezone
import dotenv
import logging
import requests
import schedule
from dateutil.parser import parse

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger()

baseurl = 'https://api.timeular.com/api/v3/'


def get_current_tracking(_api_token: str, _activities: list):

    logger.debug('Getting currently tracked item from Timeular')

    current_item = {}

    url = "tracking"

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + _api_token
    }

    try:
        response = requests.request("GET", baseurl + url, headers=headers, data=payload)
        response.raise_for_status()
        current_tracking_item = response.json()['currentTracking']

        if current_tracking_item is not None:
            for activity in _activities:
                if current_tracking_item['activityId'] == activity['id']:
                    current_item = current_tracking_item
                    logger.debug(f'Found activity {activity["name"]} to check')
                    logger.debug(f'Setting length to {activity["time"]} minutes')
                    current_item['lengthInMinutes'] = activity['time']

        # do something with the current_item object here.
        if len(current_item) > 0:

            logger.debug(f'Current_item: {current_item}')

            start_date_time = parse(current_item['startedAt'])
            stop_date_time = start_date_time + datetime.timedelta(minutes=float(current_item['lengthInMinutes']))
            minutes = int((stop_date_time - datetime.datetime.utcnow()).seconds / 60)

            if minutes == 0:
                logger.debug('Stopping activity')
                stop_tracking(_api_token)
            else:
                logger.debug(f'Minutes remaining: {minutes}')
        else:
            logger.debug(f'Not currently tracking any activity')

    except requests.exceptions.HTTPError as errh:
        logger.error(msg=f'An HTTP error occurred. {errh.response.text}')
    except requests.exceptions.ConnectionError as errc:
        logger.error(msg=f'A Connection error occurred', exc_info=errc)
    except requests.exceptions.Timeout as errt:
        logger.error(msg=f'A Timeout error occurred', exc_info=errt)
    except requests.exceptions.RequestException as err:
        logger.error(msg=f'A general RequestException occurred', exc_info=err)


def list_activities(_api_token: str, _api_activities: list) -> list:

    logger.debug('Getting list of activities from Timeular that match those in environment variable')

    url = "activities"

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + _api_token
    }

    try:
        response = requests.request("GET", baseurl + url, headers=headers, data=payload)
        response.raise_for_status()
        returned_activities = list(response.json()['activities'])
        selected_activities = list(_api_activities)
        common_activities = []
        for activity in reversed(returned_activities):
            for selected_activity in selected_activities:
                if str(activity['name']).upper() == str(selected_activity['name']).upper():
                    activity['time'] = selected_activity['time']
                    common_activities.append(activity)
        return common_activities
    except requests.exceptions.HTTPError as errh:
        logger.error(msg=f'An HTTP error occurred. {errh.response.text}')
    except requests.exceptions.ConnectionError as errc:
        logger.error(msg=f'A Connection error occurred', exc_info=errc)
    except requests.exceptions.Timeout as errt:
        logger.error(msg=f'A Timeout error occurred', exc_info=errt)
    except requests.exceptions.RequestException as err:
        logger.error(msg=f'A general RequestException occurred', exc_info=err)

    return []


def login(_api_key: str, _api_secret: str) -> str:

    logger.debug('Logging in to Timelar API to get API token')

    url = 'developer/sign-in'
    payload = json.dumps({
        "apiKey": _api_key,
        "apiSecret": _api_secret
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()['token']
    except requests.exceptions.HTTPError as errh:
        logger.error(msg=f'An HTTP error occurred. {errh.response.text}')
    except requests.exceptions.ConnectionError as errc:
        logger.error(msg=f'A Connection error occurred', exc_info=errc)
    except requests.exceptions.Timeout as errt:
        logger.error(msg=f'A Timeout error occurred', exc_info=errt)
    except requests.exceptions.RequestException as err:
        logger.error(msg=f'A general RequestException occurred', exc_info=err)
    return ''


def stop_tracking(_api_token: str):
    logger.debug('Stopping the tracking of the current activity')

    url = "tracking/stop"

    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=None)

    payload = json.dumps({
        "stoppedAt": utc_time.isoformat(timespec='milliseconds')
    })
    headers = {
        'Authorization': 'Bearer ' + _api_token,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", baseurl + url, headers=headers, data=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.error(msg=f'An HTTP error occurred. {errh.response.text}')
    except requests.exceptions.ConnectionError as errc:
        logger.error(msg=f'A Connection error occurred', exc_info=errc)
    except requests.exceptions.Timeout as errt:
        logger.error(msg=f'A Timeout error occurred', exc_info=errt)
    except requests.exceptions.RequestException as err:
        logger.error(msg=f'A general RequestException occurred', exc_info=err)


def main(_api_key: str, _api_secret: str, _api_activities: list):
    api_token = login(api_key, api_secret)

    if api_token == '':
        logger.error('No API key was returned, exiting with error')
        sys.exit(1)

    activities = list_activities(api_token, api_activities)

    # when scheduler hits, run the get_current_tracking function and receive the data into the Event tuple
    # action is the get_current_tracking function result

    logger.debug('Setting timer to retrieve Timeular currently tracked item every 30 seconds')
    schedule.every(30).seconds.do(get_current_tracking, _api_token=api_token, _activities=activities)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    dotenv.load_dotenv()
    api_key = os.getenv('API_KEY')
    api_secret = os.getenv('API_SECRET')
    api_activities = json.loads(os.getenv('API_ACTIVITIES'))

    main(api_key, api_secret, api_activities)
