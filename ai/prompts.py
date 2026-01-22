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

⚠️ INSTRUÇÃO CRÍTICA:
RESPONDA APENAS COM JSON VÁLIDO.
NÃO escreva nenhuma palavra fora do JSON.
RESPONDA EM UMA ÚNICA LINHA (SEM QUEBRA DE LINHA).

TIPOS PERMITIDOS (ESCOLHA APENAS UM):
- anime_list
- anime_page
- anime_eps
- selector_fix
- title_mapping

SE NÃO CONSEGUIR GERAR UM JSON VÁLIDO, RESPONDA EXATAMENTE COM:
{{"type":"","confidence":0.0,"rules":{{"css":"","xpath":"","regex":""}}}}

Contexto:
Anime: {ctx.get("anime")}
URL: {ctx.get("url")}
Etapa: {ctx.get("stage")}
Erro: {ctx.get("error_type")}

HTML:
{ctx.get("html")}

FORMATO OBRIGATÓRIO (EXEMPLO VÁLIDO):

{{"type":"anime_eps","confidence":0.75,"rules":{{"css":".episode-card a","xpath":"","regex":""}}}}
"""


def build_prompt_ollama_system() -> str:
    return """
Você é um analisador de HTML para scraping.

REGRAS:
- RESPONDA APENAS COM JSON VÁLIDO
- SEM EXPLICAÇÕES
- SEM MARKDOWN
- SEM TEXTO ANTES OU DEPOIS
- EM UMA ÚNICA LINHA
"""


def build_prompt_ollama_user(ctx: dict) -> str:
    return f"""
Contexto:
Anime: {ctx.get("anime")}
URL: {ctx.get("url")}
Etapa: {ctx.get("stage")}
Erro: {ctx.get("error_type")}

HTML:
{ctx.get("html")}

ESCOLHA APENAS UM DOS TIPOS ABAIXO:
- anime_list
- anime_page
- anime_eps
- selector_fix
- title_mapping

RESPONDA APENAS COM JSON VÁLIDO EM UMA LINHA.
NÃO escreva nenhuma palavra fora do JSON.

FORMATO OBRIGATÓRIO (EXEMPLO):

{{"type":"anime_page","confidence":0.6,"rules":{{"css":"h1.title","xpath":"","regex":""}}}}

SE NÃO CONSEGUIR GERAR JSON VÁLIDO, RESPONDA EXATAMENTE:

{{"type":"","confidence":0.0,"rules":{{"css":"","xpath":"","regex":""}}}}
"""