import requests


class Cloudflare:
    """Pulls all Cloudflare IP ranges"""

    def __init__(self):
        pass

    def _get_ranges(self):
        cloudflare_download_page = "https://www.cloudflare.com/ips-v4"
        r = requests.get(cloudflare_download_page)
        return r.text

    def _process_ranges(self, ranges):
        cf_ranges = []
        for line in ranges.splitlines():
            if '::' not in line:
                cf_ranges.append(line)

        return cf_ranges
