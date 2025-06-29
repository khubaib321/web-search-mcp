import bs4 as _bs4
import urllib.request as _url_req


def get_page_content_single(url: str) -> str | None:
    print("get_page_content_single:", url, flush=True)
    
    # HEAD request = headers only, no body download (Python 3.9+)
    head_req  = _url_req.Request(url, method="HEAD")
    head_resp = _url_req.urlopen(head_req, timeout=3)
    content_type = head_resp.headers.get("Content-Type", "")

    if not content_type.startswith("text/html"):
        print("-> No text content available on this page.", flush=True)
        return None
    
    html = _url_req.urlopen(url).read()
    soup = _bs4.BeautifulSoup(html, features="html.parser")

    raw_text = soup.get_text(separator="\n", strip=True)
    text_lines = [t.strip() for t in raw_text.split("\n")]

    clean_text = " ".join(text_lines)
    clean_text_truncated = f"{clean_text:.200}"
    truncated_text_length = len(clean_text) - 200
    print(f"-> {clean_text_truncated} ...[truncated {truncated_text_length:,} characters]", flush=True)

    return clean_text
