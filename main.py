from ai.hybrid import HybridAI

ctx = {
    "anime": "Naruto",
    "url": "https://site.com",
    "stage": "episode_list",
    "error_type": None,
    "html": "<html>...</html>"
}

ai = HybridAI()
result = ai.analyze(ctx)

print("TIPO:", type(result))
print("RESULTADO:", result)