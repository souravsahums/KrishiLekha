from langchain.tools import Tool
from bs4 import BeautifulSoup
import requests

def scrape_agri_portal(query):
    search_url = f"https://www.google.com/search?q=site:agricoop.nic.in+{query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    snippets = soup.select("div.BNeawe.s3v9rd.AP7Wnd")
    return "\n".join([s.text for s in snippets[:5]])

def web_scraper_tool():
    return Tool.from_function(
        func=scrape_agri_portal,
        name="Agri Web Scraper",
        description="Useful for getting live data from Indian agriculture websites for user questions."
    )
