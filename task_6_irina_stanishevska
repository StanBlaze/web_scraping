import requests
from bs4 import BeautifulSoup
import json

def get_content(url):
    response = requests.get(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
    )
    return response.text

def parse_page(page_url):
    content = get_content(page_url)
    soup = BeautifulSoup(content, 'lxml')
    related_topics_elements = soup.select('a.ssrcss-1ef12hb-StyledLink.ed0g1kj0')
    related_topics = [topic.text.strip() for topic in related_topics_elements]
    return related_topics

def parse_bbc_sport():
    url = 'https://www.bbc.com/sport'
    content = get_content(url)
    soup = BeautifulSoup(content, 'lxml')
    news_items = soup.select('a.ssrcss-zmz0hi-PromoLink')
    data = []

    for news_item in news_items[:5]:
        link = news_item.get('href')
        if not link.startswith('http'):
            link = 'https://www.bbc.com' + link
        related_topics = parse_page(link)
        data.append({
            "Link": link,
            "Topics": related_topics
        })

    with open('bbc_sport_related_topics.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    parse_bbc_sport()
