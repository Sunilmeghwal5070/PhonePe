import re

with open('app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt', 'r') as f:
    text = f.read()

# Fix selectedBank initialization
text = text.replace("    var selectedBank by remember { mutableStateOf(bankAccounts.firstOrNull()) }", "    var selectedBank by remember(bankAccounts) { mutableStateOf(bankAccounts.firstOrNull()) }")

with open('app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt', 'w') as f:
    f.write(text)
