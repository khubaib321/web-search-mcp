from . import _pages
from typing import Generator
import googlesearch as _gsearch


def _google_search(query: str, num_pages: int) -> Generator[str]:
    for result in _gsearch.search(query, num_results=num_pages, unique=True):
        if isinstance(result, str):
            yield result

        elif isinstance(result, _gsearch.SearchResult):
            yield result.url

def google_search_with_content(query: str, num_pages: int) -> Generator[tuple[str, str | None]]:
    for url in _google_search(query=query, num_pages=num_pages):
        try:
            yield url, _pages.get_page_content_single(url)
        except Exception as e:
            print(f"-> {str(e)}", flush=True)
            yield url, None
