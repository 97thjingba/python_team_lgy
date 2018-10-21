from urllib.request import urlopen
import re
html = urlopen("http://thepokerlogic.com/glossary").read().decode('utf-8')
print(html)
reh = re.findall(r"<h1>(.*?)</h1>", html)
print("h1\n", reh)
ret = re.findall(r"<head>(.*?)</head>", html)
print("title\n", ret)
res = re.findall(r"<p>(.*?)</p>", html)
print("p\n", res)
recs = re.findall(r'href="(.*?)"', html)
print("href\n", recs)
