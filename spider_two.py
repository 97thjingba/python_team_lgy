import requests
from bs4 import BeautifulSoup
import json

def parse_html(text):
    soup = BeautifulSoup(text, 'lxml')
    url_href = soup.select('.content_a a')
    all_url = []
    for url in url_href:
        all_url.append(url['href'])
    all_url2 = sorted(set(all_url), key=all_url.index)
    for href in all_url2:
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
            content_text = [c.string, c['href']]
        study = soup1.select('.study-content a')
        if len(study) == 0:
            study_text = '无'
        else:
            for i in study:
                study_text = [i.string, i['href']]


        h3_title = h3_text[0].string
        explain = p_text[4].string
        example = h4_text[0].string
        p_text = p_text[5].string
        h4_text = h4_text[1].string

        """
        建立字典
        """

        result = {
            'title': h2_title,
            'describe_title': h3_title,
            'describe_content': explain,
            'illustrate_title': example,
            'Illustrate_content': p_text,
            'relevant_title': h4_text,
            'relevant_content': content_text,
            'Study_content': study_text,
         }
        write_file(result)


def write_file(data):
    with open('spider.json', 'a', encoding='utf-8') as f:
        f.write('\n' + json.dumps(data, ensure_ascii=False))
        f.close()



def main():
    rep = requests.get("http://thepokerlogic.com/glossary")
    parse_html(rep.text)



main()