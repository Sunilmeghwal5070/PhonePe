import re

with open("app/src/main/java/com/example/ui/screens/SplashScreen.kt", "r") as f:
    content = f.read()

content = content.replace("modifier = Modifier.size(150.dp)", "modifier = Modifier.size(150.dp).clip(CircleShape)")

with open("app/src/main/java/com/example/ui/screens/SplashScreen.kt", "w") as f:
    f.write(content)
