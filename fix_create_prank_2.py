import re

with open('app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("    var senderBankLast4 by remember { mutableStateOf((1000..9999).random().toString()) }", "    var senderBankLast4 by remember(selectedBank) { mutableStateOf(selectedBank?.bankDesc?.takeLast(4) ?: (1000..9999).random().toString()) }")

with open('app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt', 'w') as f:
    f.write(text)
