import urllib3
http = urllib3.PoolManager()
r = http.request('GET','http://thepokerlogic.com/glossary')
print (r.data.decode('utf-8'))