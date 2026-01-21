def validate_response(data, context):
    if not isinstance(data, dict):
        raise ValueError("Resposta inválida")

    if "type" not in data or "rules" not in data:
        raise ValueError("Formato inválido")

    c = data.get("confidence", -1)
    if not (0 <= c <= 1):
        raise ValueError("Confidence inválido")

    rules = data["rules"]
    if not any(rules.get(k) for k in ("css", "xpath", "regex")):
        raise ValueError("Nenhuma regra retornada")