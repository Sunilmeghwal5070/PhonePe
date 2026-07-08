import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Replace maxLines = 1, overflow = TextOverflow.Ellipsis with maxLines = 2 for ads
content = content.replace("maxLines = 2,\n                            overflow = TextOverflow.Ellipsis", "maxLines = 2,\n                            overflow = TextOverflow.Visible")

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
