import requests


class Aws:
    """Pulls only AWS cloudfront IP's"""

    def __init__(self):
        pass

    def _get_ranges(self):
        aws_download_page = "https://ip-ranges.amazonaws.com/ip-ranges.json"
        r = requests.get(aws_download_page)
        return r.json()

    def _process_ranges(self, ranges):
        aws_ranges = []
        for item in ranges["prefixes"]:
            if item["service"] == "CLOUDFRONT":
                if '::' not in item["ip_prefix"]:
                    aws_ranges.append(item["ip_prefix"])

        return aws_ranges
