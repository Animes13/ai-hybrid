import json
import os

RULES_DIR = "rules"

def save_rules(page_type: str, data: dict):
    os.makedirs(RULES_DIR, exist_ok=True)

    mapping = {
        "anime_list": "page_anime_list.json",
        "anime_page": "page_anime.json",
        "anime_eps": "page_animes_eps.json"
    }

    filename = mapping.get(page_type)
    if not filename:
        return

    path = os.path.join(RULES_DIR, filename)

    rules = []
    if os.path.exists(path):
        rules = json.load(open(path, "r", encoding="utf-8"))

    rules.append(data)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)