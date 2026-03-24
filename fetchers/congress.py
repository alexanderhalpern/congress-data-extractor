import json
import requests
from fetchers.base import BaseFetcher
from utils import parse_event_id, fetch_pdf_text, is_lc_url
from schema import TRANSCRIPT_CHARS, API_CHARS


class CongressFetcher(BaseFetcher):
    def __init__(self, api_key: str):
        self.session = requests.Session()
        self.session.headers["X-Api-Key"] = api_key

    def can_handle(self, url: str) -> bool:
        return not is_lc_url(url) and parse_event_id(url)[1] is not None

    def fetch(self, url: str) -> str | None:
        congress, event_id = parse_event_id(url)
        if not congress:
            return None

        resp = self.session.get(
            f"https://api.congress.gov/v3/committee-meeting/{congress}/house/{event_id}",
            params={"format": "json"}, timeout=30,
        )
        if resp.status_code != 200:
            return None

        api_data = resp.json().get("committeeMeeting", {})
        transcript = None

        for ht in api_data.get("hearingTranscript", []):
            if not ht.get("url"):
                continue
            try:
                ht_resp = self.session.get(ht["url"], params={"format": "json"}, timeout=30)
                for fmt in ht_resp.json().get("hearing", {}).get("formats", []):
                    if fmt.get("type") == "PDF" and fmt.get("url"):
                        transcript = fetch_pdf_text(fmt["url"])
                        break
            except Exception:
                pass
            if transcript:
                break

        if not transcript:
            for label in ["Hearing: Transcript", "Hearing: Member Roster", "Hearing: Witness List", "Hearing: Cover Page"]:
                doc = next((d for d in api_data.get("meetingDocuments", []) if d.get("name") == label or d.get("type") == label), None)
                if doc and doc.get("url"):
                    try:
                        transcript = fetch_pdf_text(doc["url"])
                        break
                    except Exception:
                        pass

        parts = ["=== API METADATA ===\n" + json.dumps(api_data, default=str)[:API_CHARS]]
        if transcript:
            parts.append("=== TRANSCRIPT ===\n" + transcript[:TRANSCRIPT_CHARS])
        return "\n\n".join(parts)
