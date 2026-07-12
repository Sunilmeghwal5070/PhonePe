import re
with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("    val context = LocalContext.current\n    var networkStatus", "    var networkStatus")

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(text)

