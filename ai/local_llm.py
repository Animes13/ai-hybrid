import json
import re
import logging
import requests
from typing import Dict, Any

from ai.engine import AIEngine
from ai.prompts import build_prompt
from ai.validator import validate_response

log = logging.getLogger("LocalLLM")

class LocalLLM(AIEngine):
    MODEL = "llama3-mini"
    OLLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        html = context.get("html", "")

        if html.strip() == "" or "<html" not in html.lower():
            raise RuntimeError("HTML inválido ou placeholder. Use HTML real da pasta HTML/")

        log.info("Iniciando análise LocalLLM")
        prompt = build_prompt(context)

        try:
            response = requests.post(
                self.OLLAMA_URL,
                json={
                    "model": self.MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                    "max_tokens": 1024
                },
                timeout=600
            )
        except requests.Timeout:
            log.error("Timeout no Ollama API")
            raise RuntimeError("Timeout no Ollama API")

        if response.status_code != 200:
            log.error("Erro no Ollama API: %s", response.text)
            raise RuntimeError(response.text)

        text = response.json()["choices"][0]["message"]["content"]
        log.debug("Resposta bruta do modelo: %s", text[:500])

        data = self._safe_json(text)
        validate_response(data, context)

        log.info("LocalLLM retornou resposta válida")
        data["_source"] = "local"
        return data

    def _safe_json(self, text: str) -> Dict[str, Any]:
        text = re.sub(r"```(?:json)?", "", text)

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1 or end <= start:
            log.error("JSON incompleto na resposta. Saída completa:\n%s", text)
            raise ValueError("JSON incompleto")

        json_text = text[start:end + 1]

        try:
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            log.error("JSON inválido: %s", e)
            log.error("Trecho JSON:\n%s", json_text)
            raise ValueError("JSON incompleto")