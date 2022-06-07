import requests


class Fastly:
    """Pulls all fastly IP's"""

    def __init__(self):
        pass

    def _get_ranges(self):
        fastly_download_page = "https://api.fastly.com/public-ip-list"
        r = requests.get(fastly_download_page)
        return r.json()

    def _process_ranges(self, ranges):
        fastly_ranges = []
        for line in ranges["addresses"]:
            try:
                if '::' not in line:
                    fastly_ranges.append(line)
            except KeyError:
                pass

        return fastly_ranges
