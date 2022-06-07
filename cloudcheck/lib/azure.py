import requests
from bs4 import BeautifulSoup


class Azure:
    def __init__(self):
        pass

    def _get_ranges(self):
        """
        Get Azure IP ranges.
        Only doing Azure Front Door for now
        """

        azure_download_page = (
            "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
        )
        r = requests.get(azure_download_page)
        soup = BeautifulSoup(r.content, "html.parser")
        direct_link = soup.select_one(".failoverLink")["href"]
        r = requests.get(direct_link)
        return r.json()

    def _process_ranges(self, ranges):
        azure_ranges = []
        for item in ranges["values"]:
            try:
                if 'AzureFrontDoor' in item["name"]:
                    for addr in item["properties"]["addressPrefixes"]:
                        if '::' not in addr:
                            azure_ranges.append(addr)
            except KeyError:
                pass

        return azure_ranges
