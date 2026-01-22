import requests

class Fetcher:
    def get(self, url: str, timeout=15) -> str:
        r = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=timeout
        )
        r.raise_for_status()
        return r.text