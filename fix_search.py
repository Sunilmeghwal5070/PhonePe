with open('app/src/main/java/com/example/ui/screens/SearchScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("FASTag recharging is a prank!", "FASTag recharging is currently unavailable.")

with open('app/src/main/java/com/example/ui/screens/SearchScreen.kt', 'w') as f:
    f.write(content)
