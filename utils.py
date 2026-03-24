import re, io
import requests, pypdf
from cache import Cache


def parse_event_id(url: str) -> tuple[str | None, str | None]:
    m = re.search(r"/(\d+)(?:th|st|nd|rd)-congress/house-event/([^/?]+)", url)
    if not m:
        return None, None
    return m.group(1), m.group(2).split("/")[0]


def fetch_pdf_text(pdf_url: str) -> str:
    resp = requests.get(pdf_url, timeout=60)
    resp.raise_for_status()
    reader = pypdf.PdfReader(io.BytesIO(resp.content))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n".join(pages)


def load_urls(path: str) -> list[str]:
    urls = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                urls.append(line)
    return urls


def is_lc_url(url: str) -> bool:
    _, event_id = parse_event_id(url)
    return bool(event_id and event_id.startswith("LC"))


def row_values(data: dict, headers: list) -> list:
    values = []
    for h in headers:
        values.append(data.get(h))
    return values


def build_todo(all_urls: list[str], cache: Cache, test_n: int = 0) -> list[str]:
    todo = []
    for u in all_urls:
        if u not in cache:
            todo.append(u)

    if not test_n:
        return todo

    api_urls = []
    lc_urls = []
    for u in todo:
        if is_lc_url(u):
            lc_urls.append(u)
        else:
            api_urls.append(u)

    return api_urls[:max(1, test_n // 2)] + lc_urls[:max(1, test_n - test_n // 2)]
