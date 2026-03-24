from anthropic import Anthropic
from models import LLMResult
from schema import PROMPT, OUTPUT_SCHEMA


class LLMExtractor:
    def __init__(self, api_key, model):
        self.client = Anthropic(api_key=api_key, max_retries=3)
        self.model = model

    def extract(self, url, text) -> LLMResult:
        resp = self.client.messages.create(
            model=self.model,
            max_tokens=8192,
            system=PROMPT,
            messages=[{"role": "user", "content": f"URL: {url}\n\n{text}"}],
            output_config={"format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
        )
        return LLMResult.model_validate_json(resp.content[0].text)
