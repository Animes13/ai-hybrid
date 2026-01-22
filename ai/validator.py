VALID_TYPES = {"episode_list", "selector_fix", "title_mapping"}

def validate_response(data, context):
    if not isinstance(data, dict):
        raise ValueError("Resposta inválida")

    if "type" not in data or "rules" not in data:
        raise ValueError("Formato inválido")

    if data["type"] not in VALID_TYPES:
        raise ValueError(f"Type inválido: {data['type']}")

    confidence = data.get("confidence", -1)
    if not (0 <= confidence <= 1):
        raise ValueError("Confidence inválido")

    rules = data["rules"]
    if not any(rules.get(k) for k in ("css", "xpath", "regex")):
        raise ValueError("Nenhuma regra retornada")

    # Se confidence for alto, regras devem ser consistentes
    if confidence >= 0.8:
        if not rules.get("css") and not rules.get("xpath"):
            raise ValueError("Confidence alta mas sem CSS/XPath")