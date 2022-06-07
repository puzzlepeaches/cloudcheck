import requests


class Incapsula:
    """Pulls all Incapsula IP ranges"""

    def __init__(self):
        pass

    def _get_ranges(self):
        data = {'resp_format': 'text', }
        response = requests.get(
            'https://my.imperva.com/api/integration/v1/ips', data=data, verify=False)
        return response.text

    def _process_ranges(self, ranges):
        incapsula_ranges = []
        for line in ranges.splitlines():
            if '::' not in line:
                incapsula_ranges.append(line)

        return incapsula_ranges
