import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch

load_dotenv()

tavily_tool = TavilySearch( max_results=5)

def search_tavily(query: str) -> str:
    response = tavily_tool.invoke({
        "query": query
    })

    results = []

    for i, r in enumerate(response.get("results", []), 1):
        title = r.get("title", "Unknown")
        url = r.get("url", "")
        snippet = r.get("content", "").strip()

        if len(snippet) > 300:
            snippet = snippet[:300].rsplit(" ", 1)[0] + "..."

        results.append(
            f"{i}. {title}\n{url}\n{snippet}"
        )

    return "\n\n".join(results)