from bs4 import BeautifulSoup
import requests


def parsing(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find_all("meta", property=["og:title", "og:type", "og:image"])
    title_dict = {_['property'][3:]: _['content'] for _ in title}
    if not title:
        tag_meta = soup.find("meta", attrs={"name":"description"})
        tag_meta_dict = {tag_meta['name']: tag_meta['content']}
        tag_title = soup.find('title')
        tag_title_dict = {tag_title.name: tag_title.string}
        print({**tag_meta_dict, **tag_title_dict})
        return {**tag_meta_dict, **tag_title_dict}
    return title_dict


