with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

imports = [
    "import androidx.compose.material.icons.filled.Person",
    "import androidx.compose.material.icons.filled.Phone"
]

for imp in imports:
    if imp not in content:
        content = content.replace("import androidx.compose.material.icons.Icons", f"{imp}\nimport androidx.compose.material.icons.Icons")

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
