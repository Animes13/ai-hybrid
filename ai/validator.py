VALID_TYPES = {
    "anime_list",
    "anime_page",
    "anime_eps",
    "selector_fix",
    "title_mapping"
}


def validate_response(data: dict, context: dict):
    if not isinstance(data, dict):
        raise ValueError("Resposta não é dict")

    if "type" not in data or "rules" not in data:
        raise ValueError("Formato inválido")

    if data["type"] not in VALID_TYPES and data["type"] != "":
        raise ValueError(f"Type inválido: {data['type']}")

    confidence = data.get("confidence", 0.0)
    if not isinstance(confidence, (int, float)) or not (0 <= confidence <= 1):
        raise ValueError("Confidence inválido")

    rules = data.get("rules", {})
    if not isinstance(rules, dict):
        raise ValueError("Rules inválido")

    if not any(rules.get(k) for k in ("css", "xpath", "regex")):
        raise ValueError("Nenhuma regra retornada")

    if confidence >= 0.8 and not (rules.get("css") or rules.get("xpath")):
        raise ValueError("Confidence alta sem seletor forte")