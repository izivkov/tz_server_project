#!/usr/bin/env python3

import requests
from timezone_api.timezone_utils import load_timezones

def fetch_timezone_info(base_url, timezone):
    """
    Sends an HTTP GET request to retrieve timezone info for a given IANA name.
    Returns the parsed JSON data or None if request fails.
    """
    try:
        response = requests.get(f"{base_url}/timezone/{timezone}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching {timezone}: {e}")
        return None
    
def run():
    base_url = "http://localhost:11080"  
    timezones = load_timezones('static/timezones.json')

    for tz in timezones:
        info = fetch_timezone_info(base_url, tz)
        if info:
            print(f"{tz}: {info}")
        else:
            print(f"Failed to retrieve info for {tz}")

if __name__ == '__main__':
    run()
