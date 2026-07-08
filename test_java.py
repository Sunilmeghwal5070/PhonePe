import urllib.request
import json
url = "https://api.github.com/search/issues?q=ksp.com.intellij.openapi.application.ApplicationManager.getApplication()+is+null"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())
except Exception as e:
    print(e)
