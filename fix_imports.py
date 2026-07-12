with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    text = f.read()

imports = [
    "import androidx.compose.animation.AnimatedVisibility",
    "import androidx.compose.animation.slideInVertically",
    "import androidx.compose.animation.slideOutVertically"
]

for imp in imports:
    if imp not in text:
        text = text.replace("import androidx.compose.animation.core.*", f"{imp}\nimport androidx.compose.animation.core.*")

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(text)

