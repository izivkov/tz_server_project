# Timezone HTTP Server

## Starting the server

This HTTP server serves time data in the same format as **WorldTime.org**.

Start the server like this:

```
python ./tz_server.py
```

text
# Timezone API Endpoints Documentation

This API provides timezone-related services based on Python's `pytz` library.

---

## Endpoints

### GET /timezone

- **Description:** Returns a JSON list of all valid timezones supported by the server.
- **Request:**

GET /timezone

text
- **Response:**

{
"timezone": [
"Africa/Abidjan",
"Africa/Accra",
"America/New_York",
"Europe/London",
...
]
}

text
- **Status Codes:**  
- `200 OK` on success.

---

### GET /timezone/{timezone_name}

- **Description:** Returns detailed current date, time, offset, and daylight saving information for the specified timezone.
- **Request:**

GET /timezone/{timezone_name}

text
- **Path Parameters:**
- `timezone_name` (string): The full timezone name (supports hierarchical names like `Europe/London`).
- **Response:**

{
"utc_offset": "+02:00",
"timezone": "Europe/Berlin",
"day_of_week": 5,
"day_of_year": 297,
"datetime": "2025-10-24T10:57:48.851324+02:00",
"utc_datetime": "2025-10-24T08:57:48.851324+00:00",
"unixtime": 1761292668,
"raw_offset": 7200,
"week_number": 42,
"dst": true,
"abbreviation": "CEST",
"dst_offset": 3600,
"dst_from": "2025-03-30T01:00:00+00:00",
"dst_until": "2025-10-26T01:00:00+00:00",
"client_ip": "127.0.0.1"
}

text
- **Status Codes:**
- `200 OK` on success.
- `404 Not Found` if the timezone is not recognized.

---

### GET /validate/{timezone_name}

- **Description:** Validates whether the specified timezone name is recognized by the server.
- **Request:**

GET /validate/{timezone_name}

text
- **Path Parameters:**
- `timezone_name` (string): The timezone name to validate.
- **Response:**
- If valid:
  ```
  {
    "isValid": "true"
  }
  ```
- If invalid:
  ```
  {
    "isValid": "false"
  }
  ```
- **Status Codes:**
- `200 OK` - validation status returned.

---

## Error Response

- For unknown endpoints or methods:
- Status Code: `404 Not Found`
- Response Body:
  ```
  Unknown endpoint
  ```

---

## Create virtual environment

```
python -m venv .
source "venv/bin/activate"
```

## Starting the server automatically on boot

Create a file `/etc/systemd/system/tz_server.service` with the following content:

```
[Unit]
Description=Timezone API Server
After=network.target

[Service]
User=[YOUR_ID]
Group=[YOUR_ID]
WorkingDirectory=[YOUR PROJECT DIRECTORY]
ExecStart=[YOUR PROJECT DIRECTORY]/venv/bin/python /[YOUR PROJECT DIRECTORY]tz_server.py
Restart=always
RestartSec=5
Environment=VIRTUAL_ENV=[YOUR PROJECT DIRECTORY]/venv
Environment=PATH=[YOUR PROJECT DIRECTORY]/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

[Install]
WantedBy=multi-user.target
```

Start it like this:
```
sudo systemctl daemon-reload
sudo systemctl enable tz_server.service
sudo systemctl start tz_server.service
```