# utils/scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

HEADERS = {"User-Agent": "Mozilla/5.0"}

def google_search_query(query, num=5):
    params = {"q": query, "num": num}
    url = "https://www.google.com/search?" + urlencode(params)
    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    for g in soup.select('.tF2Cxc')[:num]:
        title = g.select_one('.DKV0Md') or g.select_one('h3')
        link_tag = g.select_one('a')
        snippet = g.select_one('.VwiC3b') or g.select_one('.IsZvec')

        if link_tag and title:
            results.append({
                "title": title.get_text(strip=True),
                "link": link_tag["href"],
                "snippet": snippet.get_text(strip=True) if snippet else ""
            })

    return results
