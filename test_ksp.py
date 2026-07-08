import urllib.request
import json
url = "https://search.maven.org/solrsearch/select?q=g:com.google.devtools.ksp+a:symbol-processing-api&rows=10&wt=json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        for doc in data['response']['docs']:
            print(doc['latestVersion'])
except Exception as e:
    print(e)
