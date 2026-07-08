import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace('import androidx.compose.foundation.layout.Box', 'import androidx.compose.foundation.layout.*')
content = content.replace('import androidx.compose.foundation.clickable\n', '')
content = content.replace('import androidx.compose.runtime.*', 'import androidx.compose.runtime.*\nimport androidx.compose.foundation.clickable')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

print("Imports fixed in Main")
