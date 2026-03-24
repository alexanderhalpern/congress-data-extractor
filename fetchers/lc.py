import re, time
import cloudscraper
from bs4 import BeautifulSoup
from fetchers.base import BaseFetcher
from utils import is_lc_url
from schema import TRANSCRIPT_CHARS


class LCFetcher(BaseFetcher):
    def __init__(self):
        self.session = cloudscraper.create_scraper()

    def can_handle(self, url: str) -> bool:
        return is_lc_url(url)

    def fetch(self, url: str) -> str | None:
        clean_url = re.sub(r"\?.*$", "", url).rstrip("/")
        if not clean_url.endswith("/text"):
            clean_url += "/text"

        for attempt in range(3):
            if attempt:
                time.sleep(5 * attempt)
            try:
                resp = self.session.get(clean_url, timeout=30)
                if resp.status_code == 200 and len(resp.text) > 500:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    content = soup.find(id="content") or soup.body
                    for tag in content(["script", "style", "noscript"]):
                        tag.decompose()
                    text = re.sub(r"\s+", " ", content.get_text(separator=" ", strip=True)).strip()
                    return text[:TRANSCRIPT_CHARS] if len(text) > 500 else None
            except Exception:
                pass
        return None
