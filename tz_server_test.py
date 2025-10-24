#!/usr/bin/env python3

import json
from urllib.parse import urlparse
import requests

def load_timezones(json_file_path):
    """
    Reads a JSON file containing a list of timezones and returns a set for fast lookup.
    
    Args:
        json_file_path (str): Path to the JSON file.
        
    Returns:
        set: A set of timezone strings.
    """
    with open(json_file_path, 'r', encoding='utf-8') as file:
        timezone_list = json.load(file)
    return set(timezone_list)

# Example usage:
# timezones = load_timezones('timezones.json')
# print("Africa/Accra" in timezones)  # True if exists

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
