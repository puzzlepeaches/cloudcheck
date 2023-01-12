import requests


class Incapsula:
    """Pulls all Incapsula IP ranges"""

    def __init__(self):
        pass

    def _get_ranges(self):
        data = {"resp_format": "json"}
        response = requests.post(
            "https://my.imperva.com/api/integration/v1/ips", data=data, verify=False
        ).json()
        response = response["ipRanges"]
        return response

    def _process_ranges(self, ranges):
        return ranges
