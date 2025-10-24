# Timezone HTTP Server

## Starting the server

This HTTP server serves time data in the same format as **WorldTime.org**.

Start the server like this:

```
python ./tz_server.py
```

## Using the server

Access the server via URL. For example, the following URL:

```
http://[YOUR SERVER]:11080/timezone/Europe/Berlin
```
Here `Europe/Berlin` is the timezone we like to query. The port is currently hardcoded to `11080`, but in the future, it might be configurable via a configuration file.

Will return time information for the timezone you requested in JSON format:

```json
{
"utc_offset": "+02:00",
"timezone": "Europe/Berlin",
"day_of_week": 4,
"day_of_year": 296,
"datetime": "2025-10-23T02:26:24.423039+02:00",
"utc_datetime": "2025-10-23T00:26:24.423039+00:00",
"unixtime": 1761179184,
"raw_offset": 3600,
"week_number": 42,
"dst": true,
"abbreviation": "CEST",
"dst_offset": 3600,
"dst_from": "2025-03-30T01:00:00+00:00",
"dst_until": "2025-10-26T01:00:00+00:00",
"client_ip": "134.123.45.67"
}
```

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