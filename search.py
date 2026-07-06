from config import tavily_client


def web_search(query):
    search = tavily_client.search(
        query=query,
        search_depth="basic",
        max_results=3
    )

    context = ""

    for result in search["results"]:
        context += (
            f"Title: {result.get('title', '')}\n"
            f"Content: {result.get('content', '')}\n"
            f"Source: {result.get('url', '')}\n\n"
        )

    return context, search["results"]