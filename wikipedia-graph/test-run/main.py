import requests
import re
import json
from collections import deque
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_html(title):
    url = f"https://en.wikipedia.org/wiki/{title}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def extract_internal_links_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()

    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/wiki/') and ':' not in href:
            title = href.split('/wiki/')[1].split('#')[0]
            links.add(title)

    return list(links)


def crawl_graph(seed_title, max_pages=100):
    visited = set()
    queue = deque([seed_title])
    graph = {}

    with tqdm(total=max_pages) as pbar:
        while queue and len(visited) < max_pages:
            title = queue.popleft()
            if title in visited:
                continue

            try:
                html = get_html(title)
                links = extract_internal_links_from_html(html)
            except Exception as e:
                print(f"Error fetching {title}: {e}")
                continue

            graph[title] = links
            visited.add(title)
            pbar.update(1)

            for link in links:
                if link not in visited and link not in queue:
                    queue.append(link)

    return graph


if True:
    seed = "Philosophy"
    graph = crawl_graph(seed, max_pages=10_000) #Did this in first test run, took me 8 hours around.

    with open("wiki_text_graph_modified.json", "w", encoding='utf-8') as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)

    # print("Saved graph to wiki_text_graph.json")
