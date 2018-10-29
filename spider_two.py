import requests
from bs4 import BeautifulSoup
import json

def parse_html(text):
    soup = BeautifulSoup(text, 'lxml')
    url_href = soup.select('.content_a a')
    allurl = []
    for url in url_href:
        allurl.append(url['href'])
    for href in allurl:
        url_new = 'http://thepokerlogic.com' + str(href)   #拼接链接
        data = requests.get(url_new).text
        soup1 = BeautifulSoup(data, 'lxml')
        h2_text = soup1.select('.glossary-detail-title')   #开始查找文件
        h3_text = soup1.find_all('h3')
        p_text = soup1.find_all('p')
        h4_text = soup1.find_all('h4')
        if len(h2_text) == 0:
            pass
        else:
            h2_title = h2_text[0].string
        content_a = soup1.select('.relevant-content a')
        for c in content_a:
            content_text = c.string
        study = soup1.select('.study-content a')
        if len(study) == 0:
            study_text = '无'
        else:
            for i in study:
                study_text = i.string

        h3_title = h3_text[0].string
        explain = p_text[4].string
        example = h4_text[0].string
        p_text = p_text[5].string
        h4_text = h4_text[1].string
        """
        建立字典
        """

        result = {
            'first_title': h2_title,
            'second_title': h3_title,
            'title_explain': explain,
            'Illustrate': example,
            'Illustrate_content': p_text,
            'Concept': h4_text,
            'Concept_content': content_text,
            'Study_content': study_text,
        }
        write_file(result)


def write_file(data):
    with open('spider_text.json', 'a', encoding='utf-8') as f:
        f.write('\n' + json.dumps(data, ensure_ascii=False))
        f.close()



def main():
    rep = requests.get("http://thepokerlogic.com/glossary")
    parse_html(rep.text)



main()
