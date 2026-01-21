from typing import Dict, Any
from ai.engine import AIEngine
from ai.local_llm import LocalLLM
from ai.gemini import GeminiClient

class HybridAI(AIEngine):

    def __init__(self, min_confidence=0.4):
        self.local = LocalLLM()
        self.gemini = GeminiClient()
        self.min_confidence = min_confidence

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        try:
            data = self.local.analyze(context)
            if data.get("confidence", 0) >= self.min_confidence:
                data["_source"] = "local"
                return data
        except Exception:
            pass

        data = self.gemini.analyze(context)
        data["_source"] = "gemini"
        return data