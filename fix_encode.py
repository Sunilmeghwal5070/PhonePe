import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

text = re.sub(r'java\.net\.URLEncoder\.encode\(([^,]+),\s*"UTF-8"\)', r'Uri.encode(\1)', text)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)
