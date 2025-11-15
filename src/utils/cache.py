import os, json, hashlib, time
from typing import Any, Optional

class SimpleCache:
    def __init__(self, cache_dir: str = "outputs/cache", ttl_seconds: int = 1800):
        self.cache_dir = cache_dir
        self.ttl = ttl_seconds
        os.makedirs(self.cache_dir, exist_ok=True)

    def _key(self, payload: Any) -> str:
        blob = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
        return hashlib.md5(blob).hexdigest()

    def get(self, payload: Any) -> Optional[dict]:
        key = self._key(payload)
        path = os.path.join(self.cache_dir, f"{key}.json")
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r") as f:
                obj = json.load(f)
            if time.time() - obj.get("_ts", 0) > self.ttl:
                return None
            return obj.get("data")
        except Exception:
            return None

    def set(self, payload: Any, data: dict) -> None:
        key = self._key(payload)
        path = os.path.join(self.cache_dir, f"{key}.json")
        with open(path, "w") as f:
            json.dump({"_ts": time.time(), "data": data}, f, indent=2)
