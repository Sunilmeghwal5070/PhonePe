with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

import re
content = re.sub(r'// 1\. Realistic White Top Header.*?// 2\. Beautiful', '// 2. Beautiful', content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
