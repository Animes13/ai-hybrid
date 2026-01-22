import os
import time
import json
import re
import logging
from typing import Dict, Any, Optional

from google import genai
from google.genai import types

from ai.engine import AIEngine
from ai.prompts import build_prompt
from ai.validator import validate_response

log = logging.getLogger("Gemini")

COOLDOWN = 90
MAX_RETRIES = 4


class GeminiPool:
    def __init__(self):
        self.keys = [k for k in (
            os.getenv("GEMINI_KEY_1"),
            os.getenv("GEMINI_KEY_2"),
            os.getenv("GEMINI_KEY_3"),
            os.getenv("GEMINI_KEY_4"),
        ) if k]

        if not self.keys:
            raise RuntimeError("Nenhuma GEMINI_KEY configurada")

        self.cooldown = {k: 0 for k in self.keys}
        self.idx = 0

    def next(self) -> Optional[str]:
        now = time.time()
        for _ in range(len(self.keys)):
            key = self.keys[self.idx]
            self.idx = (self.idx + 1) % len(self.keys)
            if self.cooldown[key] <= now:
                return key
        return None

    def fail(self, key: str):
        log.warning("Key Gemini em cooldown")
        self.cooldown[key] = time.time() + COOLDOWN


class GeminiClient(AIEngine):

    def __init__(self):
        self.pool = GeminiPool()

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        html = context.get("html", "")
        if not html or "<html" not in html.lower():
            raise RuntimeError("HTML inválido")

        last_error = None

        for attempt in range(MAX_RETRIES):
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
                        max_output_tokens=2048,
                    )
                )

                data = self._safe_json(r.text)
                validate_response(data, context)
                data["_source"] = "gemini"
                return data

            except Exception as e:
                last_error = e
                log.error("Erro Gemini: %s", e)
                if "JSON incompleto" not in str(e):
                    self.pool.fail(key)

        raise RuntimeError(f"Gemini falhou: {last_error}")

    def _safe_json(self, text: str) -> Dict[str, Any]:
        text = re.sub(r"```(?:json)?", "", text)

        start = text.find("{")
        if start == -1:
            raise ValueError("JSON incompleto")

        open_count = 0
        for i, ch in enumerate(text[start:]):
            if ch == "{":
                open_count += 1
            elif ch == "}":
                open_count -= 1
                if open_count == 0:
                    json_text = text[start:start + i + 1]
                    return json.loads(json_text)

        raise ValueError("JSON incompleto")