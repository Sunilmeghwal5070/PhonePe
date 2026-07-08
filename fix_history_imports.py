with open('app/src/main/java/com/example/ui/screens/HistoryScreen.kt', 'r') as f:
    content = f.read()

if "import androidx.compose.foundation.border" not in content:
    content = content.replace("import androidx.compose.foundation.clickable", "import androidx.compose.foundation.clickable\nimport androidx.compose.foundation.border")

with open('app/src/main/java/com/example/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(content)
