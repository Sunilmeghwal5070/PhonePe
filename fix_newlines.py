import re

with open('app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('BrandIcon("Best\nDramas", Color(0xFF581c4e))', 'BrandIcon("Best\\nDramas", Color(0xFF581c4e))')

with open('app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'w') as f:
    f.write(content)
