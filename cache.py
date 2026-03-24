import os, json
from typing import Any


class Cache:
    def __init__(self, path: str):
        self.path = path
        self.data: dict[str, Any] = json.load(open(path)) if os.path.exists(path) else {}

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def get(self, key: str) -> Any:
        return self.data.get(key)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        tmp = self.path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.data, f, indent=2, default=str)
        os.replace(tmp, self.path)
