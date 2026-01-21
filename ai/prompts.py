def build_prompt(ctx: dict) -> str:
    return f"""
Você é um analisador de HTML para scraping de alta precisão.

REGRAS ABSOLUTAS:
- Pense cuidadosamente antes de responder.
- Analise toda a estrutura do HTML.
- Verifique padrões repetidos.
- Descarte hipóteses fracas.
- NÃO invente dados.
- NÃO chute seletores.
- NÃO explique seu raciocínio.
- NÃO use markdown.
- RESPONDA APENAS COM JSON VÁLIDO.

Contexto:
Anime: {ctx.get("anime")}
URL: {ctx.get("url")}
Etapa: {ctx.get("stage")}
Erro: {ctx.get("error_type")}

HTML:
{ctx.get("html")}

Formato OBRIGATÓRIO:

{{
  "type": "episode_list | selector_fix | title_mapping",
  "confidence": 0.0,
  "rules": {{
    "css": "",
    "xpath": "",
    "regex": ""
  }}
}}
"""