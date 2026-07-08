import re

with open('/app/applet/app/src/main/java/com/example/ui/PrankViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace('"Union Bank"', '"State Bank of India"')
content = content.replace('"Union Bank Of India - 0365"', '"State Bank Of India - 0365"')

with open('/app/applet/app/src/main/java/com/example/ui/PrankViewModel.kt', 'w') as f:
    f.write(content)

