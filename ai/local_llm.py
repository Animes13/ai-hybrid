import subprocess, json, re
from typing import Dict, Any
from ai.engine import AIEngine
from ai.prompts import build_prompt
from ai.validator import validate_response

class LocalLLM(AIEngine):
    MODEL = "qwen2.5:7b"

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = build_prompt(context)

        r = subprocess.run(
            ["ollama", "run", self.MODEL],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=120
        )

        if r.returncode != 0:
            raise RuntimeError(r.stderr)

        data = self._safe_json(r.stdout)
        validate_response(data, context)
        return data

    def _safe_json(self, text: str):
        text = re.sub(r"```(?:json)?", "", text)
        start, end = text.find("{"), text.rfind("}") + 1
        return json.loads(text[start:end])