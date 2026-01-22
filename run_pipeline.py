from core.fetcher import Fetcher
from core.html_store import save_html
from core.page_detector import detect_page_type
from ai.hybrid import HybridAI
from core.rule_generator import save_rules

URLS = [
    "https://goyabu.io/lista-de-animes/page/1?l=todos&pg=1",
    "https://goyabu.io/anime/one-piece-dublado-online",
    "https://goyabu.io/40431"
]

fetcher = Fetcher()
ai = HybridAI()

for url in URLS:
    print(f"🔽 Baixando {url}")
    html = fetcher.get(url)

    filename = url.split("/")[-1] or "index"
    path = save_html(f"{filename}.html", html)

    page_type = detect_page_type(html)
    print(f"📄 Tipo detectado: {page_type}")

    if page_type == "unknown":
        continue

    context = {
        "url": url,
        "html": html,
        "stage": page_type
    }

    result = ai.analyze(context)

    save_rules(page_type, result)

    print(f"✅ Regras salvas para {page_type}\n")