import xml.etree.ElementTree as ET
import feedparser
from rich.console import Console
from agno.agent import Agent
from agno.tools.newspaper import NewspaperTools
from agno.models.ollama import Ollama

opml_file = 'feed.opml'

# --- Setup ---
console = Console()
agent = Agent(
    name="RSS Summarizer",
    model=Ollama(id="llama3.2", provider="Ollama"),
    tools=[NewspaperTools()],
    show_tool_calls=False,
    markdown=True,
)

# --- Functions from read_opml.py ---
def parse_opml(file_path):
    """Parses an OPML file and yields a dictionary for each RSS feed found."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for outline in root.findall('.//outline[@type="rss"]'):
            yield {
                'text': outline.attrib.get('text'),
                'title': outline.attrib.get('title'),
                'xmlUrl': outline.attrib.get('xmlUrl'),
                'htmlUrl': outline.attrib.get('htmlUrl'),
            }
    except FileNotFoundError:
        console.print(f"[red]Error: OPML file not found at '{file_path}'[/red]")
        return
    except ET.ParseError:
        console.print(f"[red]Error: Failed to parse OPML file at '{file_path}'[/red]")
        return


def get_latest_articles(feed_url, num_articles=5):
    """Fetches the latest articles from an RSS feed."""
    try:
        feed = feedparser.parse(feed_url)
        return feed.entries[:num_articles]
    except Exception as e:
        console.print(f"[red]Error fetching feed: {e}[/red]")
        return []

# --- Main Execution ---
if __name__ == "__main__":
    console.print("[bold #00FFFF]Starting RSS Feed Summarization...[/bold #00FFFF]")

    for feed_data in parse_opml(opml_file):
        title = feed_data.get('title') or feed_data.get('text', 'No title')
        xml_url = feed_data.get('xmlUrl')

        console.print(f"\n[bold #FFD700]## Processing Feed: {title}[/bold #FFD700]")

        if not xml_url:
            console.print("- No XML URL found. Skipping.")
            continue

        articles = get_latest_articles(xml_url, num_articles=5)

        if not articles:
            console.print("- No articles found in the feed.")
            continue

        # Summarize the first article
        first_article = articles[0]
        article_title = getattr(first_article, 'title', 'No Title Available')
        article_link = getattr(first_article, 'link', None)

        if article_link:
            console.print(f"- Summarizing article: [link={article_link}]{article_title}[/link]")
            try:
                response = agent.run(f"Please summarize {article_link}")
                console.print(response.content)
            except Exception as e:
                console.print(f"[red]Error during summarization: {e}[/red]")
        else:
            console.print("- No link available for this article, cannot summarize.")

        # Display the next 4 articles
        if len(articles) > 1:
            console.print("\n[bold #ADD8E6]Other recent articles:[/bold #ADD8E6]")
            for article in articles[1:]:
                next_article_title = getattr(article, 'title', 'No Title Available')
                next_article_link = getattr(article, 'link', None)
                if next_article_link:
                    console.print(f"- [link={next_article_link}]{next_article_title}[/link]")
                else:
                    console.print(f"- {next_article_title} (No link available)")


    console.print("\n[bold #00FFFF]Finished summarizing all feeds.[/bold #00FFFF]")
