import re

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

content = content.replace("border = borderStroke(", "border = androidx.compose.foundation.BorderStroke(1.dp, ")
content = re.sub(r"@Composable\nfun borderStroke.*$", "", content, flags=re.MULTILINE)

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/WrongPinScreen.kt", "r") as f:
    content = f.read()

content = content.replace("border = borderStroke(", "border = androidx.compose.foundation.BorderStroke(1.dp, ")
content = re.sub(r"@Composable\nfun borderStroke.*$", "", content, flags=re.MULTILINE)

with open("app/src/main/java/com/example/ui/screens/WrongPinScreen.kt", "w") as f:
    f.write(content)
