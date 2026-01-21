from abc import ABC, abstractmethod
from typing import Dict, Any


class AIEngine(ABC):

    @abstractmethod
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass