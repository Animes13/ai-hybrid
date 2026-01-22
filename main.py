import json
import os
import logging
from ai.hybrid import HybridAI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# Coloque o HTML real dentro da pasta HTML/
html_path = "HTML/ep1.html"

if not os.path.exists(html_path):
    raise FileNotFoundError(f"Arquivo não encontrado: {html_path}")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

ctx = {
    "anime": "Naruto",
    "url": "https://site.com",
    "stage": "episode_list",
    "error_type": None,
    "html": html
}

ai = HybridAI()
result = ai.analyze(ctx)

print("TIPO:", type(result))
print("RESULTADO:", json.dumps(result, ensure_ascii=False, indent=2))