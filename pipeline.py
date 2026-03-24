from tqdm import tqdm
from fetchers import BaseFetcher
from extractor import LLMExtractor
from writer import ExcelWriter
from cache import Cache


class Pipeline:
    def __init__(self, fetchers: list[BaseFetcher], extractor: LLMExtractor, writer: ExcelWriter, cache: Cache, fetch_cache: Cache):
        self.fetchers = fetchers
        self.extractor = extractor
        self.writer = writer
        self.cache = cache
        self.fetch_cache = fetch_cache

    def process(self, url: str) -> None:
        if url in self.fetch_cache:
            fetched = self.fetch_cache.get(url)
        else:
            fetcher = next((f for f in self.fetchers if f.can_handle(url)), None)
            if not fetcher:
                return
            try:
                fetched = fetcher.fetch(url)
            except Exception:
                return
            if not fetched:
                return
            self.fetch_cache.set(url, fetched)

        try:
            result = self.extractor.extract(url, fetched)
        except Exception as e:
            print(f"LLM error: {e}")
            return

        self.cache.set(url, result.model_dump())
        if result.sufficient_data:
            self.writer.write(result)
            print(result.hearing.hearingID)
        else:
            print(f"skip: {result.missing_reason}")

    def run(self, urls: list[str]) -> None:
        for url in tqdm(urls):
            if url not in self.cache:
                self.process(url)
