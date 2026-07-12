import re

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("@Composable\nimport com.example.ui.PrankViewModel\nfun QrScreen", "@Composable\nfun QrScreen")
text = text.replace("package com.example.ui.screens", "package com.example.ui.screens\n\nimport com.example.ui.PrankViewModel\n")

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'w') as f:
    f.write(text)

