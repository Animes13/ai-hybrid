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

⚠️ INSTRUÇÃO IMPORTANTE:
RESPONDA APENAS COM JSON VÁLIDO SEM NENHUM TEXTO EXTRA, NEM UMA PALAVRA ANTES OU DEPOIS.
RESPONDA EM UMA LINHA SOMENTE (SEM QUEBRAS DE LINHA).

SE VOCÊ NÃO CONSEGUIR GERAR UM JSON VÁLIDO, RESPONDA EXATAMENTE COM:
{{{{"type": "", "confidence": 0.0, "rules": {{{{"css": "", "xpath": "", "regex": ""}}}}}}}}

Contexto:
Anime: {ctx.get("anime")}
URL: {ctx.get("url")}
Etapa: {ctx.get("stage")}
Erro: {ctx.get("error_type")}

HTML:
{ctx.get("html")}

Formato OBRIGATÓRIO (EXATO):

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

def build_prompt_ollama(ctx: dict) -> str:
    return f"""
Você é um analisador de HTML para scraping de alta precisão.

⚠️ REGRAS ABSOLUTAS (Ollama):
- RESPONDA APENAS COM JSON VÁLIDO.
- NÃO explique nada.
- NÃO use markdown.
- NÃO use texto antes ou depois do JSON.
- NÃO use quebras de linha (responda em UMA LINHA).
- Se não conseguir gerar JSON válido, responda exatamente com o JSON padrão abaixo.

Contexto:
Anime: {ctx.get("anime")}
URL: {ctx.get("url")}
Etapa: {ctx.get("stage")}
Erro: {ctx.get("error_type")}

HTML:
{ctx.get("html")}

JSON OBRIGATÓRIO (EXATO):

{{"type": "episode_list | selector_fix | title_mapping", "confidence": 0.0, "rules": {{"css": "", "xpath": "", "regex": ""}}}}

Se não conseguir gerar JSON válido, responda exatamente:

{{"type": "", "confidence": 0.0, "rules": {{"css": "", "xpath": "", "regex": ""}}}}
"""