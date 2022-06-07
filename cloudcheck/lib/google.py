import requests


class Google:
    """Pulls all GCP and googleusercontent IPs"""

    def __init__(self):
        pass

    def _get_ranges(self):
        google_download_page = "https://www.gstatic.com/ipranges/cloud.json"
        r = requests.get(google_download_page)
        return r.json()

    def _process_ranges(self, ranges):
        google_ranges = []
        for line in ranges["prefixes"]:
            try:
                google_ranges.append(line["ipv4Prefix"])
            except KeyError:
                pass

        return google_ranges
