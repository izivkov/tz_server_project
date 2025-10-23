# Timezone HTTP Server

This HTTP server serves time data in the same format as **WorldTime.org**.

Start the server like this:

```
python ./tz_server.py
```

Access the server via URL. For example, the following URL:

```
http://[YOUR SERVER]:11080/timezone/Europe/Berlin
```
Here `Europe/Berlin` is the timezone we like to query.

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

The port is currently hardcoded to `11080`, but in the future, it might be configurable via a configuration file.
