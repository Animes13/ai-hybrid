import os

HTML_DIR = "HTML"

def save_html(name: str, html: str):
    os.makedirs(HTML_DIR, exist_ok=True)
    path = os.path.join(HTML_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path