#!/usr/bin/env python3

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import datetime
import pytz

PORT = 11080

class TimezoneRequestHandler(BaseHTTPRequestHandler):
    valid_timezones = set(pytz.all_timezones)    

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path_parts = parsed_url.path.strip('/').split('/')

        # Check for /validate/{timezone}
        if len(path_parts) > 1 and path_parts[0].lower() == 'validate':
            tz_name = '/'.join(path_parts[1:]).strip()  # Remove whitespace around the full timezone string
            is_valid = tz_name in self.valid_timezones

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"isValid": str(is_valid).lower()}).encode())
            return

        # If path is /timezone (or /timezone/) return all valid timezones as JSON
        if len(path_parts) == 1 and path_parts[0].lower() == 'timezone':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Return the sorted list of all valid_timezones
            timezones_list = sorted(self.valid_timezones)
            self.wfile.write(json.dumps({"timezone": timezones_list}).encode())
            return

        # Else if path starts with /timezone/{tz_name}
        if path_parts and path_parts[0].lower() == 'timezone' and len(path_parts) > 1:
            tz_name = '/'.join(path_parts[1:])  # join all remaining parts for timezone

            try:
                tz = pytz.timezone(tz_name)
            except pytz.UnknownTimeZoneError:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Unknown timezone"}).encode())
                return

            now_utc = datetime.datetime.now(datetime.timezone.utc)
            now_tz = now_utc.astimezone(tz)

            # Calculate DST info
            is_dst = bool(now_tz.dst())
            dst_offset_sec = int(now_tz.dst().total_seconds()) if is_dst else 0
            raw_offset_sec = int(now_tz.utcoffset().total_seconds()) - dst_offset_sec

            # Find DST transitions for this year (approximate)
            year = now_tz.year
            dst_from = None
            dst_until = None

            if hasattr(tz, '_utc_transition_times') and tz._utc_transition_times:
                dst_transitions = tz._utc_transition_times
                for i in range(len(dst_transitions) - 1):
                    trans = dst_transitions[i]
                    next_trans = dst_transitions[i + 1]
                    if trans.year == year:
                        dt_now_utc = now_utc.replace(tzinfo=None)
                        trans_utc = trans.replace(tzinfo=None)
                        next_trans_utc = next_trans.replace(tzinfo=None)
                        if trans_utc <= dt_now_utc < next_trans_utc:
                            if is_dst:
                                dst_from = trans.isoformat() + '+00:00'
                                dst_until = next_trans.isoformat() + '+00:00'
                            else:
                                dst_from = next_trans.isoformat() + '+00:00'
                            break
            else:
                dst_from = None
                dst_until = None

            # Format JSON response
            response = {
                "utc_offset": now_tz.strftime('%z')[:-2] + ':' + now_tz.strftime('%z')[-2:],  # +02:00 format
                "timezone": tz_name,
                "day_of_week": now_tz.weekday() + 1,
                "day_of_year": now_tz.timetuple().tm_yday,
                "datetime": now_tz.isoformat(),
                "utc_datetime": now_utc.isoformat(),
                "unixtime": int(now_utc.timestamp()),
                "raw_offset": raw_offset_sec,
                "week_number": int(now_tz.strftime('%U')),
                "dst": is_dst,
                "abbreviation": now_tz.tzname(),
                "dst_offset": dst_offset_sec,
                "dst_from": dst_from,
                "dst_until": dst_until,
                "client_ip": self.client_address[0],
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Unknown endpoint\n')

def run(server_class=HTTPServer, handler_class=TimezoneRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f'Serving timezone API on port {PORT}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
