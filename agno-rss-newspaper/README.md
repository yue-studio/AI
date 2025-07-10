# Agno RSS summary

This project contains a Python script (`rss-sum.py`) that demonstrates how to use an Agno (https://github.com/agno-agi/agno) agent to summarize RSS feeds using newspaper as the tool.
It also uses the local LLM via ollama.

The following were implemented:

1.  **Local LLM**
    *   Uses llama3.2 via Ollama (https://ollama.com/)

2.  **Newspaper3k: Article scraping & curation**
    *   Uses Newspaper to summarize the article.
    *   https://newspaper.readthedocs.io/en/latest/

3.  **Feedparser**
    *   Uses Feedparser (https://pypi.org/project/feedparser/)) to get the rss feed specified in `feed.opml`

