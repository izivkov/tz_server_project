import json
from urllib.parse import urlparse

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
