import os, time, json, re
from typing import Dict, Any, Optional
from google import genai
from google.genai import types
from ai.engine import AIEngine
from ai.prompts import build_prompt
from ai.validator import validate_response

COOLDOWN = 90
MAX_RETRIES = 4

class GeminiPool:
    def __init__(self):
        self.keys = [
            os.getenv("GEMINI_KEY_1"),
            os.getenv("GEMINI_KEY_2"),
            os.getenv("GEMINI_KEY_3"),
            os.getenv("GEMINI_KEY_4"),
        ]
        self.keys = [k for k in self.keys if k]
        if not self.keys:
            raise RuntimeError("Nenhuma GEMINI_KEY configurada")
        self.cooldown = {k: 0 for k in self.keys}
        self.idx = 0

    def next(self) -> Optional[str]:
        now = time.time()
        for _ in range(len(self.keys)):
            k = self.keys[self.idx]
            self.idx = (self.idx + 1) % len(self.keys)
            if self.cooldown[k] <= now:
                return k
        return None

    def fail(self, key: str):
        self.cooldown[key] = time.time() + COOLDOWN


class GeminiClient(AIEngine):
    def __init__(self):
        self.pool = GeminiPool()

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        last = None
        for _ in range(MAX_RETRIES):
            key = self.pool.next()
            if not key:
                break
            try:
                client = genai.Client(api_key=key)
                prompt = build_prompt(context)

                r = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.1,
                        max_output_tokens=1024,
                    )
                )

                data = self._safe_json(r.text)
                validate_response(data, context)
                return data

            except Exception as e:
                last = e
                self.pool.fail(key)

        raise RuntimeError(f"Gemini falhou: {last}")

    def _safe_json(self, text):
        text = re.sub(r"```(?:json)?", "", text)
        start, end = text.find("{"), text.rfind("}") + 1
        return json.loads(text[start:end])