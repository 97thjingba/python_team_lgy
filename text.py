import requests
from bs4 import BeautifulSoup
import json
import re


def get_response(url):
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64)'
                       'AppleWebKit/537.36 (KHTML, like Gecko)'
                       'Chrome/63.0.3239.26'
                       'Safari/537.36 Core/1.63.6756.400'
                       'QQBrowser/10.3.2545.400')
    }
    return requests.get(url, headers=headers)


def parse_html(text):
    soup = BeautifulSoup(text, 'lxml')
    content = soup.find('div', class_='content')
    all_url = []
    for term_href in content.select('li a'):
        href = 'https://www.pk.cn' + term_href.get('href')
        all_url.append(href)
    all_url2 = sorted(set(all_url), key=all_url.index)
    for url in all_url2:
        if get_response(url) in [500, 404]:
            write_terms('404:该页面找不到\n')
            continue
        soup1 = BeautifulSoup(get_response(url).text, 'lxml')
        con2 = soup1.find('div', class_='glossarySection--content')
        if con2 is None:
            write_terms('无')
            continue
        title = con2.h2.text
        con2.h2.replace_with('')
        p_title = re.findall('</h2>\s*(.*?)\s*<br', str(con2), re.S)
        if len(p_title) == 0:
            p_title = '无'
        else:
            p_title = p_title[0]
        topics = con2.text.replace('\n', ' ')
        topics = topics.replace('\r', ' ')
        topics = topics.replace(' ', '')
        result = {
            "h2": title,
            "explain": p_title,
            "content": topics,
        }
        write_terms(json.dumps(result, ensure_ascii=False))


def write_terms(content):
    with open('result.json', 'a', encoding='utf-8') as file:
        file.write(content + '\n')

if __name__ == '__main__':
    rep = requests.get("http://thepokerlogic.com/glossary")
    rep.encoding = 'utf-8'
    parse_html(rep.text)