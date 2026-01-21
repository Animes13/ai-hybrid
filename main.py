import logging
from ai.hybrid import HybridAI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

ctx = {
    "anime": "Naruto",
    "url": "https://site.com",
    "stage": "episode_list",
    "error_type": None,
    "html": "<html>...</html>"
}

ai = HybridAI()
result = ai.analyze(ctx)

print("TIPO:", type(result))
print("RESULTADO:", result)