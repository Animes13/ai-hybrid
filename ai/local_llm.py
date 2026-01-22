import subprocess
import json
import re
import logging
from typing import Dict, Any
from ai.engine import AIEngine
from ai.prompts import build_prompt
from ai.validator import validate_response

log = logging.getLogger("LocalLLM")

class LocalLLM(AIEngine):
    MODEL = "qwen2.5:7b"

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        html = context.get("html", "")

        # NÃO inventar se HTML não for real
        if html.strip() == "" or "<html" not in html.lower():
            raise RuntimeError("HTML inválido ou placeholder. Use HTML real da pasta HTML/")

        log.info("Iniciando análise LocalLLM")
        prompt = build_prompt(context)

        try:
            r = subprocess.run(
                ["ollama", "run", self.MODEL],
                input=prompt,
                text=True,
                capture_output=True,
                timeout=300  # Aumentado
            )
        except subprocess.TimeoutExpired:
            log.error("Timeout no Ollama")
            raise RuntimeError("Timeout no Ollama")

        if r.returncode != 0:
            log.error("Erro no Ollama: %s", r.stderr)
            raise RuntimeError(r.stderr)

        log.debug("Resposta bruta do modelo: %s", r.stdout[:500])

        data = self._safe_json(r.stdout)
        validate_response(data, context)

        log.info("LocalLLM retornou resposta válida")
        data["_source"] = "local"
        return data

    def _safe_json(self, text: str) -> Dict[str, Any]:
        text = re.sub(r"```(?:json)?", "", text)

        start = text.find("{")
        if start == -1:
            log.error("Nenhum JSON encontrado na resposta. Saída completa:\n%s", text)
            raise ValueError("Nenhum JSON encontrado")

        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1

            if depth == 0:
                json_text = text[start:i+1]
                try:
                    return json.loads(json_text)
                except json.JSONDecodeError as e:
                    log.error("JSON inválido: %s", e)
                    log.error("Trecho JSON:\n%s", json_text)
                    raise

        log.error("JSON incompleto na resposta. Saída completa:\n%s", text)
        raise ValueError("JSON incompleto")