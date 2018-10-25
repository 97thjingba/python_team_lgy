from urllib.request import urlopen
import re
html = urlopen("http://thepokerlogic.com/glossary").read().decode('utf-8')

reh = re.findall(r"<h1>(.*?)</h1>", html)

ret = re.findall(r"<head>(.*?)</head>", html)

res = re.findall(r"<p>(.*?)</p>", html)

recs = re.findall(r'href="(.*?)"', html)
rec = re.findall(r'<li>="(.*?)'.html)
print(rec)


# print(html, "\n", reh, "\n", ret, "\n", res, "\n", recs)
