from datetime import datetime

import ntplib


def get_current_year() -> int:
    try:
        client = ntplib.NTPClient()
        response = client.request("pool.ntp.org", version=3)
        return datetime.fromtimestamp(response.tx_time).year
    except Exception:
        return datetime.now().year
