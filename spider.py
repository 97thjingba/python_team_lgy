import requests
from bs4 import BeautifulSoup

rep = requests.get("http://thepokerlogic.com/glossary")
soup = BeautifulSoup(rep.text, 'lxml')
print(soup.h2)
#抓网页上的<p>内容
han_name = "p.glossary-describe"
han = soup.select(han_name)
for h in han:
    print(h)
#抓网页上的链接和文字
href_name = 'a'
href = soup.select(href_name)
for hr in href:
    print(hr['href'], hr.text)
#抓取链接内容
# url = 'http://thepokerlogic.com/glossary'
# div_name = 'div.content_a a'
# divs = soup.select(div_name)
# for div in divs:
#     print(divs)








