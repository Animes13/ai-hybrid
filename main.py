from ai.hybrid import HybridAI

ctx = {
    "anime": "Naruto",
    "url": "https://site.com",
    "stage": "episode_list",
    "error_type": None,
    "html": "<html>...</html>"
}

ai = HybridAI()
print(ai.analyze(ctx))