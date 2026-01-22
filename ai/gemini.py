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

        # NÃO inventar se HTML não for real
        if html.strip() == "" or "..." in html:
            raise RuntimeError("HTML inválido ou placeholder. Use HTML real da pasta HTML/")

        last_error = None

        for attempt in range(1, MAX_RETRIES + 1):
            key = self.pool.next()
            if not key:
                break

            log.info("Tentativa Gemini %s/%s", attempt, MAX_RETRIES)

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

                log.info("Gemini retornou resposta válida")
                data["_source"] = "gemini"
                return data

            except Exception as e:
                log.error("Erro Gemini: %s", e)
                last_error = e
                self.pool.fail(key)

        raise RuntimeError(f"Gemini falhou após retries: {last_error}")

    def _safe_json(self, text: str) -> Dict[str, Any]:
        text = re.sub(r"```(?:json)?", "", text)
        match = re.search(r"\{.*\}", text, re.S)

        if not match:
            raise ValueError("Nenhum JSON encontrado")

        return json.loads(match.group())