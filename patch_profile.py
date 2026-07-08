import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('import androidx.compose.ui.text.style.TextAlign\npackage com.example.ui.screens', 'package com.example.ui.screens\nimport androidx.compose.ui.text.style.TextAlign')

with open('/app/applet/app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.write(content)
