with open('app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("but since it's a prank app", "but since camera is disabled")

with open('app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'w') as f:
    f.write(content)
