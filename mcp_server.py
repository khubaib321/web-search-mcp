import asyncio as _aio
import fastmcp as _fastmcp
import pydantic as _pydantic

import lib as _lib


mcp = _fastmcp.FastMCP("Web search tools")


class SinglePageContentResponse(_pydantic.BaseModel):
    content: str | None


class GoogleSearchResponse(_pydantic.BaseModel):
    results: dict[str, str]


@mcp.tool(
    name="google-search",
    description="""
    Perform a quick google with the given text and return links top num_pages web pages.

    Returns a list containing url and the corresponding web page content.
    """
)
def google_search(text: str) -> GoogleSearchResponse:
    num_pages = 5
    print("=============================================")
    print("Searching for:", f"'{text}'", "- reading top", num_pages, "results", flush=True)

    results: dict[str, str] = {}
    for url, content in _lib.google_search_with_content(query=text, num_pages=num_pages):
        if content is None:
            continue

        results[url] = content

    return GoogleSearchResponse(results=results)


@mcp.tool(
    name="get-web-page-content",
    description="""
    Get a web page contents as Markdown text.
    """
)
def get_web_page_content(url: str) -> SinglePageContentResponse:
    print("=============================================")
    print("Reading web page:", f"'{url}'", flush=True)

    result = _lib.get_page_content_single(url)

    return SinglePageContentResponse(content=result)


if __name__ == "__main__":
    # mcp.run()
    # mcp.run("streamable-http")
    _aio.run(mcp.run_http_async(transport="sse", port=8002))
