import logging
from typing import Dict, Any

from ai.engine import AIEngine
from ai.local_llm import LocalLLM
from ai.gemini import GeminiClient


log = logging.getLogger("HybridAI")


class HybridAI(AIEngine):

    def __init__(self, min_confidence: float = 0.4):
        self.local = LocalLLM()
        self.gemini = GeminiClient()
        self.min_confidence = min_confidence

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        try:
            data = self.local.analyze(context)
            conf = data.get("confidence", 0)

            log.info("Confidence LocalLLM: %.2f", conf)

            if conf >= self.min_confidence:
                data["_source"] = "local"
                return data

            log.info("Confidence baixa, fallback Gemini")

        except Exception as e:
            log.warning("LocalLLM falhou: %s", e)

        data = self.gemini.analyze(context)
        data["_source"] = "gemini"
        return data