from abc import ABC, abstractmethod
from typing import Dict, Any


class AIEngine(ABC):

    @abstractmethod
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deve SEMPRE retornar:
        {
          "type": str,
          "confidence": float (0-1),
          "rules": { "css": str, "xpath": str, "regex": str }
        }
        """
        raise NotImplementedError