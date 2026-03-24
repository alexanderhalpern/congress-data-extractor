import sys, os
from config import Settings
from cache import Cache
from fetchers import CongressFetcher, LCFetcher
from extractor import LLMExtractor
from writer import ExcelWriter
from pipeline import Pipeline
from utils import load_urls, build_todo
from models import LLMResult


def main() -> None:
    settings = Settings()

    test_n = int(sys.argv[sys.argv.index("--test") + 1]) if "--test" in sys.argv else 0

    os.makedirs("out", exist_ok=True)
    all_urls = load_urls("in/congress.txt")
    cache = Cache("out/results_cache.json")
    fetch_cache = Cache("out/fetch_cache.json")
    todo = build_todo(all_urls, cache, test_n)

    print(f"{len(all_urls)} total, {len(cache.data)} cached, {len(todo)} to process")
    if not todo:
        return

    writer = ExcelWriter()
    fetchers = [CongressFetcher(settings.congress_api_key), LCFetcher()]
    extractor = LLMExtractor(settings.anthropic_api_key, settings.anthropic_model)
    pipeline = Pipeline(fetchers, extractor, writer, cache, fetch_cache)

    for url in all_urls:
        entry = cache.get(url)
        if entry:
            result = LLMResult.model_validate(entry)
            if result.sufficient_data:
                writer.write(result)

    pipeline.run(todo)
    print(f"saved to {writer.out_file}")


if __name__ == "__main__":
    main()
