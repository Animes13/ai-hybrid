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
        data = self.local.analyze(context)
        if data.get("confidence", 0) >= self.min_confidence:
            return data

        log.info("Fallback Gemini")
        return self.gemini.analyze(context)