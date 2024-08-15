import re
from datetime import timedelta, datetime

def parse_date_input(s: str):
    now = datetime.now()
    if s == "now":
        return now
    if match := re.match(r"(\d+)\s?(h|day|week)", s):
        v, arg = int(match.group(1)), {"h": "hours", "day": "days", "week": "weeks"}[match.group(2)]
        try:
            return now - timedelta(**{arg: v})
        except TypeError:
            pass
    for fmt in (r"%Y-%m-%dT%H:%M:%S", r"%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    raise ValueError(f"Time argument should be ISO (2023-11-17[T18:01:32]) or '\d+ h|day|week' formatted. Got '{s}'")
