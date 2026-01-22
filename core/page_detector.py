def detect_page_type(html: str) -> str:
    h = html.lower()

    if "lista-de-animes" in h:
        return "anime_list"

    if "episódios" in h or "allEpisodes" in h:
        return "anime_eps"

    if "<h1" in h and "episódio" not in h:
        return "anime_page"

    return "unknown"